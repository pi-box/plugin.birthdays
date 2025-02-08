@echo off
setlocal

:: Define variables
set "SOURCE_DIR=src"
set "OUTPUT_ZIP=dist\pi-box.birthdays.zip"

:: Create dist directory if it doesn't exist
if not exist "dist" mkdir "dist"

:: Compress files into ZIP
powershell.exe -Command "Compress-Archive -Path '%SOURCE_DIR%\*' -DestinationPath '%OUTPUT_ZIP%' -Force"

