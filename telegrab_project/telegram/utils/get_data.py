from telethon.sync import TelegramClient
from datetime import datetime, timedelta
import re
from telethon.tl.functions.messages import GetHistoryRequest
from telegrab_project.telegram.config import *
import json


def count_words_in_messages() -> dict:
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
    with TelegramClient("algo59", API_ID, API_HASH) as client:
        for channel in CHANNELS:
            for message in client.iter_messages(channel, offset_date=datetime.now() - timedelta(hours=HOURS, days=DAYS), reverse=True):
                if message.text:
                    for word in WORD_LIST:
                        count = len(re.findall(word, message.text))
                        date = message.date.strftime("%d/%m")
                        if word in word_date_amount_dict.keys():
                            if date in word_date_amount_dict[word].keys():
                                word_date_amount_dict[word][date] = word_date_amount_dict[word][date] + count
                            else:
                                word_date_amount_dict[word][date] = count
                        else:
                            word_date_amount_dict[word] = {date: count}
    return word_date_amount_dict


def count_combinations_in_messages() -> dict:
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
    with TelegramClient("algo59", API_ID, API_HASH) as client:
        for channel in CHANNELS:
            for message in client.iter_messages(channel,
                                                offset_date=datetime.now() - timedelta(hours=HOURS, days=DAYS),
                                                reverse=True):
                if message.text:
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


def save_temp_dict(dic):
    with open("message_dict.json", "w", encoding="utf-8") as dict_file:
        json.dump(dic, dict_file, indent=4, ensure_ascii=False)


def get_temp_dict():
    try:
        with open("message_dict.json", "r", encoding="utf-8") as dict_file:
            amount_dict = json.load(dict_file)
            return amount_dict
    except:
        return False