@echo off
setlocal
cd /d "%~dp0"

echo Installing build tools...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller

if errorlevel 1 (
    echo.
    echo Could not install the build tools. Check your Python installation.
    pause
    exit /b 1
)

echo.
echo Building JobFinder.exe...
python -m PyInstaller --noconfirm --clean --onefile --windowed --name JobFinder --icon "assets\jobfinder.ico" --add-data "assets\jobfinder_logo.png;assets" main.py

if exist "dist\JobFinder.exe" (
    echo.
    echo Build complete: dist\JobFinder.exe
) else (
    echo Build failed. Review the messages above.
    pause
    exit /b 1
)
pause
