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

echo "📚 Combining chapters..."

# Clear temp file
> "$TEMP_FILE"

# Add title page
cat >> "$TEMP_FILE" << 'EOF'
---
title: The Zebra Programming Language
subtitle: A Modern Language with Safety and Performance
author: Zebra Community
date: April 2026
lang: en
toc: true
toc-depth: 2
number-sections: true
---

EOF

# Part 1: Foundations
echo "  Part 1: Foundations..."
cat >> "$TEMP_FILE" << 'EOF'
# Part 1: Foundations

EOF
cat Part-1-Foundations/01-Getting-Started.md >> "$TEMP_FILE" 2>/dev/null || echo "⚠️  Skipping 01-Getting-Started.md"
echo "" >> "$TEMP_FILE"
cat Part-1-Foundations/02-Values-and-Types.md >> "$TEMP_FILE" 2>/dev/null || echo "⚠️  Skipping 02-Values-and-Types.md"
echo "" >> "$TEMP_FILE"
cat Part-1-Foundations/03-Collections.md >> "$TEMP_FILE" 2>/dev/null || echo "⚠️  Skipping 03-Collections.md"
echo "" >> "$TEMP_FILE"
cat Part-1-Foundations/04-Functions-and-Scope.md >> "$TEMP_FILE" 2>/dev/null || echo "⚠️  Skipping 04-Functions-and-Scope.md"
echo "" >> "$TEMP_FILE"
cat Part-1-Foundations/05-Control-Flow.md >> "$TEMP_FILE" 2>/dev/null || echo "⚠️  Skipping 05-Control-Flow.md"
echo "" >> "$TEMP_FILE"
cat Part-1-Foundations/06-Strings-and-Unicode.md >> "$TEMP_FILE" 2>/dev/null || echo "⚠️  Skipping 06-Strings-and-Unicode.md"

# Part 2: Objects & Interfaces
echo "  Part 2: Objects & Interfaces..."
cat >> "$TEMP_FILE" << 'EOF'

# Part 2: Objects and Interfaces

EOF
cat Part-2-Objects-and-Interfaces/07-Classes-and-Instances.md >> "$TEMP_FILE" 2>/dev/null || echo "⚠️  Skipping 07-Classes-and-Instances.md"
echo "" >> "$TEMP_FILE"
cat Part-2-Objects-and-Interfaces/08-Interfaces-and-Protocols.md >> "$TEMP_FILE" 2>/dev/null || echo "⚠️  Skipping 08-Interfaces-and-Protocols.md"
echo "" >> "$TEMP_FILE"
cat Part-2-Objects-and-Interfaces/09-Inheritance-and-Mixins.md >> "$TEMP_FILE" 2>/dev/null || echo "⚠️  Skipping 09-Inheritance-and-Mixins.md"
echo "" >> "$TEMP_FILE"
cat Part-2-Objects-and-Interfaces/10-Properties-and-Computed-Values.md >> "$TEMP_FILE" 2>/dev/null || echo "⚠️  Skipping 10-Properties-and-Computed-Values.md"

# Part 3: Advanced Features
echo "  Part 3: Advanced Features..."
cat >> "$TEMP_FILE" << 'EOF'

# Part 3: Advanced Features

EOF
cat Part-3-Advanced-Features/11-Nil-Tracking-and-Safety.md >> "$TEMP_FILE" 2>/dev/null || echo "⚠️  Skipping 11-Nil-Tracking-and-Safety.md"
echo "" >> "$TEMP_FILE"
cat Part-3-Advanced-Features/12-Error-Handling-with-Results.md >> "$TEMP_FILE" 2>/dev/null || echo "⚠️  Skipping 12-Error-Handling-with-Results.md"
echo "" >> "$TEMP_FILE"
cat Part-3-Advanced-Features/13-Generics-and-Type-Constraints.md >> "$TEMP_FILE" 2>/dev/null || echo "⚠️  Skipping 13-Generics-and-Type-Constraints.md"
echo "" >> "$TEMP_FILE"
cat Part-3-Advanced-Features/14-Contracts-and-Assertions.md >> "$TEMP_FILE" 2>/dev/null || echo "⚠️  Skipping 14-Contracts-and-Assertions.md"
echo "" >> "$TEMP_FILE"
cat Part-3-Advanced-Features/15-Pipelines-and-Function-Composition.md >> "$TEMP_FILE" 2>/dev/null || echo "⚠️  Skipping 15-Pipelines-and-Function-Composition.md"

# Part 4: Practical Projects
echo "  Part 4: Practical Projects..."
cat >> "$TEMP_FILE" << 'EOF'

# Part 4: Practical Projects

EOF
cat Part-4-Practical-Projects/16-Project-1-CLI-Tool.md >> "$TEMP_FILE" 2>/dev/null || echo "⚠️  Skipping 16-Project-1-CLI-Tool.md"
echo "" >> "$TEMP_FILE"
cat Part-4-Practical-Projects/17-18_Projects-2-3.md >> "$TEMP_FILE" 2>/dev/null || echo "⚠️  Skipping 17-18_Projects-2-3.md"

# Part 5: Ecosystem
echo "  Part 5: Ecosystem..."
cat >> "$TEMP_FILE" << 'EOF'

# Part 5: Ecosystem and Reference

EOF
cat Part-5-Ecosystem/19-22_Final-Chapters.md >> "$TEMP_FILE" 2>/dev/null || echo "⚠️  Skipping 19-22_Final-Chapters.md"

echo "📖 Converting to PDF..."
echo "   (This may take a minute...)"
echo ""

# Build PDF with pandoc
pandoc "$TEMP_FILE" \
  -o "$OUTPUT_FILE" \
  --pdf-engine=xelatex \
  --toc \
  --toc-depth=2 \
  --number-sections \
  --highlight-style=zenburn \
  -V geometry:margin=1in \
  -V geometry:top=1in \
  -V geometry:bottom=1in \
  -V fontsize=11pt \
  -V mainfont="Calibri" \
  -V monofont="Monaco" \
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
