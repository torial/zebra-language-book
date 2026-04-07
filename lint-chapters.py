#!/usr/bin/env python3
"""
Zebra Programming Book - Chapter Linter

Checks all chapters for:
- Correct code block formatting
- Broken links and references
- Consistent terminology
- Missing or incorrect metadata
- Diagram references

Usage:
    python3 lint-chapters.py

Output:
    lint-report.txt (detailed findings)
"""

import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict

class ChapterLinter:
    def __init__(self, book_root: str = "."):
        self.book_root = Path(book_root)
        self.issues = defaultdict(list)
        self.stats = {
            'files': 0,
            'chapters': 0,
            'code_blocks': 0,
            'links': 0,
            'diagrams': 0,
            'warnings': 0,
            'errors': 0,
        }

    def find_chapters(self) -> List[Path]:
        """Find all markdown chapter files."""
        chapters = []
        for part_dir in sorted(self.book_root.glob("Part-*")):
            if not part_dir.is_dir():
                continue
            chapters.extend(sorted(part_dir.glob("*.md")))
        return chapters

    def lint_chapter(self, filepath: Path):
        """Lint a single chapter file."""
        self.stats['files'] += 1

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

        except Exception as e:
            self._add_issue(filepath, f"Read error: {e}", 'error')
            return

        relative_path = filepath.relative_to(self.book_root)
        self.stats['chapters'] += 1

        # Check: Chapter header
        self._check_chapter_header(filepath, relative_path, lines)

        # Check: Code blocks
        self._check_code_blocks(filepath, relative_path, content)

        # Check: Diagram references
        self._check_diagram_references(filepath, relative_path, content)

        # Check: Links and references
        self._check_links(filepath, relative_path, content)

        # Check: Consistency
        self._check_consistency(filepath, relative_path, content)

    def _check_chapter_header(self, filepath: Path, relative_path: Path, lines: List[str]):
        """Check for proper chapter header."""
        if not lines[0].startswith('# '):
            self._add_issue(filepath, "Chapter should start with '# Title'", 'error')
            return

        # Check for metadata section after header
        has_metadata = False
        for line in lines[1:10]:
            if line.startswith('**Audience:**') or line.startswith('**Time:**'):
                has_metadata = True
                break

        if not has_metadata:
            self._add_issue(filepath, "Missing metadata section (Audience, Time, Prerequisites)", 'warning')

    def _check_code_blocks(self, filepath: Path, relative_path: Path, content: str):
        """Check code block formatting and metadata."""
        # Find all code blocks
        pattern = r'```zebra\n(.*?)```'
        blocks = list(re.finditer(pattern, content, re.DOTALL))
        self.stats['code_blocks'] += len(blocks)

        for i, match in enumerate(blocks):
            code = match.group(1)
            has_file_tag = '// file:' in code
            has_teaches_tag = '// teaches:' in code
            has_chapter_tag = '// chapter:' in code

            # Check for required metadata
            if not has_file_tag:
                self._add_issue(
                    filepath,
                    f"Code block #{i+1} missing '// file:' tag",
                    'warning'
                )

            if not has_teaches_tag:
                self._add_issue(
                    filepath,
                    f"Code block #{i+1} missing '// teaches:' tag",
                    'warning'
                )

            if not has_chapter_tag:
                self._add_issue(
                    filepath,
                    f"Code block #{i+1} missing '// chapter:' tag",
                    'warning'
                )

            # Validate chapter tag matches filename
            if has_chapter_tag:
                match_chapter = re.search(r'// chapter: (.+)', code)
                if match_chapter:
                    chapter_tag = match_chapter.group(1).strip()
                    expected = relative_path.stem
                    if chapter_tag != expected:
                        self._add_issue(
                            filepath,
                            f"Code block #{i+1} chapter tag '{chapter_tag}' doesn't match file '{expected}'",
                            'warning'
                        )

    def _check_diagram_references(self, filepath: Path, relative_path: Path, content: str):
        """Check that referenced diagrams exist."""
        # Find all diagram references: ![...](../diagrams/...)
        pattern = r'!\[.*?\]\((.*?diagrams/.*?\.svg)\)'
        references = re.findall(pattern, content)
        self.stats['diagrams'] += len(references)

        diagrams_dir = self.book_root / "diagrams"

        for ref in references:
            # Normalize path
            if ref.startswith('../'):
                diagram_path = self.book_root / ref
            else:
                diagram_path = self.book_root / ref

            if not diagram_path.exists():
                self._add_issue(
                    filepath,
                    f"Diagram not found: {ref}",
                    'error'
                )

    def _check_links(self, filepath: Path, relative_path: Path, content: str):
        """Check internal links and references."""
        # Find all links: [text](...)
        pattern = r'\[.*?\]\((.*?)\)'
        links = re.findall(pattern, content)
        self.stats['links'] += len(links)

        for link in links:
            # Skip external links and anchors
            if link.startswith('http') or link.startswith('#'):
                continue

            # Check for relative links
            if '.md' in link:
                # Extract file path (before any #anchor)
                file_path = link.split('#')[0]

                # Resolve relative path
                if file_path.startswith('../'):
                    target = self.book_root / file_path
                else:
                    target = filepath.parent / file_path

                if file_path and not target.exists():
                    self._add_issue(
                        filepath,
                        f"Broken link: {link}",
                        'warning'
                    )

    def _check_consistency(self, filepath: Path, relative_path: Path, content: str):
        """Check for consistency in terminology and formatting."""
        issues = []

        # Check for common inconsistencies
        checks = [
            (r'zebra', 'Zebra', "Language name should be capitalized"),
            (r'nilable', 'nullable', "Should use 'nullable' not 'nilable'"),
            (r'Result Type', 'Result(T, E)', "Should use Result(T, E) notation"),
        ]

        for pattern, expected, message in checks:
            if re.search(pattern, content, re.IGNORECASE):
                if not re.search(expected, content):
                    self._add_issue(filepath, message, 'info')

        # Check for common formatting issues
        if '```' in content and '```zebra' not in content:
            # Has code blocks but not Zebra code blocks
            self._add_issue(filepath, "Code blocks should use ```zebra syntax", 'warning')

    def _add_issue(self, filepath: Path, message: str, level: str = 'warning'):
        """Record an issue."""
        relative_path = filepath.relative_to(self.book_root)
        self.issues[relative_path].append({
            'message': message,
            'level': level,
        })

        if level == 'error':
            self.stats['errors'] += 1
        elif level == 'warning':
            self.stats['warnings'] += 1

    def run(self):
        """Run linter on all chapters."""
        print("=" * 70)
        print("Zebra Programming Book - Chapter Linter")
        print("=" * 70)
        print()

        chapters = self.find_chapters()

        if not chapters:
            print("✗ No chapters found!")
            return False

        print(f"Linting {len(chapters)} chapters...\n")

        for i, chapter in enumerate(chapters, 1):
            print(f"[{i}/{len(chapters)}] {chapter.relative_to(self.book_root)}")
            self.lint_chapter(chapter)

        # Print summary
        self._print_summary()

        # Save report
        self._save_report()

        return self.stats['errors'] == 0

    def _print_summary(self):
        """Print linting summary."""
        print()
        print("=" * 70)
        print("LINTING SUMMARY")
        print("=" * 70)
        print()

        print(f"Files scanned:     {self.stats['files']}")
        print(f"Chapters:          {self.stats['chapters']}")
        print(f"Code blocks:       {self.stats['code_blocks']}")
        print(f"Diagram refs:      {self.stats['diagrams']}")
        print(f"Link checks:       {self.stats['links']}")
        print()

        print(f"Errors:            {self.stats['errors']}")
        print(f"Warnings:          {self.stats['warnings']}")
        print()

        # Show issues by file
        if self.issues:
            print("ISSUES BY FILE:")
            print("-" * 70)

            for filepath in sorted(self.issues.keys()):
                file_issues = self.issues[filepath]
                errors = [i for i in file_issues if i['level'] == 'error']
                warnings = [i for i in file_issues if i['level'] == 'warning']

                print(f"\n{filepath}")
                if errors:
                    for issue in errors:
                        print(f"  ✗ ERROR: {issue['message']}")
                if warnings:
                    for issue in warnings:
                        print(f"  ⚠️  WARNING: {issue['message']}")

        print()

        if self.stats['errors'] == 0:
            print("✓ No errors found!")
        else:
            print(f"⚠️  {self.stats['errors']} error(s) to fix")

    def _save_report(self):
        """Save linting report to file."""
        report_path = Path("lint-report.txt")

        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write("ZEBRA PROGRAMMING BOOK - LINTING REPORT\n")
                f.write("=" * 70 + "\n\n")

                f.write("STATISTICS\n")
                f.write("-" * 70 + "\n")
                f.write(f"Files scanned:     {self.stats['files']}\n")
                f.write(f"Chapters:          {self.stats['chapters']}\n")
                f.write(f"Code blocks:       {self.stats['code_blocks']}\n")
                f.write(f"Diagram refs:      {self.stats['diagrams']}\n")
                f.write(f"Link checks:       {self.stats['links']}\n")
                f.write(f"Errors:            {self.stats['errors']}\n")
                f.write(f"Warnings:          {self.stats['warnings']}\n\n")

                if self.issues:
                    f.write("ISSUES\n")
                    f.write("-" * 70 + "\n\n")

                    for filepath in sorted(self.issues.keys()):
                        f.write(f"{filepath}\n")
                        for issue in self.issues[filepath]:
                            prefix = "✗" if issue['level'] == 'error' else "⚠️"
                            f.write(f"  {prefix} {issue['level'].upper()}: {issue['message']}\n")
                        f.write("\n")

                f.write("=" * 70 + "\n")
                f.write("END OF REPORT\n")

            print(f"✓ Saved report: {report_path}")

        except Exception as e:
            print(f"✗ Error saving report: {e}")

def main():
    try:
        linter = ChapterLinter(".")
        success = linter.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Linting cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
