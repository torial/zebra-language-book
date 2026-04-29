# Building the Zebra Programming Book PDF

This directory contains scripts to automatically generate a professional PDF from the Zebra Programming Book markdown source.

## Quick Start

### Windows
1. Install Pandoc (one-time setup)
2. Double-click `build-pdf.bat`
3. PDF opens automatically in your default reader

### Mac/Linux
1. Install Pandoc (one-time setup)
2. Run `./build-pdf.sh` in terminal
3. PDF opens automatically

---

## Installation Prerequisites

### Windows

**Option 1: Chocolatey (Recommended)**
```powershell
choco install pandoc
```

**Option 2: Direct Download**
- Visit https://pandoc.org/installing.html
- Download the Windows installer
- Run installer and follow prompts

**Option 3: Scoop**
```powershell
scoop install pandoc
```

### Mac

```bash
brew install pandoc
```

### Linux (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install pandoc
```

### Linux (Fedora/RedHat)

```bash
sudo dnf install pandoc
```

---

## Usage

### Windows: `build-pdf.bat`

```bash
# Simply double-click the file, or run in Command Prompt:
build-pdf.bat

# Or from PowerShell:
.\build-pdf.bat
```

**Features:**
- ✅ Validates Pandoc is installed
- ✅ Combines all chapters in correct order
- ✅ Checks for each chapter file
- ✅ Automatically opens PDF when done
- ✅ Shows file size and page count
- ✅ Cleans up temporary files

### Mac/Linux: `build-pdf.sh`

```bash
# Make executable (first time only):
chmod +x build-pdf.sh

# Run the script:
./build-pdf.sh

