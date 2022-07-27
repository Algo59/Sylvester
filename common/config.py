import getpass
import numpy as np
import os
TOPICS = {
    "حزب الله" : "חזבאלה" ,
    "انتخابات" : "בחירות" ,
    "الطيران الإسراأيلي" : "כלי הטיס הישראלים",
    "العدو الإسراأيلي" : "האויב הישראלי",
    "العدو الصهيوني" : "האויב הציוני",
    "تركيب سياج" : "התקנת גדר",
    "تصعيد" : "הסלמה",
    "جنوب لبنان" : "דרום לבנון",
    "حدود" : "גבולות",
    "انفجار" : "פיצוץ",
}
COMBINATIONS = [("الطيران الإسراأيلي", "العدو الإسراأيلي", "العدو الصهيوني"), ("حزب الله", "العدو الإسراأيلي"),
                ("حزب الله", "العدو الصهيوني"), ("تركيب سياج", "تصعيد"), ("العدو الإسراأيلي", "تركيب سياج"),
                ("حزب الله", "تصعيد"), ("حزب الله", "جنوب لبنان"), ("الطيران الإسراأيلي", "انفجار"),
                ("تركيب سياج", "حدود")]

WORD_LIST = list(TOPICS.keys())
user = getpass.getuser()
PATH_TO_CHANNELS = f"/Users/{user}/PycharmProjects/sylvester/telegrab_project/telegram/config/channels_list.pkl"
PATH_TO_TELE_WORDS = f"/Users/{user}/PycharmProjects/sylvester/telegrab_project/telegram/config/tele_word_list.pkl"
PATH_TO_TWIT_WORDS = f"/Users/{user}/PycharmProjects/sylvester/twit/config/twit_word_list.pkl"
PATH_TO_TWIT_DATA_FILE = f"/Users/{user}/PycharmProjects/sylvester/twitter_data/twit_knwoledge.xlsx"
PATH_TO_TELEGRAM_EXCELS = f"/Users/{user}/PycharmProjects/sylvester/telegram_data/all_time_telegram_data"
PATH_TO_ALL_TELE_MESSAGES = f"/Users/{user}/PycharmProjects/sylvester/telegram_data/current_telegram_messages.json"
TWIT_DATA_FOLDER_PATH = f"/Users/{user}/PycharmProjects/sylvester/twitter_data"
TELE_DATA_FOLDER_PATH = rf"/Users/{user}/Downloads/telegram_data"
TEMP_PATH_TO_FIG = os.path.join(TWIT_DATA_FOLDER_PATH, "temp_fig.png")
rand_spair_colors = color_list = [tuple(np.random.uniform(0,1,[3])) for x in range(30)]
COLOR_LIST = [(1.0, 0.59, 0.36), (0.36, 1.0, 0.99), (0.36, 1.0, 0.48), (0.87, 0.36, 1.0), (1.0, 1.0, 0.36), (0.36, 0.67, 0.72), (0.82, 0.8, 0.77), (0.79, 0.56, 0.56), (0.82, 0.74, 1.0), (1.0, 0.74, 0.87), (0.3, 0.11, 1.0), (0.71, 0.53, 0.4)] + rand_spair_colors


BACKGROUND_COLOR = (40/255, 46/255, 60/255)
TEXT_COLOR = 'white'