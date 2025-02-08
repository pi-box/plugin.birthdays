@echo off
set "SOURCE_DIR=src"
set "OUTPUT_ZIP=pi-box.birthdays.zip"

powershell.exe -Command "Compress-Archive -Path '%SOURCE_DIR%\*' -DestinationPath '%OUTPUT_ZIP%' -Force"
