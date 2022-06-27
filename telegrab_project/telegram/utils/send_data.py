from telethon.sync import TelegramClient
from datetime import datetime, timedelta
import re
from telegrab_project.telegram.config import *


def send_message(to, text):
    with TelegramClient("algo59", API_ID, API_HASH) as client:
        client.send_message(to, text)


def send_file(to, path):
    with TelegramClient("algo59", API_ID, API_HASH) as client:
        client.send_file(to, path)
