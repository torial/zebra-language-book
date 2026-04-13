"""Fix // comments → # comments inside ```zebra code blocks.

Does NOT touch:
- shared block structure (shared blocks are a correct language feature)
- Anything outside ```zebra ... ``` blocks
- URLs containing ://
"""
import re
import glob
import os

def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Split by code fences to find zebra blocks
    parts = re.split(r'(```zebra\b.*?\n)', content)

    in_zebra_block = False
    result = []
    for i, part in enumerate(parts):
        if part.startswith('```zebra'):
            in_zebra_block = True
            result.append(part)
            continue

        if in_zebra_block:
            # Find the closing ```
            end_idx = part.find('\n```')
            if end_idx >= 0:
                zebra_code = part[:end_idx]
                rest = part[end_idx:]
                zebra_code = fix_zebra_comments(zebra_code)
                result.append(zebra_code + rest)
                in_zebra_block = False
            else:
                result.append(fix_zebra_comments(part))
        else:
            result.append(part)

    content = ''.join(result)

    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def fix_zebra_comments(code):
    """Convert // comments to # comments in zebra code."""
    lines = code.split('\n')
    fixed = []
    for line in lines:
        if '//' in line and '://' not in line:
            line = fix_comment(line)
        fixed.append(line)
    return '\n'.join(fixed)


def fix_comment(line):
    """Replace // comments with # comments, avoiding // inside strings."""
    in_string = False
    string_char = None
    i = 0
    while i < len(line):
        c = line[i]
        if in_string:
            if c == '\\':
                i += 2
                continue
            if c == string_char:
                in_string = False
        else:
            if c in ('"', "'"):
                in_string = True
                string_char = c
            elif c == '/' and i + 1 < len(line) and line[i + 1] == '/':
                # Found comment start
                return line[:i] + '#' + line[i + 2:]
        i += 1
    return line


if __name__ == '__main__':
    os.chdir(r'c:\projects\zebra-language-book')

    files = sorted(set(
        glob.glob('Part-*/**/*.md', recursive=True) +
        glob.glob('QUICKSTART-30-Minutes.md') +
        glob.glob('CHEATSHEET-Syntax.md') +
        glob.glob('PATTERNS-Common-Tasks.md')
    ))

    changed = 0
    for f in files:
        if fix_file(f):
            print(f'Fixed: {f}')
            changed += 1
    print(f'\n{changed} files changed out of {len(files)}')
