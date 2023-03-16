import asyncio
import os
from aiogram import Bot, Dispatcher
from schedule import get_schedule
import dotenv
import json
from datetime import datetime
import telebot


dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = Bot(TOKEN)
bot_telebot = telebot.TeleBot(TOKEN)  # Your token here
dp = Dispatcher(bot)
YOUR_CHAT_ID = int()
YOUR_GROUP_NAME = ""
with open('groups.json', 'r', encoding='utf-8') as f:
    groups = json.load(f)


async def main():
    print("Bot is waiting.")
    while True:
        if datetime.now().strftime("%H:%M") == "8:00":
            print("Message has been sent.")
        await asyncio.create_task(bot.send_message(chat_id=YOUR_CHAT_ID, text=get_schedule(YOUR_GROUP_NAME)))
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())

