import json
from pathlib import Path
import os

PROJECT_ROOT = Path(__file__).resolve().parent.parent
SETTINGS_FILE = PROJECT_ROOT / "data" / "user_settings.json"


def save_user_settings(setting_dict):
    SETTINGS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_FILE,"w") as f:
        json.dump(setting_dict, f)

def load_user_settings():
    if SETTINGS_FILE.exists():
        with open(SETTINGS_FILE) as f:
            return json.load(f)
    return {}

def read_json_file(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {}

def write_json_file(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
