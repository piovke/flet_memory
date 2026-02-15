import json

GROUPS_KEY = "memory_groups_v1"
PAO_KEY = "memory_pao_v1"

def load_data(page, key):
    """
    Uniwersalna funkcja ładowania danych.
    Próbuje pobrać z:
    1. Bazy telefonu/przeglądarki (Client Storage)
    2. Pliku lokalnego JSON (Komputer)
    """

    # 1. Próba: Client Storage (Telefon/Web)
    try:
        # Sprawdzamy czy page ma ten atrybut (hasattr) i czy nie jest None
        if hasattr(page, 'client_storage') and page.client_storage:
            if page.client_storage.contains_key(key):
                return page.client_storage.get(key)
    except Exception as e:
        print(f"Info: Client storage niedostępne ({e})")

    # 2. Próba: Plik lokalny (PC)
    # To zadziała na Windowsie, gdzie client_storage robi problemy
    try:
        filename = f"{key}.json"
        if os.path.exists(filename):
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception:
        pass

    # Jeśli nic nie znaleziono, zwracamy pusty słownik
    return {}


def save_data(page, key, data):
    """
    Uniwersalna funkcja zapisywania danych.
    """

    # 1. Zapis: Client Storage (Telefon/Web)
    try:
        if hasattr(page, 'client_storage') and page.client_storage:
            page.client_storage.set(key, data)
    except Exception:
        pass

    # 2. Zapis: Plik lokalny (PC - Kopia zapasowa)
    try:
        filename = f"{key}.json"
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception:
        pass