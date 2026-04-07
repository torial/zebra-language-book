@echo off
REM Convert all SVGs in diagrams folder to PNG using Inkscape
REM Usage: convert-svg-to-png.bat

echo.
echo Converting SVG diagrams to PNG (300 DPI)...
echo.

setlocal enabledelayedexpansion

set "SVG_DIR=diagrams"
set "DPI=300"
set "COUNT=0"

if not exist "%SVG_DIR%" (
    echo Error: %SVG_DIR% directory not found
    pause
    exit /b 1
)

REM Check if Inkscape is available
where inkscape >nul 2>nul
if errorlevel 1 (
    echo Error: Inkscape is not in PATH
    echo Please install: choco install inkscape
    pause
    exit /b 1
)

echo Found Inkscape. Converting diagrams...
echo.

REM Convert each SVG file to PNG
for %%f in ("%SVG_DIR%\*.svg") do (
    set /a COUNT=!COUNT! + 1
    set "FILENAME=%%~nf"
    set "BASENAME=%%~nf"
    echo [!COUNT!] Converting !BASENAME!.svg to !BASENAME!.png...

    REM Use Inkscape to convert SVG to PNG
    inkscape "%%f" --export-type=png --export-dpi=%DPI% --export-filename="%SVG_DIR%\%%~nf.png"

    if errorlevel 1 (
        echo ⚠️  Failed to convert %%f
    ) else (
        echo    ✓ Created %SVG_DIR%\%%~nf.png
    )
)

echo.
echo ✅ Conversion complete! Converted %COUNT% SVG files to PNG at %DPI% DPI.
echo.
pause
