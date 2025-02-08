#!/bin/bash

SOURCE_DIR="src"
OUTPUT_ZIP="pi-box.birthdays.zip"

zip -r "$OUTPUT_ZIP" "$SOURCE_DIR"
echo "Compression completed: $OUTPUT_ZIP"
