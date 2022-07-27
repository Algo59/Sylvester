import os

import pandas as pd
from telethon.sync import TelegramClient
from datetime import datetime, timedelta
import re
from telethon.tl.functions.messages import GetHistoryRequest
from common import *
from telegrab_project.telegram.config import *
import json
import pickle



def save_all_messages(channels):
    """
    Description:
        save all messages from all channels in last wanted time to a dictionary in wanted path
    """
    all_messages = {}
    with TelegramClient("algo59", API_ID, API_HASH) as client:
        for channel in channels:
            index = 0
            try:
                for message in client.iter_messages(channel, offset_date=datetime.now() - timedelta(hours=HOURS, days=DAYS), reverse=True):
                    if message.text:
                        date = message.date.strftime("%d/%m/%Y")
                        text = message.text
                        all_messages[index] = {"date" : date, "text" : text,  "channel" : channel}
                        index += 1
            except Exception as e:
                print(channel + "\n " + Exception)
    #save json for app
    with open(PATH_TO_ALL_TELE_MESSAGES, "w", encoding="utf-8") as all_messages_file:
        json.dump(all_messages, all_messages_file, indent=4, ensure_ascii=False)
    #save excel for data conservation
    now = datetime.now().strftime("%d_%m_%Y")
    name_for_save = f"month_back_telegram_messages_as_of_{now}.xlsx"
    df = pd.DataFrame.from_dict(data=all_messages, orient='index', columns=["date", "text", "channel"])
    df.to_excel(os.path.join(PATH_TO_TELEGRAM_EXCELS, name_for_save), index=False)




def get_messages():
    try:
        with open(PATH_TO_ALL_TELE_MESSAGES, "r", encoding="utf-8") as dict_file:
            all_messages_dict = json.load(dict_file)
            return all_messages_dict
    except FileNotFoundError:
        print("\n\n\n messages file does not exist, create it by running telemain.py \n\n\n")
        return False


def count_words_in_messages(all_messages_dict: dict, word_list: list, date_range: list):
    """
        Description:
            iterate through all messages in all channels wanted, in wanted dates, and search for occurrences of word in WORDS_LIST
            then create dictionary where keys are words from word list and values are dictionaries where keys are dates and
            values are amount of occurrences:
            example:
                {"hizbala" : {"12/4" : 5, "13/4" :3}}

        :return: word_date_amount dictionary
        """
    word_date_amount_dict = {}
    start_date, end_date = date_range[0], date_range[1]
    for i in all_messages_dict:
        text = all_messages_dict[i]["text"]
        date = all_messages_dict[i]["date"]
        real_date = datetime.strptime(date, "%d/%m/%Y")
        if end_date > real_date > start_date:
            for word in word_list:
                count = len(re.findall(word, text))
                if word in word_date_amount_dict.keys():
                    if date in word_date_amount_dict[word].keys():
                        word_date_amount_dict[word][date] = word_date_amount_dict[word][date] + count
                    else:
                        word_date_amount_dict[word][date] = count
                else:
                    word_date_amount_dict[word] = {date: count}
    return word_date_amount_dict


#channels func
def save_channels_list(channel_list):
    with open(PATH_TO_CHANNELS, "wb") as f:
        pickle.dump(channel_list, f)



def get_channels_list():
    try:
        with open(PATH_TO_CHANNELS, "rb") as f:
            channel_list = pickle.load(f)
            return channel_list
    except FileNotFoundError:
        return False


def add_channel(channel):
    channel_list = get_channels_list()
    channel_list.append(channel)
    save_channels_list(channel_list)


def reset_channels():
    save_channels_list(CHANNELS)


# telegram words funcs
def save_tele_word_list(word_list):
    with open(PATH_TO_TELE_WORDS, "wb") as f:
        pickle.dump(word_list, f)



def get_tele_word_list():
    try:
        with open(PATH_TO_TELE_WORDS, "rb") as f:
            word_list = pickle.load(f)
            return word_list
    except FileNotFoundError:
        return []


def add_tele_word(word):
    word_list = get_tele_word_list()
    word_list.append(word)
    save_tele_word_list(word_list)


def remove_tele_word():
    word_list = get_tele_word_list()
    word_list.pop(-1)
    save_tele_word_list(word_list)


def reset_tele_words():
    save_tele_word_list([])




