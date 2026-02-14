import json
from pathlib import Path

CURRENT_DIR = Path(__file__).parent
ROOT_DIR = CURRENT_DIR.parent.parent
STORAGE_DIR = ROOT_DIR / "storage"

GROUPS_FILE = STORAGE_DIR / "groups.json"
PAO_FILE = STORAGE_DIR / "pao.json"


def load_groups():
    if not GROUPS_FILE.exists():
        return {}
    try:
        with open(GROUPS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Błąd ładowania groups.json: {e}")
        return {}

def load_pao():
    if not PAO_FILE.exists():
        return {}
    try:
        with open(PAO_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Błąd ładowania pao.json: {e}")
        return {}

def save_groups(data):
    try:
        with open(GROUPS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Błąd zapisu JSON: {e}")

def save_pao(data):
    try:
        with open(PAO_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Błąd zapisu JSON: {e}")
