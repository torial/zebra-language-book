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
set "ZEBRA_DIAGRAMS=%ZEBRA_PROJECT%\diagrams"
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

REM Clear temp file
if exist "%TEMP_FILE%" del "%TEMP_FILE%"

REM Add title page
(
echo ---
echo title: The Zebra Programming Language
echo subtitle: A Modern Language with Safety and Performance
echo author: Zebra Community
echo date: April 2026
echo lang: en
echo toc: true
echo toc-depth: 2
echo number-sections: true
echo ---
echo.
) > "%TEMP_FILE%"

REM Part 1: Foundations
echo   Part 1: Foundations...
(
echo # Part 1: Foundations
echo.
) >> "%TEMP_FILE%"

if exist "Part-1-Foundations\01-Getting-Started.md" (
    type "Part-1-Foundations\01-Getting-Started.md" >> "%TEMP_FILE%"
) else (
    echo ⚠️  Skipping 01-Getting-Started.md
)
echo. >> "%TEMP_FILE%"

if exist "Part-1-Foundations\02-Values-and-Types.md" (
    type "Part-1-Foundations\02-Values-and-Types.md" >> "%TEMP_FILE%"
) else (
    echo ⚠️  Skipping 02-Values-and-Types.md
)
echo. >> "%TEMP_FILE%"

if exist "Part-1-Foundations\03-Collections.md" (
    type "Part-1-Foundations\03-Collections.md" >> "%TEMP_FILE%"
) else (
    echo ⚠️  Skipping 03-Collections.md
)
echo. >> "%TEMP_FILE%"

if exist "Part-1-Foundations\04-Functions-and-Scope.md" (
    type "Part-1-Foundations\04-Functions-and-Scope.md" >> "%TEMP_FILE%"
) else (
    echo ⚠️  Skipping 04-Functions-and-Scope.md
)
echo. >> "%TEMP_FILE%"

if exist "Part-1-Foundations\05-Control-Flow.md" (
    type "Part-1-Foundations\05-Control-Flow.md" >> "%TEMP_FILE%"
) else (
    echo ⚠️  Skipping 05-Control-Flow.md
)
echo. >> "%TEMP_FILE%"

if exist "Part-1-Foundations\06-Strings-and-Unicode.md" (
    type "Part-1-Foundations\06-Strings-and-Unicode.md" >> "%TEMP_FILE%"
) else (
    echo ⚠️  Skipping 06-Strings-and-Unicode.md
)

REM Part 2: Objects & Interfaces
echo   Part 2: Objects ^& Interfaces...
(
echo.
echo # Part 2: Objects and Interfaces
echo.
) >> "%TEMP_FILE%"

if exist "Part-2-Objects-and-Interfaces\07-Classes-and-Instances.md" (
    type "Part-2-Objects-and-Interfaces\07-Classes-and-Instances.md" >> "%TEMP_FILE%"
) else (
    echo ⚠️  Skipping 07-Classes-and-Instances.md
)
echo. >> "%TEMP_FILE%"

if exist "Part-2-Objects-and-Interfaces\08-Interfaces-and-Protocols.md" (
    type "Part-2-Objects-and-Interfaces\08-Interfaces-and-Protocols.md" >> "%TEMP_FILE%"
) else (
    echo ⚠️  Skipping 08-Interfaces-and-Protocols.md
)
echo. >> "%TEMP_FILE%"

if exist "Part-2-Objects-and-Interfaces\09-Inheritance-and-Mixins.md" (
    type "Part-2-Objects-and-Interfaces\09-Inheritance-and-Mixins.md" >> "%TEMP_FILE%"
) else (
    echo ⚠️  Skipping 09-Inheritance-and-Mixins.md
)
echo. >> "%TEMP_FILE%"

if exist "Part-2-Objects-and-Interfaces\10-Properties-and-Computed-Values.md" (
    type "Part-2-Objects-and-Interfaces\10-Properties-and-Computed-Values.md" >> "%TEMP_FILE%"
) else (
    echo ⚠️  Skipping 10-Properties-and-Computed-Values.md
)

REM Part 3: Advanced Features
echo   Part 3: Advanced Features...
(
echo.
echo # Part 3: Advanced Features
echo.
) >> "%TEMP_FILE%"

if exist "Part-3-Advanced-Features\11-Nil-Tracking-and-Safety.md" (
    type "Part-3-Advanced-Features\11-Nil-Tracking-and-Safety.md" >> "%TEMP_FILE%"
) else (
    echo ⚠️  Skipping 11-Nil-Tracking-and-Safety.md
)
echo. >> "%TEMP_FILE%"

if exist "Part-3-Advanced-Features\12-Error-Handling-with-Results.md" (
    type "Part-3-Advanced-Features\12-Error-Handling-with-Results.md" >> "%TEMP_FILE%"
) else (
    echo ⚠️  Skipping 12-Error-Handling-with-Results.md
)
echo. >> "%TEMP_FILE%"

if exist "Part-3-Advanced-Features\13-Generics-and-Type-Constraints.md" (
    type "Part-3-Advanced-Features\13-Generics-and-Type-Constraints.md" >> "%TEMP_FILE%"
) else (
    echo ⚠️  Skipping 13-Generics-and-Type-Constraints.md
)
echo. >> "%TEMP_FILE%"

if exist "Part-3-Advanced-Features\14-Contracts-and-Assertions.md" (
    type "Part-3-Advanced-Features\14-Contracts-and-Assertions.md" >> "%TEMP_FILE%"
) else (
    echo ⚠️  Skipping 14-Contracts-and-Assertions.md
)
echo. >> "%TEMP_FILE%"

if exist "Part-3-Advanced-Features\15-Pipelines-and-Function-Composition.md" (
    type "Part-3-Advanced-Features\15-Pipelines-and-Function-Composition.md" >> "%TEMP_FILE%"
) else (
    echo ⚠️  Skipping 15-Pipelines-and-Function-Composition.md
)

REM Part 4: Practical Projects
echo   Part 4: Practical Projects...
(
echo.
echo # Part 4: Practical Projects
echo.
) >> "%TEMP_FILE%"

if exist "Part-4-Practical-Projects\16-Project-1-CLI-Tool.md" (
    type "Part-4-Practical-Projects\16-Project-1-CLI-Tool.md" >> "%TEMP_FILE%"
) else (
    echo ⚠️  Skipping 16-Project-1-CLI-Tool.md
)
echo. >> "%TEMP_FILE%"

if exist "Part-4-Practical-Projects\17-18_Projects-2-3.md" (
    type "Part-4-Practical-Projects\17-18_Projects-2-3.md" >> "%TEMP_FILE%"
) else (
    echo ⚠️  Skipping 17-18_Projects-2-3.md
)

REM Part 5: Ecosystem
echo   Part 5: Ecosystem...
(
echo.
echo # Part 5: Ecosystem and Reference
echo.
) >> "%TEMP_FILE%"

if exist "Part-5-Ecosystem\19-22_Final-Chapters.md" (
    type "Part-5-Ecosystem\19-22_Final-Chapters.md" >> "%TEMP_FILE%"
) else (
    echo ⚠️  Skipping 19-22_Final-Chapters.md
)

echo.
echo 🔧 Fixing diagram paths...
if exist "fix-diagram-paths.py" (
    python fix-diagram-paths.py "%TEMP_FILE%" "%TEMP_FILE%" "%ZEBRA_DIAGRAMS%"
) else (
    echo ⚠️  fix-diagram-paths.py not found
)

echo.
echo 📖 Converting to PDF...
echo    (This may take a minute...)
echo.

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