# Or:
bash build-pdf.sh
```

**Features:**
- ✅ Same as Windows version
- ✅ Uses xelatex for high-quality PDF
- ✅ Cleans up temp files automatically
- ✅ Shows completion status

---

## Output

Both scripts generate: **`zebra-programming-book.pdf`**

### PDF Features
- **Table of Contents** — Auto-generated with links
- **Chapter Numbering** — Chapters and sections numbered
- **Code Highlighting** — Syntax highlighting for Zebra code
- **Embedded Diagrams** — All 13 SVG diagrams included
- **Page Breaks** — Proper formatting between chapters
- **Metadata** — Author, title, date included
- **Professional Typography** — Proper fonts and spacing
- **Hyperlinks** — Clickable links in table of contents

### File Info
- **Format:** PDF (portable, viewable on any device)
- **Size:** ~50-70 MB (depends on images/diagrams)
- **Pages:** ~120+ pages (depending on content)
- **Quality:** Print-ready (300 DPI equivalent)

---

## What Gets Included

The PDF includes all chapters in this order:

### Part 1: Foundations (Chapters 01-06)
- Getting Started
- Values and Types
- Collections
- Functions and Scope
- Control Flow
- Strings and Unicode

### Part 2: Objects & Interfaces (Chapters 07-10)
- Classes and Instances
- Interfaces and Protocols
- Composition and Mixins
- Properties and Computed Values

### Part 3: Advanced Features (Chapters 11-15)
- Nil Tracking and Safety
- Error Handling with Results
- Generics and Type Constraints
- Contracts and Assertions
- Pipelines and Function Composition

### Part 4: Practical Projects (Chapters 16-18)
- Project 1: CLI Tool
- Project 2: HTTP Server
- Project 3: Text Data Analysis

### Part 5: Ecosystem (Chapters 19-22)
- Standard Library Tour
- File I/O and System Access
- Regular Expressions
- FFI and Interop

---

## Customization

### Change Output Filename

**Windows (`build-pdf.bat`):**
Edit this line:
```batch
set OUTPUT_FILE=my-custom-name.pdf
```

**Mac/Linux (`build-pdf.sh`):**
Edit this line:
```bash
OUTPUT_FILE="my-custom-name.pdf"
```

### Adjust PDF Styling

Open the script and modify these settings:

```
-V fontsize=11pt          # Change text size (10, 12, 14, etc.)
-V geometry:margin=1in    # Change page margins
-V mainfont="Calibri"     # Change main font (Helvetica, Times, etc.)
-V monofont="Monaco"      # Change code font
-V linestretch=1.5        # Change line spacing (1.0-2.0)
```

### Skip Chapters

If you want to skip certain chapters, comment them out in the script:

**Windows (batch):**
```batch
REM if exist "Part-1-Foundations\01-Getting-Started.md" (
REM     type "Part-1-Foundations\01-Getting-Started.md" >> "%TEMP_FILE%"
REM )
```

**Mac/Linux (bash):**
```bash
# cat Part-1-Foundations/01-Getting-Started.md >> "$TEMP_FILE"
```

---

## Troubleshooting

### ❌ "Pandoc is not installed"

**Solution:** Install pandoc following the installation steps above.

### ❌ PDF file not created

**Check:**
1. Do you have write permissions in the directory?
2. Is the output filename valid (no special characters)?
3. Run script again and check error messages

**Windows:** Run Command Prompt as Administrator
**Mac/Linux:** Check file permissions: `ls -la build-pdf.sh`

### ❌ SVG diagrams don't appear

**Possible causes:**
- Diagram files missing or wrong path
- Check that `diagrams/` folder exists with `.svg` files

**Solution:**
- Verify diagram paths in markdown files
- Use absolute paths if relative paths fail

### ❌ Fonts look wrong

**Solution:**
- Different systems may substitute fonts
- Edit the script to use system-available fonts
- Common options: Helvetica, Times, Courier, Arial

### ⚠️ PDF is very large

**If PDF > 100 MB:**
- Reduce image quality: change `--dpi=300` to `--dpi=150`
- Remove diagrams (edit markdown files)
- Use compression: `pdflatex` instead of `xelatex` (but may lose quality)

---

## Advanced Options

### Command Line Usage

**Windows (PowerShell):**
```powershell
& ".\build-pdf.bat"
```

**Mac/Linux (Terminal):**
```bash
./build-pdf.sh
./build-pdf.sh > build.log  # Save output to log
```

### Manual Pandoc Command

If you want to run pandoc directly:

```bash
pandoc *.md \
  -o zebra-book.pdf \
  --toc \
  --number-sections \
  --pdf-engine=xelatex \
  -V fontsize=11pt \
  -V geometry:margin=1in
```

### Create Multiple Formats

**HTML version (for web):**
```bash
pandoc *.md -o zebra-book.html --toc
```

**EPUB version (for e-readers):**
```bash
pandoc *.md -o zebra-book.epub --toc
```

**DOCX version (for editing):**
```bash
pandoc *.md -o zebra-book.docx --toc
```

---

## System Requirements

| Requirement | Version | Notes |
|-------------|---------|-------|
| Pandoc | 2.0+ | https://pandoc.org |
| LaTeX | Modern | Usually auto-installed with pandoc |
| Disk Space | ~100 MB | For temp files and output |
| RAM | 2+ GB | Recommended for large documents |

---

## Performance

| Operation | Time |
|-----------|------|
| Combine chapters | < 1 second |
| Convert to PDF | 30-60 seconds |
| Open PDF | < 5 seconds |
| **Total** | **~1 minute** |

---

## Support

### Common Questions

**Q: Can I edit the PDF?**
A: Most PDF readers allow annotation. For editing text, regenerate from markdown.

**Q: Can I generate just one chapter?**
A: Modify the script to include only that chapter's markdown file.

**Q: What if chapters are added/removed?**
A: Edit the script to add/remove corresponding lines.

**Q: Can I use different page sizes?**
A: Yes, add `-V papersize=a5` for smaller pages, `b5`, etc.

---

## License

These build scripts are provided as part of the Zebra Programming Book.

---

**Last Updated:** April 7, 2026  
**Status:** Ready for production use  
**Platforms:** Windows, Mac, Linux
