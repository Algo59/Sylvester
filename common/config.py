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

PATH_TO_CHANNELS = "/Users/algocto/PycharmProjects/sylvester/telegrab_project/telegram/config/channels_list.pkl"
PATH_TO_TELE_WORDS = "/Users/algocto/PycharmProjects/sylvester/telegrab_project/telegram/config/tele_word_list.pkl"
PATH_TO_TWIT_WORDS = "/Users/algocto/PycharmProjects/sylvester/telegrab_project/telegram/config/twit_word_list.pkl"