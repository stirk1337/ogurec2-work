import os
from datetime import timezone, timedelta

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
TELEGRAM_API_ID = os.getenv('TELEGRAM_API_ID')
TELEGRAM_API_HASH = os.getenv('TELEGRAM_API_HASH')
TENOR_API_KEY = os.getenv('TENOR_API_KEY')

TIME_ZONE = timezone(timedelta(hours=5))  # Russia, Ekaterinburg

BOT_CHAT_ID = 749662464538443948
MAIN_CHAT_ID = 670981415306788870

GPT_TELEGRAM_NAME_STR = 'gpt3_unlim_chatbot'
MAXIMUM_GPT_MESSAGE_LENGTH = 50
