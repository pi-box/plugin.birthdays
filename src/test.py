import requests

BOT_TOKEN = "7648058574:AAG9dZXLvAWjXY9854O_UG0R2XrZx9Ge0WY"
URL = f"https://api.telegram.org/bot{BOT_TOKEN}/getUpdates"

response = requests.get(URL)
updates = response.json()

for update in updates.get("result", [-1002335352740]):
    if "message" in update:
        chat_id = update["message"]["chat"]["id"]
        user = update["message"]["from"]["first_name"]
        text = update["message"]
        print(f"Message from {user} in chat {chat_id}: {text}")
