# Building PDF with PNG Diagrams

## Overview

The updated build process now:
1. **Converts SVG diagrams to PNG** (300 DPI) using Inkscape
2. **Updates markdown files** to reference `.png` instead of `.svg`
3. **Combines chapters** and fixes image paths
4. **Generates PDF** with Pandoc

## Prerequisites

- **Pandoc** — Markdown to PDF converter
- **MiKTeX** — LaTeX distribution
- **Inkscape** — SVG to PNG conversion
- **Python 3** — Script automation

### Install Prerequisites

```bash
choco install pandoc miktex inkscape python
```

## Building the PDF

### One-Time Setup (Optional)
```bash
REM Set environment variables
setup-env.bat
```

### Build the PDF

```bash
cd C:\Projects\cobra-language\zebra-book
build-pdf.bat
```

**First Run:** Will convert all SVGs to PNGs and update markdown (takes 1-2 minutes)  
**Subsequent Runs:** Skips conversion since PNGs already exist (takes 30 seconds)

## What Happens

### Step 1: SVG → PNG Conversion
```
Converting SVG diagrams to PNG (300 DPI)...
  - 01-type-hierarchy.svg...
  - 02-collections-comparison.svg...
  ... (13 total)
```

Creates `diagrams/*.png` files at 300 DPI (print quality)

### Step 2: Update Markdown References
```
Updating markdown image references from .svg to .png...
✓ Part-1-Foundations/02-Values-and-Types.md: Updated 1 references
✓ Part-1-Foundations/03-Collections.md: Updated 1 references
... (13 total)
```

Changes all markdown files from `![alt](../diagrams/foo.svg)` to `![alt](../diagrams/foo.png)`

### Step 3: Combine and Build PDF
```
Combining chapters...
📖 Converting to PDF...
✅ PDF successfully created!
   File: zebra-programming-book.pdf
```

Opens the PDF automatically

## Files Involved

| File | Purpose |
|------|---------|
| `build-pdf.bat` | Main build script (updated with PNG conversion) |
| `convert-svg-to-png.bat` | Standalone SVG to PNG converter (optional, called by build-pdf.bat) |
| `update-image-refs.py` | Updates markdown to reference .png files |
| `fix-diagram-paths.py` | Converts relative paths to absolute (existing) |
| `diagrams/*.svg` | Original vector diagrams (unchanged) |
| `diagrams/*.png` | Generated raster diagrams (300 DPI) |
| `Part-*/*.md` | Updated to reference .png files |

## Troubleshooting

### "Inkscape is not in PATH"
- Run: `choco install inkscape`
- Restart your terminal
- Try again

### "PNG conversion fails"
- Verify Inkscape installed: `where inkscape`
- Try manual conversion: `convert-svg-to-png.bat`
- Check that `diagrams/` folder exists with `.svg` files

### "PDF still has errors"
- Delete all `diagrams/*.png` files to force reconversion
- Run `build-pdf.bat` again

### "I want to revert to SVG references"
- The original markdown files are backed up in Git
- Run: `git checkout Part-*/\*.md`
- Or manually change `.png)` back to `.svg)` in markdown files

## Manual Conversion (if needed)

To convert SVGs to PNGs manually:

```bash
REM Navigate to book directory
cd C:\Projects\cobra-language\zebra-book

REM Run the converter
convert-svg-to-png.bat

REM Update markdown references
python update-image-refs.py
```

## Output Quality

- **DPI:** 300 (print quality)
- **Format:** PNG (lossless)
- **Size:** Approximately 500KB-1MB total
- **Display:** Sharp in PDF viewer, scales to page width

## Advantages of PNG Approach

✅ **Works reliably** — No rsvg-convert dependency issues  
✅ **High quality** — 300 DPI is excellent for printing  
✅ **Universal** — Works with any PDF engine (pdflatex, xelatex, wkhtmltopdf)  
✅ **One-time cost** — Conversion only runs once  
✅ **Reversible** — Can regenerate from original SVGs anytime  

## Next Steps

If you want to enhance the output later:
- Add SVG → PDF conversion as alternative (better scalability)
- Generate both PNG and PDF versions
- Use a web-based build system (WeasyPrint, wkhtmltopdf)
- Create an automated CI/CD pipeline
