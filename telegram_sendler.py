import os
import logging
from telegram import Bot
from dotenv import load_dotenv

load_dotenv('config.env')

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

logging.basicConfig(level=logging.INFO)


def send_message_to_telegram(name, email, message_content):
    if not BOT_TOKEN or not CHAT_ID:
        logging.error("Telegram credentials are missing!")
        return

    try:
        bot = Bot(token=BOT_TOKEN)

        msg_text = f"New message from {name} ({email}):\n\n{message_content}"

        bot.send_message(chat_id=CHAT_ID, text=msg_text)
        logging.info(f"Message sent to Telegram successfully for {name} ({email})")

    except Exception as e:
        logging.error(f"Failed to send message to Telegram: {e}")
