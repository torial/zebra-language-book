#!/usr/bin/env python3
"""
Update markdown image references from .svg to .png
Processes all markdown files in Part directories
"""
import os
import re
from pathlib import Path

def update_file(filepath):
    """Update image references in a markdown file from .svg to .png"""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Replace .svg with .png in image references
    original_count = content.count('.svg')
    updated = content.replace('.svg)', '.png)')

    if original_count > 0:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated)
        return original_count

    return 0

def main():
    # Find all markdown files in Part directories
    part_dirs = [
        'Part-1-Foundations',
        'Part-2-Objects-and-Interfaces',
        'Part-3-Advanced-Features',
        'Part-4-Practical-Projects',
        'Part-5-Ecosystem'
    ]

    total_updated = 0
    files_modified = 0

    for part_dir in part_dirs:
        if not os.path.isdir(part_dir):
            continue

        # Find all .md files in this part
        for md_file in Path(part_dir).glob('*.md'):
            count = update_file(str(md_file))
            if count > 0:
                files_modified += 1
                total_updated += count
                print(f"✓ {md_file}: Updated {count} references")

    print()
    if files_modified > 0:
        print(f"✅ Updated {total_updated} image references in {files_modified} files")
    else:
        print("No image references found to update")

if __name__ == '__main__':
    main()
