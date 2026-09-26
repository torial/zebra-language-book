#!/bin/bash
# Zebra Programming Book - PDF Builder (Unix/Mac/Linux)
# Usage: ./build-pdf.sh
# Prerequisites: pandoc (brew install pandoc on Mac, apt-get install pandoc on Linux)

set -e

echo "🔨 Building Zebra Programming Book PDF..."
echo ""

# Check if pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo "❌ Pandoc is not installed."
    echo ""
    echo "Install it:"
    echo "  Mac:    brew install pandoc"
    echo "  Linux:  sudo apt-get install pandoc"
    echo "  Windows: choco install pandoc"
    exit 1
fi

# Create temporary file with all chapters
TEMP_FILE="/tmp/zebra-book-combined.md"
OUTPUT_FILE="zebra-programming-book.pdf"
BOOK_DIR="book"

# Pandoc's --resource-path uses ':' on Unix-y pandoc and ';' on Windows pandoc
# (even when the script runs in Git Bash). Detect once.
case "$(uname -s 2>/dev/null)" in
    MINGW*|MSYS*|CYGWIN*) PATHSEP=';' ;;
    *)                    PATHSEP=':' ;;
esac

echo "📚 Combining chapters..."

# The chapter list is book/SUMMARY.md -- the same list the website is built from --
# written out by book_combine.py. This script used to carry its own hand-written list,
# which had drifted: 07b and 18b were missing from every PDF, and a missing file was
# skipped with a warning instead of failing the build.
PY=$(command -v python3 || command -v python)
[ -n "$PY" ] || { echo "❌ python is required (book_combine.py builds the chapter list)"; exit 1; }
"$PY" book_combine.py "$TEMP_FILE"

echo "📖 Converting to PDF..."
echo "   (This may take a minute...)"
echo ""

# Build PDF with pandoc
pandoc "$TEMP_FILE" \
  --resource-path=".${PATHSEP}$BOOK_DIR${PATHSEP}$BOOK_DIR/Part-1-Foundations${PATHSEP}$BOOK_DIR/Part-2-Objects-and-Interfaces${PATHSEP}$BOOK_DIR/Part-3-Advanced-Features${PATHSEP}$BOOK_DIR/Part-4-Practical-Projects${PATHSEP}$BOOK_DIR/Part-5-Ecosystem" \
  -o "$OUTPUT_FILE" \
  --pdf-engine=xelatex \
  --include-in-header=header.tex \
  --toc \
  --toc-depth=2 \
  --number-sections \
  --syntax-highlighting=zenburn \
  -V geometry:margin=1in \
  -V geometry:top=1in \
  -V geometry:bottom=1in \
  -V fontsize=12pt \
  -V mainfont="Noto Serif" \
  -V sansfont="Noto Sans" \
  -V monofont="DejaVu Sans Mono" \
  -V linestretch=1.5 \
  -V colorlinks=true \
  -V linkcolor=blue \
  --metadata author="Zebra Community" \
  --metadata date="$(date '+%B %d, %Y')" \
  --shift-heading-level-by=0 \
  --top-level-division=chapter

# Check if successful
if [ -f "$OUTPUT_FILE" ]; then
    SIZE=$(du -h "$OUTPUT_FILE" | cut -f1)
    PAGES=$(pdfinfo "$OUTPUT_FILE" 2>/dev/null | grep Pages | awk '{print $2}' || echo "?")
    echo ""
    echo "✅ PDF successfully created!"
    echo "   File: $OUTPUT_FILE"
    echo "   Size: $SIZE"
    echo "   Pages: $PAGES"
    echo ""
    echo "📖 You can now open it:"
    echo "   open $OUTPUT_FILE    (Mac)"
    echo "   xdg-open $OUTPUT_FILE (Linux)"
else
    echo "❌ Failed to create PDF"
    exit 1
fi

# Cleanup
rm -f "$TEMP_FILE"
