from telethon.sync import TelegramClient
from datetime import datetime, timedelta
import re
from telethon.tl.functions.messages import GetHistoryRequest
from common import WORD_LIST, COMBINATIONS, PATH_TO_CHANNELS
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
                        date = message.date.strftime("%d/%m")
                        text = message.text
                        all_messages[index] = {"text" : text, "date" : date}
                        index += 1
            except Exception as e:
                print(channel + "\n " + Exception)

    with open(PATH_TO_ALL_MESSAGES, "w", encoding="utf-8") as all_messages_file:
        json.dump(all_messages, all_messages_file, indent=4, ensure_ascii=False)


def get_messages():
    try:
        with open(PATH_TO_ALL_MESSAGES, "r", encoding="utf-8") as dict_file:
            all_messages_dict = json.load(dict_file)
            return all_messages_dict
    except FileNotFoundError:
        print("\n\n\n messages file does not exist, create it by running telemain.py \n\n\n")
        return False

def count_words_in_messages(all_messages_dict: dict, word_list: list):
    """
        Description:
            iterate through all messages in all channels wanted, and search for occurrences of word in WORDS_LIST
            then create dictionary where keys are words from word list and values are dictionaries where keys are dates and
            values are amount of occurrences:
            example:
                {"hizbala" : {"12/4" : 5, "13/4" :3}}

        :return: word_date_amount dictionary
        """
    word_date_amount_dict = {}
    for i in all_messages_dict:
        text = all_messages_dict[i]["text"]
        date = all_messages_dict[i]["date"]
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


def count_combinations_in_messages(all_messages_dict) -> dict:
    """
       Description:
           iterate through all messages in all channels wanted, and search for occurrences of combinations in
           COMBINATION_LIST then create dictionary where keys are combinations from word list and values
           are dictionaries where keys are dates and
           values are amount of occurrences:
           example:
               {("hizbala", "haslama") : {"12/4" : 5, "13/4" :3}}

       :return: comb_date_amount dictionary
       """
    comb_date_amount_dict = {}
    word_date_amount_dict = {}
    for i in all_messages_dict:
        text = all_messages_dict[i]["text"]
        date = all_messages_dict[i]["date"]
        for word in WORD_LIST:
            for comb in COMBINATIONS:
                for word in comb:
                    if word not in message.text:
                        break
                else:
                    date = message.date.strftime("%d/%m")
                    if comb in comb_date_amount_dict.keys():
                        if date in comb_date_amount_dict[comb].keys():
                            comb_date_amount_dict[comb][date] = comb_date_amount_dict[comb][date] + 1
                        else:
                            comb_date_amount_dict[comb][date] = 1
                    else:
                        comb_date_amount_dict[comb] = {date: 1}
    return comb_date_amount_dict


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