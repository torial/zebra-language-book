#!/usr/bin/env python3
"""
Zebra Programming Book - Code Example Extractor

Extracts all code examples from markdown chapters into individual .zbr files.
Maintains organization by chapter and metadata from code blocks.

Usage:
    python3 extract-examples.py

Output:
    examples/
    ├── 01-getting-started/
    │   ├── 01_hello_world.zbr
    │   └── ...
    ├── 02-values-and-types/
    │   ├── 02_integers.zbr
    │   └── ...
    └── manifest.json (index of all examples)
"""

import os
import re
import sys as _sys
try:  # Windows consoles default to cp1252 and choke on the check marks
    _sys.stdout.reconfigure(encoding='utf-8')
    _sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass
import json
import sys
from pathlib import Path
from typing import List, Dict, Tuple

class ExampleExtractor:
    def __init__(self, book_root: str = "."):
        self.book_root = Path(book_root)
        self.examples_dir = self.book_root / "examples"
        self.examples = []

    def create_directories(self):
        """Create examples directory structure."""
        self.examples_dir.mkdir(exist_ok=True)
        print(f"✓ Created {self.examples_dir}/")

    def find_chapters(self) -> List[Tuple[str, Path]]:
        """Find all chapter markdown files."""
        chapters = []

        # Search in Part directories.  The chapters live under book/Part-*; the
        # original glob looked for Part-* at the REPO ROOT, which matched nothing
        # after the reorg -- find_chapters() returned [] and the script still exited
        # 0, so extraction quietly became a no-op (and validation kept re-checking
        # months-old files).  Search both layouts, and fail loudly if neither exists.
        part_dirs = sorted(self.book_root.glob("book/Part-*"))
        if not part_dirs:
            part_dirs = sorted(self.book_root.glob("Part-*"))
        if not part_dirs:
            raise SystemExit(
                "extract-examples: no Part-* chapter directories found under "
                + str(self.book_root.resolve())
                + " -- refusing to silently extract nothing.")
        for part_dir in part_dirs:
            if not part_dir.is_dir():
                continue

            for md_file in sorted(part_dir.glob("*.md")):
                # Extract chapter name from filename
                chapter_name = md_file.stem
                chapters.append((chapter_name, md_file))

        return chapters

    def extract_code_blocks(self, chapter_name: str, content: str) -> List[Dict]:
        """Extract all code blocks from markdown content."""
        code_blocks = []

        # Match ```zebra ... ``` blocks
        pattern = r'```zebra\n(.*?)```'

        for match in re.finditer(pattern, content, re.DOTALL):
            code = match.group(1).strip()
            if not code:
                continue

            # Parse metadata from code comments
            metadata = self._parse_metadata(code)
            metadata['chapter'] = chapter_name
            metadata['content'] = code
            metadata['index'] = len(code_blocks)

            code_blocks.append(metadata)

        return code_blocks

    def _parse_metadata(self, code: str) -> Dict:
        """Extract metadata from code block comments."""
        metadata = {
            'file': None,
            'teaches': None,
            'project': None,
        }

        # Look for comment lines at the start.  Accept BOTH comment styles:
        # Zebra comments are `#`; the `//` form is Cobra-era and survives only in
        # older chapters.  Recognising only `//` meant every modern block lost its
        # filename and was dropped by write_example -- silently, with exit 0.
        lines = code.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            for prefix in ('# ', '// '):
                for key in ('file', 'teaches', 'project'):
                    marker = prefix + key + ':'
                    if marker in line:
                        metadata[key] = line.split(marker)[1].strip()

        return metadata

    def create_chapter_dir(self, chapter_name: str) -> Path:
        """Create chapter subdirectory."""
        # Convert chapter name to directory format
        # 01-Getting-Started -> 01-getting-started
        chapter_dir = self.examples_dir / chapter_name.lower().replace(' ', '-')
        chapter_dir.mkdir(exist_ok=True)
        return chapter_dir

    def write_example(self, chapter_dir: Path, metadata: Dict) -> bool:
        """Write code example to file."""
        if not metadata['file']:
            # No `file:` header -- synthesise a stable name rather than dropping the
            # block.  Silently discarding unnamed blocks is what made this tool report
            # zero examples per chapter while still exiting successfully.
            slug = metadata.get('chapter', 'block').lower().replace(' ', '-')
            metadata['file'] = slug + '_' + str(metadata.get('index', 0)).zfill(3) + '.zbr'

        filepath = chapter_dir / metadata['file']

        try:
            # newline= LF is REQUIRED: Python on Windows writes CRLF by
            # default and the Zebra tokenizer rejects CR with
            # error.UnexpectedCharacter and no source location.
            with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
                f.write(metadata['content'])
            return True
        except Exception as e:
            print(f"  ✗ Error writing {filepath}: {e}")
            return False

    def process_chapters(self) -> int:
        """Process all chapters and extract examples."""
        chapters = self.find_chapters()
        total_examples = 0

        if not chapters:
            print("✗ No chapters found!")
            return 0

        print(f"Found {len(chapters)} chapters\n")

        for chapter_name, chapter_path in chapters:
            print(f"📖 {chapter_name}:")

            try:
                with open(chapter_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                print(f"  ✗ Error reading {chapter_path}: {e}")
                continue

            # Extract code blocks
            code_blocks = self.extract_code_blocks(chapter_name, content)

            if not code_blocks:
                print(f"  (no examples)")
                continue

            # Create chapter directory
            chapter_dir = self.create_chapter_dir(chapter_name)

            # Write each example
            written = 0
            for block in code_blocks:
                if self.write_example(chapter_dir, block):
                    written += 1
                    self.examples.append({
                        'chapter': chapter_name,
                        'file': block['file'],
                        'teaches': block['teaches'],
                        'project': block.get('project'),
                        'path': str(chapter_dir / block['file']).replace('\\', '/')
                    })

            print(f"  ✓ Extracted {written} examples → {chapter_dir.name}/")
            total_examples += written

        return total_examples

    def create_manifest(self):
        """Create JSON manifest of all examples."""
        manifest = {
            'version': '1.0',
            'total_examples': len(self.examples),
            'generated': str(Path(__file__).stat().st_mtime),
            'examples': self.examples
        }

        manifest_path = self.examples_dir / "manifest.json"

        try:
            with open(manifest_path, 'w', encoding='utf-8', newline='\n') as f:
                json.dump(manifest, f, indent=2)
            print(f"\n✓ Created manifest: {manifest_path}")
            return True
        except Exception as e:
            print(f"\n✗ Error creating manifest: {e}")
            return False

    def create_readme(self):
        """Create README for examples directory."""
        readme_path = self.examples_dir / "README.md"

        readme_content = f"""# Zebra Programming Book - Code Examples

This directory contains {len(self.examples)} runnable code examples extracted from the Zebra Programming Book.

## Organization

Examples are organized by chapter:

```
examples/
├── 01-getting-started/
├── 02-values-and-types/
├── 03-collections/
├── ...
└── manifest.json
```

## Running Examples

Each `.zbr` file is a complete, runnable program:

```bash
zebra examples/01-getting-started/01_hello_world.zbr
```

## Example Manifest

See `manifest.json` for a complete index of all examples with metadata:
- Chapter name
- What concept each example teaches
- Associated project (if any)

## Testing All Examples

Run the validation script:

```bash
python3 ../validate-examples.py
```

This compiles and tests each example to ensure correctness.

## By the Numbers

- **Total Examples:** {len(self.examples)}
- **Chapters Covered:** {len(set(e['chapter'] for e in self.examples))}
- **Topics:** {len(set(e['teaches'] for e in self.examples if e['teaches']))}

## Quick Reference

### Examples by Chapter

"""

        # Group by chapter
        by_chapter = {}
        for example in self.examples:
            chapter = example['chapter']
            if chapter not in by_chapter:
                by_chapter[chapter] = []
            by_chapter[chapter].append(example)

        for chapter in sorted(by_chapter.keys()):
            examples = by_chapter[chapter]
            readme_content += f"\n### {chapter} ({len(examples)} examples)\n"
            for ex in examples:
                teaches = ex['teaches'] or 'basic example'
                readme_content += f"- `{ex['file']}` — {teaches}\n"

        try:
            with open(readme_path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(readme_content)
            print(f"✓ Created README: {readme_path}")
            return True
        except Exception as e:
            print(f"✗ Error creating README: {e}")
            return False

    def run(self):
        """Run the extraction process."""
        print("=" * 60)
        print("Zebra Programming Book - Code Example Extractor")
        print("=" * 60)
        print()

        # Create directories
        self.create_directories()
        print()

        # Process chapters
        total = self.process_chapters()

        if total == 0:
            print("\n✗ No examples extracted!")
            return False

        print(f"\n{'=' * 60}")
        print(f"✓ Successfully extracted {total} examples!")
        print(f"{'=' * 60}\n")

        # Create manifest
        self.create_manifest()

        # Create README
        self.create_readme()

        print(f"\n✓ Examples ready in: {self.examples_dir}/")
        print(f"\nNext steps:")
        print(f"  1. Review examples: ls -la {self.examples_dir}/")
        print(f"  2. Run one: zebra {self.examples_dir}/01-getting-started/01_hello_world.zbr")
        print(f"  3. Validate all: python3 validate-examples.py")

        return True

def main():
    try:
        extractor = ExampleExtractor(".")
        success = extractor.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Extraction cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
