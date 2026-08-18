@echo off
setlocal
cd /d "%~dp0"

echo Installing build dependencies...
python -m pip install --upgrade pip
python -m pip install -r requirements-build.txt

echo Building standalone Windows executable...
python -m PyInstaller --noconfirm --clean invitation_studio.spec

echo.
if exist "dist\Would Kill For Pie.exe" (
  echo Build succeeded:
  echo   dist\Would Kill For Pie.exe
) else (
  echo Build failed. Check the PyInstaller output above.
  exit /b 1
)
