import json
import os

GROUPS_KEY = "groups"
PAO_KEY = "pao"
BIRTHDAY_KEY = "birthdays"

# funkcje próbują  client_storage(android) i  json (windows)

def load_data(page, key):
    try:
        if hasattr(page, 'client_storage') and page.client_storage:
            if page.client_storage.contains_key(key):
                return page.client_storage.get(key)
    except Exception as e:
        print(f"Info: Client storage niedostępne ({e})")
    try:
        filename = f"{key}.json"
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass
    return {}


def save_data(page, key, data):
    try:
        if hasattr(page, 'client_storage') and page.client_storage:
            page.client_storage.set(key, data)
    except Exception:
        pass
    try:
        filename = f"{key}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception:
        pass