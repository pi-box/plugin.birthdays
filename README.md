# Pi-Box\_birthdays Plugin

Pi-Box\_birthdays is a plugin for the Pi-Box multimedia system that automates birthday greetings through the Telegram group. It retrieves birthday details from an Excel file, removes outdated videos, and uploads the relevant birthday greeting video daily.

## Features

- Automatically sends a birthday greeting video to a Telegram group based on an Excel list.
- Deletes outdated birthday videos to keep the group clean.
- Runs as a scheduled service (cron job) for full automation.

## Installation

### Prerequisites

Ensure your system has the required dependencies:

```bash
sudo apt update
sudo apt install -y python3-pip git
sudo apt install -y ffmpeg
sudo pip install TgCrypto pyrogram pandas pillow openpyxl
```

### Download and Setup

Navigate to the installation directory and download the plugin:

```bash
cd /usr/local/bin/
sudo mkdir pibox_birthdays
cd pibox_birthdays/
sudo wget https://github.com/pi-box/plugin.birthdays/raw/refs/heads/main/dist/pibox.birthdays.zip
sudo unzip pibox.birthdays.zip
sudo rm pibox.birthdays.zip
```

#### Making the Telegram Group Public

Make the Telegram group **public** so the bot can post messages, and note its group link (e.g., `@your_group_link`).

#### Telegram Bot Configuration

To enable Telegram functionality, create and configure a bot:

1. Create a bot via [BotFather](https://t.me/botfather) on Telegram.

2. Obtain the bot token.

3. Add the bot to the Telegram group.

4. Grant the bot permissions to send messages in the group.

#### Running Configuration Setup

Run the setup script to configure the bot:

```bash
sudo python3 setup.py
```

Follow the prompts and enter:

- Telegram API ID
- Telegram API Hash
- Telegram Bot Token
- Telegram Group Link

## Updating the Birthday List

The plugin uses an Excel file (`birthdays.xlsx`) located in the `assets` directory to determine birthdays. Update this file with the names and birth dates of all recipients.

## Running the Plugin

To manually run the plugin:

```bash
sudo python3 pibox.birthdays.py
```

To automate execution, set up a cron job to run the script daily at midnight:

```bash
sudo crontab -e
```

Add the following line:

```bash
0 0 * * * /usr/bin/python3 /usr/local/bin/pibox_birthdays/pibox.birthdays.py
```

## Development and Packaging

To modify and package the plugin:

1. Clone the repository:
   ```bash
   git clone https://github.com/pi-box/plugin.birthdays.git
   ```
2. Make changes as needed.
3. Create a new ZIP package:
   - On Windows: Run `compress.bat`
   - On Linux/Mac: Run `compress.sh`

This will generate a new ZIP file in the `dist` folder, ready for deployment.

## License

This project is open-source under the MIT License.

## Support

For issues and contributions, visit the [GitHub repository](https://github.com/pi-box/plugin.birthdays).

