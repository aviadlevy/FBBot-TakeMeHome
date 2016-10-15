# coding=utf-8
DEFAULT_MSG = """Please Choose you language by sending "set lang <number>"
1. English
2. Hebrew
And set your location by sending "set home <your home>\""""
FB_MAX_LENGTH = 320
LINE = {"iw": " קו ".decode("utf-8"),
        "en": " number "}
ARRIVING_AT = {"iw": " שמגיע לתחנה ב ".decode("utf-8"),
               "en": " that arriving to the station at "}
DEST_TIME = {"iw": " ומגיע ליעד ב ".decode("utf-8"),
             "en": " and arriving to destination at "}
DONE_SEND_LOC = {"1": "Done! now send me your location, and I'll get you home.",
                 "2": "יופי! עכשיו שלח/י לי את המיקום הנוכחי שלך"}
DONE_SET_HOME = {"1": "Done! now set your home:\nset home <your home>.",
                 "2": "יופי! עכשיו שלח/י לי את הכתובת שלך כך:\nset home <your_home>"}
SEND_LOC = {"1": "Please send your current location",
            "2": "שלח/י לי את המיקום הנוכחי שלך"}
SET_LANG_FIRST = "Please set your language first.\nsend: 'set lang <number>\n1. English\n2. Hebrew"
DONE_LANG = {"1": "Set English. Now send your location",
             "2": "נקבעה עברית. עכשיו שלח/י מיקום"}