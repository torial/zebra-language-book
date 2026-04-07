# Zebra Book PDF Build Guide

## Prerequisites

1. **Pandoc** — Markdown to PDF converter
   ```bash
   choco install pandoc
   ```

2. **MiKTeX** — LaTeX distribution for PDF generation
   ```bash
   choco install miktex
   ```

3. **Python 3** — For diagram path fixing
   - Already installed on most systems
   - Check: `python --version`

## Environment Setup (One-Time)

Set global environment variables so the build script can find files:

**Option 1: Automatic (Recommended)**
```bash
Right-click C:\Projects\cobra-language\setup-env.bat → "Run as Administrator"
```

**Option 2: Manual**
- Windows Key + X → System
- Advanced system settings → Environment Variables
- Add these User variables:
  - `ZEBRA_PROJECT` = `C:\Projects\cobra-language`
  - `ZEBRA_BOOK` = `C:\Projects\cobra-language\zebra-book`
  - `ZEBRA_DIAGRAMS` = `C:\Projects\cobra-language\zebra-book\diagrams`

Then **restart your terminal**.

## Building the PDF

Navigate to the book directory:
```bash
cd C:\Projects\cobra-language\zebra-book
```

Double-click **`build-pdf.bat`** or run:
```bash
build-pdf.bat
```

The script will:
1. ✅ Combine all chapters into a single markdown file
2. ✅ Fix relative diagram paths (`../diagrams/`) to absolute paths
3. ✅ Convert to PDF using Pandoc + MiKTeX
4. ✅ Open the PDF automatically

**Output:** `zebra-programming-book.pdf`

## How the Fix Works

### The Problem
Diagram references in markdown use relative paths:
```markdown
![Type Hierarchy](../diagrams/01-type-hierarchy.svg)
```

When Pandoc runs from a temp directory, `../diagrams/` doesn't resolve correctly.

### The Solution
Before PDF generation, `fix-diagram-paths.py` converts relative paths to absolute:

**Before:**
```markdown
![Type Hierarchy](../diagrams/01-type-hierarchy.svg)
```

**After:**
```markdown
![Type Hierarchy](C:\Projects\cobra-language\zebra-book\diagrams/01-type-hierarchy.svg)
```

Then Pandoc can reliably find all diagram files.

## What if It Fails?

### "Pandoc not found"
```bash
choco install pandoc
```

### "xelatex not found"
```bash
choco install miktex
```

### "Could not fetch resource diagrams/..."
- Verify environment variables are set: `echo %ZEBRA_DIAGRAMS%`
- Check diagrams folder exists: `dir C:\Projects\cobra-language\zebra-book\diagrams`
- Try running build script from `zebra-book` directory (not parent)

### "fix-diagram-paths.py not found"
- Verify you're in the correct directory: `cd C:\Projects\cobra-language\zebra-book`
- The script should be in the same directory as `build-pdf.bat`

## Advanced: Manual Build

If the batch script has issues, you can build manually:

```bash
REM 1. Combine chapters (batch file does this)
REM 2. Fix paths
python fix-diagram-paths.py combined.md combined-fixed.md "C:\Projects\cobra-language\zebra-book\diagrams"

REM 3. Convert to PDF
pandoc combined-fixed.md ^
  -o zebra-programming-book.pdf ^
  --pdf-engine=xelatex ^
  --toc ^
  --number-sections ^
  --syntax-highlighting=zenburn
```

## File Structure

```
zebra-book/
├── build-pdf.bat                 ← Run this
├── fix-diagram-paths.py          ← Called by build-pdf.bat
├── PDF_BUILD_GUIDE.md            ← This file
├── Part-1-Foundations/
│   ├── 01-Getting-Started.md
│   ├── 02-Values-and-Types.md    (references ../diagrams/)
│   └── ...
├── Part-2-Objects-and-Interfaces/
│   └── ...
├── Part-3-Advanced-Features/
│   └── ...
├── Part-4-Practical-Projects/
│   └── ...
├── Part-5-Ecosystem/
│   └── ...
├── diagrams/
│   ├── 01-type-hierarchy.svg
│   ├── 02-collections-comparison.svg
│   └── ... (13 SVG files)
└── zebra-programming-book.pdf    ← Output
```

## Troubleshooting Checklist

- [ ] Pandoc installed: `pandoc --version`
- [ ] MiKTeX installed: `xelatex --version`
- [ ] Environment variables set: `echo %ZEBRA_PROJECT%`
- [ ] In correct directory: `cd C:\Projects\cobra-language\zebra-book`
- [ ] Diagrams folder exists: `dir diagrams\`
- [ ] `fix-diagram-paths.py` exists in current directory
- [ ] Python installed: `python --version`

## References

- [Pandoc Documentation](https://pandoc.org/)
- [MiKTeX Installation Guide](https://miktex.org/)
- [Environment Variables (Windows)](https://docs.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_environment_variables)
