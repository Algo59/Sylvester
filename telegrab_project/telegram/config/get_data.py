from datetime import datetime, timedelta
API_ID = 18690322
API_HASH = "e81cc2024ef52e8c743512032db44e5f"
PHONE_NUM = +972508661382
HOURS = 0
DAYS = 7
CHANNELS = ["https://t.me/Lebanon_24", "https://t.me/lbworldnews"]
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
WORD_LIST = TOPICS.keys()