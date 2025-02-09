#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
telegram.py - Telegram Bot Management for Pi-Box Birthdays Plugin

This module handles interactions with Telegram, including sending and deleting birthday videos.
It connects to the Telegram API using Pyrogram and manages video messages within a group.

Functionality:
1. Loads bot configuration details from a JSON file.
2. Uploads birthday greeting videos to a specified Telegram group.
3. Deletes outdated videos to keep the group clean.
4. Maintains a local database of sent messages for tracking purposes.
5. Provides direct HTTP-based video upload to Telegram API.

Dependencies:
- Pyrogram: For interacting with the Telegram API.
- requests: For direct HTTP requests to Telegram API.
- JSON: For handling configuration and message storage.
- os: For file path operations.
- datetime: For managing message timestamps.

Usage:
This module is used by `pibox.birthdays.py` to upload birthday videos and remove old ones.
"""

import os
import json
import requests
from pyrogram import Client
from datetime import datetime

# Define base directory and configuration file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(BASE_DIR, "telegram.config")
DB_FILE = os.path.join(BASE_DIR, "messages.db")

def load_config():
    """
    Load configuration data from the config file.
    
    :return: Dictionary containing configuration data.
    """
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading config file: {e}")
        return {}

config_data = load_config()
bot_token = config_data.get("bot_token")
group_id = config_data.get("group_id")
if not bot_token or not group_id:
    raise ValueError("Bot token or group ID not found in config file.")

def get_all_messages():
    """
    Retrieves all stored messages from the local database.
    
    :return: List of stored message metadata.
    """
    try:
        with open(DB_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def add_message(message):
    """
    Adds a new message entry to the local message database.
    
    :param message: Telegram message object.
    """
    messages = get_all_messages()
    
    message_data = {
        "id": message.id,
        "caption": message.caption,
        "date": message.date.isoformat(),
    }
    messages.append(message_data)
    
    with open(DB_FILE, "w") as file:
        json.dump(messages, file, indent=4)

def delete_old_videos(caption, date_to_keep):
    """
    Deletes old video messages in the Telegram group that match a specific caption
    and were not sent on the specified date.
    
    :param caption: The caption text used to identify birthday videos.
    :param date_to_keep: The date of the messages to retain (YYYY-MM-DD format).
    """
    bot = Client("bot")
    with bot:
        messages = get_all_messages()
        updated_messages = []
        
        for message in messages:
            if message["caption"] and message["caption"].strip() == caption.strip():
                message_date = datetime.fromisoformat(message["date"]).date()
                if message_date != date_to_keep:
                    print(f"Deleting video message ID {message['id']} from {message_date}...")
                    bot.delete_messages(group_id, message["id"])
                    continue  # Do not retain deleted messages
            updated_messages.append(message)
        
        with open(DB_FILE, "w") as file:
            json.dump(updated_messages, file, indent=4)
        
        print("Deletion process completed!")

def upload_video(video_path, caption):
    """
    Uploads a video to a Telegram group using the bot API.
    
    :param video_path: Path to the video file to upload.
    :param caption: Caption text for the video.
    """
    url = f"https://api.telegram.org/bot{bot_token}/sendVideo"
    
    with open(video_path, "rb") as video_file:
        response = requests.post(url, data={"chat_id": group_id, "caption": caption}, files={"video": video_file})
    
    if response.status_code == 200:
        print("✅ הווידאו נשלח בהצלחה!")
    else:
        print(f"❌ שגיאה בשליחה: {response.text}")
