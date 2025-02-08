#!/bin/bash

SOURCE_DIR="src"
OUTPUT_ZIP="dist/pi-box.birthdays.zip"

# Create dist directory if it doesn't exist
mkdir -p "dist"

# Compress files into ZIP
zip -r "$OUTPUT_ZIP" "$SOURCE_DIR"

echo "Compression completed: $OUTPUT_ZIP"
