import os, json
import sysconfig
from pyrogram import Client
from datetime import datetime

# Global variables
CLI_DIR = "" if os.name == 'nt' else sysconfig.get_path("scripts")
CONFIG_FILE = os.path.join(CLI_DIR, "telegram.config")
DB_FILE = os.path.join(CLI_DIR, "messages.db")

# Initialize the Telegram client
bot = Client("bot")

def load_config():
    """Load configuration data from the config file."""
    try:
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading config file: {e}")
        return {}

config_data = load_config()
group_link = config_data.get("group_link")
if not group_link:
    raise ValueError("Group link not found in config file.")

def get_all_messages():
    try:
        with open(DB_FILE, "r") as file:
            messages = json.load(file)  # Load existing data
    except (FileNotFoundError, json.JSONDecodeError):
        messages = []  # If file doesn't exist or is empty, start with an empty list

    return messages

def add_message(message):
    messages = get_all_messages()

    message_data = {
        "id": message.id,
        "caption": message.caption,
        "date": message.date.isoformat(),
    }
    messages.append(message_data)  # Append new message

    with open(DB_FILE, "w") as file:
        json.dump(messages, file, indent=4)  # Save updated array

def delete_old_videos(caption, date_to_keep):
    """
    Deletes all video messages in a given Telegram group that contain a specific caption 
    and were not sent on a specific date.

    :param caption: The caption text to match for deletion.
    :param date_to_keep: The date (YYYY-MM-DD) to keep messages.
    """

    with bot:
        messages = get_all_messages()
        updated_messages = []  # Create a new list for messages to keep
        
        for message in messages:
            if message["caption"] and message["caption"].strip() == caption.strip():
                message_date = datetime.fromisoformat(message["date"]).date()
                if message_date != date_to_keep:
                    print(f"Deleting video message ID {message['id']} from {message_date}...")
                    bot.delete_messages(group_link, message["id"])
                    continue  # Skip adding this message to updated_messages

            updated_messages.append(message)  # Keep the message if it wasn't deleted

        with open(DB_FILE, "w") as file:
            json.dump(updated_messages, file, indent=4)  # Save updated array

        print("Deletion process completed!")

def upload_video(video_path, caption):
    """
    Uploads a video to a Telegram group as a bot.

    :param video_path: The file path of the video to upload.
    :param caption: Optional caption for the video.
    """
    with bot:
        message = bot.send_video(
            chat_id=group_link,
            video=video_path,
            caption=caption,
            supports_streaming=True  # Enables Telegram streaming
        )
        add_message(message)

    print("Video uploaded successfully!")
    return message
