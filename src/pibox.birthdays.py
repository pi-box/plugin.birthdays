#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
pibox.birthdays.py - Main script for Pi-Box Birthdays Plugin

This script automates the process of sending birthday greetings via a Telegram group.
It performs the following tasks:

1. Reads an Excel file containing a list of birthdays.
2. Identifies birthdays that match the current date.
3. Generates a personalized birthday video.
4. Uploads the birthday video to the designated Telegram group.
5. Deletes outdated videos to keep the group clean.

Dependencies:
- load_birthdays.py: Parses the Excel file and retrieves today's birthdays.
- video_handler.py: Handles the video processing.
- telegram.py: Manages Telegram interactions (uploading and deleting videos).

Usage:
This script is intended to be run as a scheduled job (e.g., via cron) to ensure daily execution.
"""

import os
from datetime import datetime

import load_birthdays
import video_handler
import telegram

# Define base directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def main():
    """
    Main function that orchestrates the birthday greeting process.
    """
    xlsx_path = os.path.join(ASSETS_DIR, "birthdays.xlsx")  # Path to the birthdays list
    video_template = os.path.join(ASSETS_DIR, "birthday.mp4")  # Template video for greetings
    video_caption = "birthday"  # Caption used to identify birthday videos
    today = datetime.today().date()  # Get today's date

    # Remove outdated birthday videos
    telegram.delete_old_videos(video_caption, today)
    
    # Retrieve today's birthdays
    birthdays_today = load_birthdays.find_birthdays_today(xlsx_path, today)

    # Process each birthday person
    for name in birthdays_today:
        output_video = os.path.join(ASSETS_DIR, f"{name}.mp4")
        
        # Generate a personalized birthday video
        video_handler.create(ASSETS_DIR, name, video_template, output_video)
        
        # Upload the generated video to the Telegram group
        telegram.upload_video(output_video, video_caption)
        
        # Remove the temporary video file to save space
        os.remove(output_video)

if __name__ == "__main__":
    main()
