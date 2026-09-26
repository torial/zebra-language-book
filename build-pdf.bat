@echo off
REM Zebra Programming Book - PDF Builder (Windows)
REM Usage: build-pdf.bat
REM Prerequisites: pandoc (choco install pandoc, or download from https://pandoc.org/installing.html)

setlocal enabledelayedexpansion

echo.
echo 🔨 Building Zebra Programming Book PDF...
echo.

REM Set global Zebra project variable if not already set
if not defined ZEBRA_PROJECT (
    set "ZEBRA_PROJECT=C:\Projects\zebra-language-book"
)
set "BOOK_DIR=book"
set "ZEBRA_DIAGRAMS=%ZEBRA_PROJECT%\%BOOK_DIR%\diagrams"
echo 📂 ZEBRA_PROJECT=%ZEBRA_PROJECT%
echo 🖼️  ZEBRA_DIAGRAMS=%ZEBRA_DIAGRAMS%

REM Check if pandoc is installed
where pandoc >nul 2>nul
if errorlevel 1 (
    echo ❌ Pandoc is not installed.
    echo.
    echo Install it using one of these methods:
    echo   1. Chocolatey: choco install pandoc
    echo   2. Download:   https://pandoc.org/installing.html
    echo   3. Scoop:      scoop install pandoc
    echo.
    pause
    exit /b 1
)

REM Set variables
set TEMP_FILE=%TEMP%\zebra-book-combined.md
set OUTPUT_FILE=zebra-programming-book.pdf

REM Note: SVG to PNG conversion and markdown updates should be done manually first:
REM   1. convert-svg-to-png.bat
REM   2. python update-image-refs.py
REM Then run this script for PDF generation

echo.
echo 📚 Combining chapters...
echo.

REM The chapter list is book\SUMMARY.md -- the same list the website is built from --
REM written out by book_combine.py. This script used to hand-list every chapter and had
REM drifted (07b and 18b were missing from every PDF).
python book_combine.py "%TEMP_FILE%"
if errorlevel 1 (
    echo ❌ book_combine.py failed -- see above
    pause
    exit /b 1
)

REM Build PDF with pandoc
REM Note: Using xelatex which is more reliable with image handling
pandoc "%TEMP_FILE%" ^
  -o "%OUTPUT_FILE%" ^
  --pdf-engine=xelatex ^
  --toc ^
  --toc-depth=2 ^
  --number-sections ^
  --syntax-highlighting=zenburn ^
  --metadata author="Zebra Community"

REM Check if successful
if exist "%OUTPUT_FILE%" (
    echo.
    echo ✅ PDF successfully created!
    echo    File: %OUTPUT_FILE%
    echo.
    echo 📖 Opening PDF...
    start "%OUTPUT_FILE%"
) else (
    echo.
    echo ❌ Failed to create PDF
    echo.
    pause
    exit /b 1
)

REM Cleanup
if exist "%TEMP_FILE%" del "%TEMP_FILE%"

echo.
echo Done!
pause
