"""Mechanical migration of dead Zebra syntax inside ```zebra blocks.

Migrations applied (only inside ```zebra fenced blocks; prose untouched):

  1. `var X as T`              → `var X: T`
  2. `def F(...) as T`         → `def F(...): T`        (also rewrites params)
  3. `def F(... as T, ...)`    → `def F(...: T, ...)`   (params with no return annot)
  4. `def F as T`              → `def F: T`             (getter / no-paren form)
  5. `cue init(... as T, ...)` → `cue init(...: T, ...)`
  6. `prop X as T`             → `def X: T`             (prop keyword removed 2026-04-19)
  7. `shared` (group block)    → `static`
  8. `shared def F`            → `static def F`
  9. `shared var X`            → `static var X`

Carefully preserved (NOT migrated — these `as` uses are binding clauses):
  - `if X as N`
  - `else if X as N`
  - `if X is T as N`
  - `branch on V as N`
  - Generic-constraint clauses inside `(T where T implements I)` are left alone.

Run from the repo root:
    python fix_modern_syntax.py
"""
import re
import glob
import os
import sys


# Type expression: lowercase primitive, capitalised name, optional (args), optional ?, optional ^
TYPE_RE = r'\^?[A-Za-z_][\w]*(?:\([^)]*\))?\??'

# A single param: `name as Type` → `name: Type` (handles default values too)
def fix_param(match):
    name = match.group(1)
    type_ = match.group(2)
    rest = match.group(3) or ''
    return f'{name}: {type_}{rest}'

PARAM_AS_RE = re.compile(
    r'\b([a-z_]\w*)\s+as\s+(' + TYPE_RE + r')(\s*=\s*[^,)]+|)'
)

# `var NAME as TYPE` (line-leading after optional whitespace)
VAR_AS_RE = re.compile(
    r'(\bvar\s+\w+)\s+as\s+(' + TYPE_RE + r')'
)

# `def NAME(PARAMS) as TYPE` — capture so we can reformat
DEF_RET_RE = re.compile(
    r'(\bdef\s+\w+\s*\([^)]*\))\s+as\s+(' + TYPE_RE + r')'
)

# `def NAME as TYPE` (no parens — getter form)
DEF_GETTER_RE = re.compile(
    r'(\bdef\s+\w+)\s+as\s+(' + TYPE_RE + r')(?=\s|$)'
)

# `prop NAME as TYPE` (legacy keyword — rewrite to `def NAME: TYPE`)
PROP_AS_RE = re.compile(
    r'\bprop\s+(\w+)\s+as\s+(' + TYPE_RE + r')'
)

# `shared` block form (alone on a line, indented)
SHARED_GROUP_RE = re.compile(r'^(\s*)shared\s*$')
# `shared def F` / `shared var X` (inline)
SHARED_INLINE_RE = re.compile(r'(^|\s)shared(\s+(?:def|var|cue)\b)')


def fix_param_block(text):
    """Apply param-level `as` → `:` to a parenthesised parameter list."""
    return PARAM_AS_RE.sub(fix_param, text)


def transform_zebra_line(line):
    """Apply all migrations to a single line inside a zebra code block."""
    # 1. shared keyword (group block form)
    line = SHARED_GROUP_RE.sub(r'\1static', line)
    # 2. shared (inline form)
    line = SHARED_INLINE_RE.sub(r'\1static\2', line)

    # 3. prop NAME as TYPE → def NAME: TYPE
    line = PROP_AS_RE.sub(r'def \1: \2', line)

    # 4. def NAME(PARAMS) as TYPE → def NAME(PARAMS): TYPE  (return annot)
    def def_ret_repl(m):
        head = m.group(1)
        type_ = m.group(2)
        # Also fix params inside the captured `def NAME(PARAMS)` head
        head_fixed = re.sub(
            r'\(([^)]*)\)$',
            lambda mm: '(' + fix_param_block(mm.group(1)) + ')',
            head,
        )
        return f'{head_fixed}: {type_}'
    line = DEF_RET_RE.sub(def_ret_repl, line)

    # 5. def NAME as TYPE (getter, no parens) — guard against re-matching above
    line = DEF_GETTER_RE.sub(r'\1: \2', line)

    # 6. var NAME as TYPE
    line = VAR_AS_RE.sub(r'\1: \2', line)

    # 7. Remaining param `NAME as TYPE` inside any `(...)` — covers
    #    void-return def, cue init, and lambda forms not caught above.
    line = re.sub(
        r'\(([^)]*\bas\b[^)]*)\)',
        lambda mm: '(' + fix_param_block(mm.group(1)) + ')',
        line,
    )

    return line


def fix_zebra_block(block_text):
    """Apply line-by-line transforms inside a zebra code block body."""
    lines = block_text.split('\n')
    return '\n'.join(transform_zebra_line(ln) for ln in lines)


# Match a zebra fenced block: ```zebra ... ```
ZEBRA_BLOCK_RE = re.compile(
    r'(```zebra\b[^\n]*\n)(.*?)(\n```)',
    re.DOTALL,
)


def fix_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    content = ZEBRA_BLOCK_RE.sub(
        lambda m: m.group(1) + fix_zebra_block(m.group(2)) + m.group(3),
        content,
    )

    if content != original:
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(content)
        return True
    return False


def main():
    root = os.path.dirname(os.path.abspath(__file__))
    md_files = []
    for pattern in ('*.md', 'Part-*/*.md', 'Appendices/*.md'):
        md_files.extend(glob.glob(os.path.join(root, pattern)))

    changed = []
    for path in sorted(md_files):
        try:
            if fix_file(path):
                changed.append(os.path.relpath(path, root))
        except Exception as e:
            print(f'ERROR on {path}: {e}', file=sys.stderr)

    if changed:
        print(f'Modified {len(changed)} files:')
        for p in changed:
            print(f'  {p}')
    else:
        print('No changes (already migrated or no matches).')


if __name__ == '__main__':
    main()
