import json
import os
from datetime import datetime


FILE = "chat_history.json"


def load_history():

    if not os.path.exists(FILE):
        return {}

    with open(FILE, "r", encoding="utf-8") as f:
        return json.load(f)



def save_chat(chat_id, messages):

    history = load_history()

    history[chat_id] = {
        "time": str(datetime.now()),
        "messages": messages
    }

    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)



def get_chats():

    return load_history()