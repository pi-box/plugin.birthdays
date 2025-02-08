#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""
setup.py - Configuration and setup script for Pi-Box Birthdays Plugin

This script is responsible for authenticating and configuring the Telegram bot, 
including creating and saving a configuration file.

Main functionalities:
1. Load configuration data from a JSON file if available.
2. Authenticate and establish a connection with Telegram using Pyrogram.
3. Request missing configuration details from the user.
4. Save authentication and configuration data for future use.
"""

import os
import json
import sysconfig
from pyrogram import Client

# Define the base directory of the script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    """
    Main function to manage the bot setup and authentication process.
    """
    BOT_FILE = "bot"  # Session file name for Pyrogram
    CONFIG_FILE = os.path.join(BASE_DIR, "telegram.config")  # Path to the configuration file
    
    config_data = {}
    
    # Check if the configuration file exists and load data if available
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config_data = json.load(file)
    
    try:
        # Attempt to authenticate using an existing session file
        bot = Client(BOT_FILE)
        bot.start()
        print("Authentication successful! Session file exists.")
    except Exception as e:
        print("Session file not found or invalid. Setting up a new session...")
        
        # Request authentication details from the user if missing from config
        api_id = config_data.get("api_id") or int(input("Enter your Telegram API ID: "))
        api_hash = config_data.get("api_hash") or input("Enter your Telegram API Hash: ").strip()
        bot_token = config_data.get("bot_token") or input("Enter your Telegram Bot Token: ").strip()
        
        # Initialize a new Telegram client session
        bot = Client(BOT_FILE, api_id=api_id, api_hash=api_hash, bot_token=bot_token)
        bot.start()
        print("Authentication successful! Session file created.")
    
    # Request the group link if not already stored
    if "group_link" not in config_data:
        group_link = input("Enter your Telegram group link (e.g., @your_group_link_here): ").strip()
        config_data.update({"group_link": group_link})
    
    # Save configuration data to a JSON file for future use
    with open(CONFIG_FILE, "w") as file:
        json.dump(config_data, file, indent=4)
    
    print("Configuration saved successfully.")
    
if __name__ == "__main__":
    main()
