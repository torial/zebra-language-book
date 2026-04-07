#!/usr/bin/env python3
"""
Fix diagram paths in markdown files for PDF generation.
Converts relative paths (../diagrams/) to absolute paths.
"""
import sys
import os
from pathlib import Path

def fix_diagram_paths(input_file, output_file, zebra_diagrams_path):
    """Replace relative diagram paths with absolute paths."""

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace ../diagrams/ with absolute path
    # Normalize path separators to forward slashes for Pandoc
    original_count = content.count('../diagrams/')
    normalized_path = zebra_diagrams_path.replace('\\', '/')
    content = content.replace('../diagrams/', normalized_path + '/')

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)

    return original_count

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: fix-diagram-paths.py <input_file> <output_file> <zebra_diagrams_path>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]
    zebra_diagrams_path = sys.argv[3]

    if not os.path.exists(input_file):
        print(f"Error: Input file not found: {input_file}", file=sys.stderr)
        sys.exit(1)

    count = fix_diagram_paths(input_file, output_file, zebra_diagrams_path)
    print(f"Fixed {count} diagram path references")
    if count > 0:
        print(f"Saved to: {output_file}")
