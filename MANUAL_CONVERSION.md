# Manual SVG to PNG Conversion

If you want to convert SVGs and update markdown **before** building the PDF, use these scripts.

## Step 1: Convert SVG Diagrams to PNG

**Option A: Batch script (recommended)**
```bash
cd C:\Projects\cobra-language\zebra-book
convert-svg-to-png.bat
```

**Option B: Manual Inkscape commands**
```bash
cd diagrams
for %f in (*.svg) do inkscape "%f" --export-type=png --export-dpi=300 --export-filename="%~nf.png"
cd ..
```

**What it does:**
- Converts all `.svg` files in `diagrams/` to `.png` at 300 DPI
- Keeps original SVG files intact
- Creates high-quality raster images suitable for PDF embedding

**Result:**
```
diagrams/
├── 01-type-hierarchy.svg
├── 01-type-hierarchy.png         ← NEW
├── 02-collections-comparison.svg
├── 02-collections-comparison.png ← NEW
└── ... (13 SVG + 13 PNG pairs)
```

## Step 2: Update Markdown Image References

**Run the Python script:**
```bash
cd C:\Projects\cobra-language\zebra-book
python update-image-refs.py
```

**What it does:**
- Scans all markdown files in `Part-*` directories
- Changes `![alt](../diagrams/foo.svg)` to `![alt](../diagrams/foo.png)`
- Saves updated markdown files

**Example change:**
```markdown
# Before
![Type Hierarchy Diagram](../diagrams/01-type-hierarchy.svg)

# After
![Type Hierarchy Diagram](../diagrams/01-type-hierarchy.png)
```

**Output:**
```
✓ Part-1-Foundations/02-Values-and-Types.md: Updated 1 references
✓ Part-1-Foundations/03-Collections.md: Updated 1 references
✓ Part-1-Foundations/04-Functions-and-Scope.md: Updated 1 references
... (all chapters updated)
✅ Updated 13 image references in 13 files
```

## Step 3: Build PDF

Once conversion and markdown updates are complete:

```bash
build-pdf.bat
```

The batch file will:
- Detect that PNGs already exist (skips conversion)
- Combine chapters
- Fix image paths for Pandoc
- Generate PDF with embedded PNG diagrams

## Troubleshooting

### "convert-svg-to-png.bat doesn't run"
- Make sure you're in the `zebra-book` directory
- Verify Inkscape is installed: `where inkscape`

### "Python script fails"
- Make sure you're in the `zebra-book` directory
- Verify Python is installed: `python --version`
- Check that `Part-*` directories exist

### "I want to revert the markdown changes"
Use Git to restore original markdown:
```bash
git checkout Part-*/\*.md
```

Then re-run `python update-image-refs.py` after converting SVGs again.

## Manual Steps Reference

If you prefer to do everything manually:

```bash
REM 1. Convert one SVG to PNG
inkscape diagrams\01-type-hierarchy.svg --export-type=png --export-dpi=300 --export-filename=diagrams\01-type-hierarchy.png

REM 2. Update one markdown file
REM (Edit with text editor: change .svg to .png in image references)

REM 3. Build PDF
pandoc combined.md -o output.pdf --pdf-engine=pdflatex
```
