@echo off
setlocal enabledelayedexpansion

echo ================================
echo ⏱ Creating timestamp folder...
echo ================================

REM Get date and time
for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd_HH-mm-ss"') do set DATETIME=%%i

set BUILD_NAME=build_output_%DATETIME%
set BUILD_DIR=%BUILD_NAME%

mkdir %BUILD_DIR%

echo ================================
echo 📦 Copying backend to %BUILD_DIR%...
echo ================================

robocopy backend %BUILD_DIR%\backend /E /XD __pycache__ venv node_modules DB-Script Documentation tests .qodo .vscode logs /XF *.pyc *.pyo .env requirements.txt web.config 

echo ================================
echo 🤐 Zipping package: %BUILD_NAME%.zip
echo ================================

REM This command zips the contents of the new build folder into a zip file with the same name
powershell -NoProfile -Command "Compress-Archive -Path '%BUILD_DIR%\*' -DestinationPath '%BUILD_DIR%\%BUILD_NAME%.zip' -Force"

echo ================================
echo ✅ Build package ready: %BUILD_DIR%
echo ✅ Zip file created: %BUILD_DIR%\%BUILD_NAME%.zip
echo ================================

pause