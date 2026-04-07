#!/usr/bin/env python3
"""
Strip image references from markdown file to avoid SVG conversion issues.
Replaces ![alt](image.svg) with [IMAGE: alt text]
"""
import sys
import re

def strip_images(input_file, output_file):
    """Replace image syntax with text placeholders."""

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace ![alt](path) with [IMAGE: alt]
    pattern = r'!\[([^\]]*)\]\([^\)]+\)'
    replacement = r'[IMAGE: \1]'
    modified = re.sub(pattern, replacement, content)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(modified)

    # Count how many were replaced
    count = len(re.findall(pattern, content))
    return count

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: strip-images.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    count = strip_images(input_file, output_file)
    print(f"Stripped {count} image references")
    if count > 0:
        print(f"Saved to: {output_file}")
