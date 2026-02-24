import json
import os

GROUPS_KEY = "groups"
PAO_KEY = "pao"
BIRTHDAY_KEY = "birthdays"
SETTINGS_KEY = "settings"

# if word doesnt exists adds it
def add_pao(page, digit_pair, pao, text):
    if not digit_pair or len(digit_pair)!=2:
        return None

    data = load_data(page, PAO_KEY)

    if digit_pair not in data:
        data[digit_pair] = {"P": [], "A": [], "O": []}

    if text not in data[digit_pair][pao] and text != "":
        data[digit_pair][pao].append(text)
        save_data(page, PAO_KEY, data)

def delete_pao(page, digit_pair, pao, word_to_delete):
    if not digit_pair or len(digit_pair)!=2:
        return

    data = load_data(page, PAO_KEY)

    if digit_pair not in data:
        return

    category_list = data[digit_pair].get(pao, [])
    if word_to_delete in category_list:
        category_list.remove(word_to_delete)
        data[digit_pair][pao] = category_list
        save_data(page, PAO_KEY, data)


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


def get_pao_suggestions(page, digit_pair, pao):
    if not digit_pair or len(digit_pair)!=2:
        return []

    data = load_data(page, PAO_KEY)

    if digit_pair not in data:
        return []

    words_list = data[digit_pair].get(pao, [])
    return words_list
