# Building the Zebra Programming Book

This replaces four overlapping build docs (`BUILD_PDF_README.md`,
`BUILD_WITH_PNG_DIAGRAMS.md`, `PDF_BUILD_GUIDE.md`, `README-BOOK-GUIDE.md`) with
one description of what the scripts and `Makefile` actually do.

## The pipeline

```
extract  →  lint          →  html
         →  validate      →  pdf
```

- **`extract`** (`extract-examples.py`) reads every chapter under
  `book/Part-*/*.md`, pulls out ```` ```zebra ```` code blocks, and writes each
  one to `examples/<chapter>/<file>.zbr`. It also writes
  `examples/manifest.json` and `examples/README.md`. `lint`, `validate` and
  `html` all depend on it in the `Makefile`.
- **`lint`** (`lint-chapters.py`) checks the chapters themselves (broken
  links, missing metadata, etc.) and writes `lint-report.txt`.
- **`validate`** (`validate-examples.py`) compiles every extracted `.zbr` file
  with the real Zebra compiler and gates on regression — see
  [Validating examples](#validating-examples-the-baseline) below.
- **`html`** runs `mdbook build`, which renders `book/` (chapter order and
  titles come from `book/SUMMARY.md`, settings from `book.toml`) into
  `public/`. `make serve` (or `mdbook serve --open`) gives a live-reloading
  local preview. GitHub Pages is published from the same build by
  `.github/workflows/pages.yml` on every push to `main`; `public/` is
  git-ignored and never committed.
- **`pdf`** (`build-pdf.sh` / `build-pdf.bat`) combines `book/Part-*/*.md` (in
  a fixed, hardcoded order — see the script if you add or reorder chapters)
  into one file and runs it through pandoc. It reads `book/` chapters
  directly, not the `examples/` output.

Run individual steps or everything:

```bash
make extract
make lint
make validate
make html
make pdf

make all      # extract, lint, validate, html, pdf, in that order
make quick    # extract + validate only — fast sanity check while editing
```

**There is no `make build` target.** If you see that command in older notes,
it should be `make all` or `make quick`.

Other useful targets: `make status` (what tools/dirs are present), `make
verify-scripts` (checks the four Python scripts exist), `make clean` /
`make distclean` (remove generated output), `make help` (full target list).
`make watch` and `make dev` also exist but `watch` requires `fswatch`, which
is not installed by anything here.

## Tools you need

| Tool | Needed for | Notes |
|---|---|---|
| Python 3 | extract, lint, validate | Standard library only — no pip install. |
| mdBook | html | `cargo install mdbook`, or download a prebuilt binary from [mdBook releases](https://github.com/rust-lang/mdBook/releases) and put it on `PATH`. The Pages workflow pins the version in `MDBOOK_VERSION`. |
| Zebra compiler | validate | See [Locating the compiler](#locating-the-compiler). Everything else runs without it. |
| pandoc | pdf | `brew install pandoc` (Mac) / `apt-get install pandoc` (Linux) / `choco install pandoc` (Windows). |
| A LaTeX distribution with `xelatex` | pdf | e.g. `texlive-xetex` on Linux, MiKTeX on Windows. `build-pdf.sh` passes `--pdf-engine=xelatex` unconditionally. |
| Noto Serif, Noto Sans, DejaVu Sans Mono fonts | pdf | `build-pdf.sh` sets these as `-V mainfont`/`-V sansfont`/`-V monofont`. If they're not installed, pandoc/xelatex will substitute or error — install `fonts-noto` and `fonts-dejavu` (Linux) if you hit font errors. |
| Inkscape | optional, Windows-only | Only for `convert-svg-to-png.bat`; see [Diagrams](#diagrams-current-state) below. |

`extract`/`lint` need only Python 3. `html` needs only mdBook. `validate`
additionally needs the compiler. `pdf` additionally needs pandoc + xelatex + those fonts.

## Locating the compiler

`validate-examples.py` looks for the Zebra compiler in this order:

1. the `$ZEBRA` environment variable, if it points at an existing file;
2. `zebra` (or `zebra.exe`) on `$PATH`;
3. a sibling checkout at `../zebra-language/zig-out/bin/zebra.exe` (a
   Windows-suffixed path — this fallback only matches a Windows sibling
   build; on Linux/Mac, set `$ZEBRA` or put `zebra` on `PATH` instead of
   relying on it).

If none of those resolve, `validate-examples.py` exits with an explicit error
rather than silently skipping compilation.

```bash
export ZEBRA=/path/to/zig-out/bin/zebra
python3 validate-examples.py
```

## Validating examples: the baseline

`validate-examples.py` does not require every example to compile — many code
blocks are deliberately non-standalone (a one-line fragment, a "here's the
wrong way" example, one half of a two-file example). Instead it gates on
**regression** against `validation-baseline.txt`, the list of examples that
compiled the last time someone locked it in:

```bash
python3 validate-examples.py                  # compile everything, fail only
                                               # if something in the baseline
                                               # stopped compiling
python3 validate-examples.py --update-baseline  # re-lock the current passing
                                                 # set as the new baseline
```

Run without `--update-baseline` in CI or before a PR; run with it after you've
confirmed a newly-broken example is fixed (or confirmed a newly-passing one is
correct) and want to move the baseline forward. If `validation-baseline.txt`
doesn't exist, the script warns and passes — there's nothing to regress
against yet.

Output: `validation-report.json` and `validation-report.txt` (full pass/fail
detail for every example), plus the baseline file itself when updating.

## Platform notes

- **Mac/Linux:** `bash build-pdf.sh` (or `chmod +x build-pdf.sh && ./build-pdf.sh`).
  Combines chapters, runs pandoc with `xelatex`, cleans up its temp file.
- **Windows:** `build-pdf.bat`. Same combine-and-pandoc flow. It also prints a
  reminder to run the optional PNG conversion step first (see below) — it
  does not run that step for you.
- `extract-examples.py`, `validate-examples.py`, `lint-chapters.py` are plain
  Python and run the same on every platform. `mdbook` ships prebuilt binaries
  for Windows, Mac and Linux.

## Diagrams: current state

Thirteen chapters reference `../diagrams/*.png` images (see `book/diagrams/`;
the `../` is relative to the `book/Part-*/` directory the chapter lives in, and
resolves the same way for mdBook and for pandoc's `--resource-path`).
`book/diagrams/` holds both the SVG sources and the 300-DPI PNGs the
chapters reference (an older note here said none existed; that is no longer
true). If you edit an SVG, the optional Windows-only reconversion path is:

```bash
convert-svg-to-png.bat      REM requires Inkscape (choco install inkscape);
                             REM converts diagrams/*.svg to diagrams/*.png at 300 DPI
python update-image-refs.py REM rewrites chapter .md files from .svg to .png references
```

`build-pdf.bat` does not run these for you — run them first, once, before
building the PDF. There is no Mac/Linux equivalent of `convert-svg-to-png.bat`;
on those platforms you'd invoke Inkscape yourself or use pandoc/LaTeX's native
SVG handling if the diagrams stay as SVG.

## Output

| Path | From |
|---|---|
| `examples/` | `extract` |
| `public/` (git-ignored; `public/index.html` is the entry point) | `html` |
| `zebra-programming-book.pdf` | `pdf` (via `build-pdf.sh`; written to the repo root, not a `build/` subdirectory) |
| `lint-report.txt` | `lint` |
| `validation-report.json`, `validation-report.txt` | `validate` |
