#!/usr/bin/env python3
"""
Zebra Programming Book - Code Example Validator

Compiles and validates all extracted examples to ensure correctness.

Usage:
    python3 validate-examples.py

Output:
    validation-report.json (detailed results)
    validation-report.txt (human-readable summary)
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

class ExampleValidator:
    def __init__(self, examples_dir: str = "examples"):
        self.examples_dir = Path(examples_dir)
        self.results = {
            'total': 0,
            'passed': 0,
            'failed': 0,
            'skipped': 0,
            'examples': [],
            'timestamp': datetime.now().isoformat(),
        }

    def find_examples(self) -> List[Path]:
        """Find all .zbr files in examples directory."""
        if not self.examples_dir.exists():
            print(f"✗ Examples directory not found: {self.examples_dir}")
            return []

        examples = list(self.examples_dir.rglob("*.zbr"))
        return sorted(examples)

    def compile_example(self, filepath: Path) -> Tuple[bool, str, str]:
        """Attempt to compile an example with the Zebra compiler."""
        try:
            # Try to compile with zebra compiler
            result = subprocess.run(
                ["zebra", "-c", str(filepath)],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.returncode == 0:
                return True, "Compiled successfully", ""
            else:
                return False, "Compilation failed", result.stderr or result.stdout

        except FileNotFoundError:
            return None, "Compiler not found", "zebra command not in PATH"
        except subprocess.TimeoutExpired:
            return False, "Compilation timeout", "Took longer than 10 seconds"
        except Exception as e:
            return False, "Compilation error", str(e)

    def validate_syntax(self, filepath: Path) -> Tuple[bool, str]:
        """Basic syntax validation without compilation."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check for basic structure
            checks = [
                ("class Main" in content or "class " in content, "Must have at least one class"),
                ("def main" in content or "def " in content, "Must have at least one method"),
                (content.strip(), "File must not be empty"),
            ]

            for check, message in checks:
                if not check:
                    return False, message

            return True, "Syntax OK"

        except Exception as e:
            return False, f"Read error: {e}"

    def validate_example(self, filepath: Path) -> Dict:
        """Validate a single example."""
        relative_path = filepath.relative_to(self.examples_dir)

        result = {
            'file': str(relative_path).replace('\\', '/'),
            'path': str(filepath).replace('\\', '/'),
            'status': 'unknown',
            'message': '',
            'details': '',
        }

        self.results['total'] += 1

        # First: syntax check
        syntax_ok, syntax_msg = self.validate_syntax(filepath)
        if not syntax_ok:
            result['status'] = 'skipped'
            result['message'] = 'Syntax check failed'
            result['details'] = syntax_msg
            self.results['skipped'] += 1
            return result

        # Second: try to compile
        compile_ok, compile_msg, compile_err = self.compile_example(filepath)

        if compile_ok is None:
            # Compiler not available, skip
            result['status'] = 'skipped'
            result['message'] = compile_msg
            result['details'] = compile_err
            self.results['skipped'] += 1

        elif compile_ok:
            result['status'] = 'passed'
            result['message'] = 'Compiled successfully'
            self.results['passed'] += 1

        else:
            result['status'] = 'failed'
            result['message'] = compile_msg
            result['details'] = compile_err[:200]  # Truncate error
            self.results['failed'] += 1

        return result

    def run(self):
        """Run validation on all examples."""
        print("=" * 70)
        print("Zebra Programming Book - Code Example Validator")
        print("=" * 70)
        print()

        # Find examples
        examples = self.find_examples()

        if not examples:
            print(f"✗ No examples found in {self.examples_dir}")
            return False

        print(f"Found {len(examples)} examples\n")
        print("Validating...")
        print()

        # Validate each example
        for i, filepath in enumerate(examples, 1):
            result = self.validate_example(filepath)
            self.results['examples'].append(result)

            # Status indicator
            status_icon = {
                'passed': '✓',
                'failed': '✗',
                'skipped': '⊝',
                'unknown': '?'
            }.get(result['status'], '?')

            # Print progress
            if i % 10 == 0 or i == len(examples):
                print(f"  [{i}/{len(examples)}] {status_icon} {result['file']}")

        # Print summary
        self._print_summary()

        # Save reports
        self._save_reports()

        return self.results['failed'] == 0

    def _print_summary(self):
        """Print validation summary."""
        print()
        print("=" * 70)
        print("VALIDATION SUMMARY")
        print("=" * 70)

        total = self.results['total']
        passed = self.results['passed']
        failed = self.results['failed']
        skipped = self.results['skipped']

        print(f"Total examples:  {total}")
        print(f"✓ Passed:        {passed} ({100*passed//total if total else 0}%)")
        print(f"✗ Failed:        {failed}")
        print(f"⊝ Skipped:       {skipped}")
        print()

        if failed > 0:
            print("FAILED EXAMPLES:")
            for ex in self.results['examples']:
                if ex['status'] == 'failed':
                    print(f"  ✗ {ex['file']}")
                    print(f"    {ex['message']}")
                    if ex['details']:
                        print(f"    {ex['details'][:100]}")

        print()
        if failed == 0:
            print("✓ All examples validated successfully!")
        else:
            print(f"⚠️  {failed} example(s) failed validation")

        print()

    def _save_reports(self):
        """Save validation reports."""
        # JSON report
        json_path = Path("validation-report.json")
        try:
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(self.results, f, indent=2)
            print(f"✓ Saved JSON report: {json_path}")
        except Exception as e:
            print(f"✗ Error saving JSON report: {e}")

        # Text report
        txt_path = Path("validation-report.txt")
        try:
            with open(txt_path, 'w', encoding='utf-8') as f:
                f.write("ZEBRA PROGRAMMING BOOK - EXAMPLE VALIDATION REPORT\n")
                f.write("=" * 70 + "\n\n")
                f.write(f"Generated: {self.results['timestamp']}\n\n")

                f.write("SUMMARY\n")
                f.write("-" * 70 + "\n")
                f.write(f"Total examples:  {self.results['total']}\n")
                f.write(f"Passed:          {self.results['passed']}\n")
                f.write(f"Failed:          {self.results['failed']}\n")
                f.write(f"Skipped:         {self.results['skipped']}\n\n")

                if self.results['failed'] > 0:
                    f.write("FAILED EXAMPLES\n")
                    f.write("-" * 70 + "\n")
                    for ex in self.results['examples']:
                        if ex['status'] == 'failed':
                            f.write(f"\n{ex['file']}\n")
                            f.write(f"  {ex['message']}\n")
                            if ex['details']:
                                f.write(f"  {ex['details']}\n")

                f.write("\n" + "=" * 70 + "\n")
                f.write("END OF REPORT\n")

            print(f"✓ Saved text report: {txt_path}")
        except Exception as e:
            print(f"✗ Error saving text report: {e}")

        print()

def main():
    try:
        validator = ExampleValidator("examples")
        success = validator.run()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Validation cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Fatal error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
