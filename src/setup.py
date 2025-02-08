import os
import json
import sysconfig
from pyrogram import Client

def main():
    BOT_FILE = "bot"
    CONFIG_FILE = "telegram.config"
    
    config_data = {}
    
    # Check if the config file exists and load it if available
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            config_data = json.load(file)
    
    try:
        # Initialize client using existing session
        bot = Client(BOT_FILE)
        bot.start()
        print("Authentication successful! Session file exists.")
    except Exception as e:
        print("Session file not found or invalid. Setting up a new session...")
        
        # Get API credentials from user if not in config
        api_id = config_data.get("api_id") or int(input("Enter your Telegram API ID: "))
        api_hash = config_data.get("api_hash") or input("Enter your Telegram API Hash: ").strip()
        bot_token = config_data.get("bot_token") or input("Enter your Telegram Bot Token: ").strip()
        
        # Initialize the Telegram client
        bot = Client(BOT_FILE, api_id=api_id, api_hash=api_hash, bot_token=bot_token)
        bot.start()
        print("Authentication successful! Session file created.")
    
    # Ask for group link if not already stored
    if "group_link" not in config_data:
        group_link = input("Enter your Telegram group link (e.g., @your_group_link_here): ").strip()
        config_data.update({"group_link": group_link})
    
    # Save config data to file
    with open(CONFIG_FILE, "w") as file:
        json.dump(config_data, file, indent=4)
    
    print("Configuration saved successfully.")
    
if __name__ == "__main__":
    main()
