#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
from datetime import datetime

import load_birthdays
import video_handler
import telegram

# Global variables
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")

def main():
    xlsx_path = os.path.join(ASSETS_DIR, "birthdays.xlsx")
    video_template = os.path.join(ASSETS_DIR, "birthday.mp4")
    video_caption = "birthday"
    today = datetime.today().date() # Define today's date

    telegram.delete_old_videos(video_caption, today)
    birthdays_today = load_birthdays.find_birthdays_today(xlsx_path, today)

    for name in birthdays_today:
        output_video = os.path.join(ASSETS_DIR, f"{name}.mp4")
        video_handler.create(ASSETS_DIR, name, video_template, output_video)
        telegram.upload_video(output_video, video_caption)
        os.remove(output_video)

if __name__ == "__main__":
    main()
