from pathlib import Path
import json
from datetime import datetime

TASK_FILE = Path("data/user_tasks.json")
MAX_TASKS = 50

def load_task_dict():
    if not TASK_FILE.exists():
        return {}
    try:
        with TASK_FILE.open("r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If file is empty or corrupted, return empty dict
        return {}


def save_task_dict(task_dict):
    sorted_tasks = dict(sorted(task_dict.items(), key=lambda item: item[1]["last_used"], reverse=True)[:MAX_TASKS])
    TASK_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(TASK_FILE, "w", encoding="utf-8") as f:
        json.dump(sorted_tasks, f, indent=2)

def update_task_memory(task_name):
    task_dict = load_task_dict()
    today = datetime.today().strftime("%Y-%m-%d")
    if task_name in task_dict:
        task_dict[task_name]["count"]+=1
        task_dict[task_name]["last_used"] = today
    else:
        task_dict[task_name] = {"count": 1, "last_used": today}
    save_task_dict(task_dict)

def get_all_tasks():
    return list(load_task_dict().keys())