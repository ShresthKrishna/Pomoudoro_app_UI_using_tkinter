from pathlib import Path
import json
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TASK_FILE = Path(PROJECT_ROOT)/"data"/"tasks.json"
MAX_TASKS = 50

def load_task_dict():
    if not TASK_FILE.exists():
        return {}
    with TASK_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)                   # ← return the loaded dict

def save_task_dict(task_dict):
    # sort by last_used desc, then truncate to MAX_TASKS entries
    items = sorted(
        task_dict.items(),
        key=lambda x: x[1]["last_used"],
        reverse=True
    )[:MAX_TASKS]
    sorted_tasks = dict(items)

    TASK_FILE.parent.mkdir(parents=True, exist_ok=True)
    with TASK_FILE.open("w", encoding="utf-8") as f:
        json.dump(sorted_tasks, f, indent=2)

def update_task_memory(task_name):
    tasks = load_task_dict()
    today = datetime.today().strftime("%Y-%m-%d")
    if task_name in tasks:
        tasks[task_name]["count"] += 1
        tasks[task_name]["last_used"] = today
    else:
        tasks[task_name] = {"count": 1, "last_used": today}
    save_task_dict(tasks)

def get_all_tasks():
    return list(load_task_dict().keys())
