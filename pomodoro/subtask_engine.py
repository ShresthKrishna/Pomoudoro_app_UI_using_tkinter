import json
from pathlib import Path
from typing import List, Dict, Optional

PROJECT_ROOT = Path(__file__).resolve().parents[1]
USER_TASK_FILE = PROJECT_ROOT / "data" / "user_tasks.json"
print("[DEBUG] USER_TASK_FILE is:", USER_TASK_FILE.resolve())
def _load_all() -> List[Dict]:
    USER_TASK_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not USER_TASK_FILE.exists():
        return []
    with USER_TASK_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def _save_all(all_tasks: List[Dict]):
    print("[DEBUG] Writing to", USER_TASK_FILE)
    print("[DEBUG] Data:", all_tasks)
    with USER_TASK_FILE.open("w", encoding="utf-8") as f:
        json.dump(all_tasks, f, indent=2)


def get_subtasks(task_name: str) -> List[Dict]:
    for entry in _load_all():
        if entry["task"] == task_name:
            return entry.get("subtasks", [])
    return []

def get_active_subtask(task_name: str) -> List[Dict]:
    for entry in _load_all():
        if entry["task"] == task_name:
            return entry.get("subtasks", [])
    return []

def mark_subtask_progress(task_name: str) -> Optional[Dict]:
    all_tasks = _load_all()
    for entry in all_tasks:
        if entry["task"]==task_name:
            for sub in entry.get("subtasks", []):
                if sub["conpleted"] < sub["goal"]:
                    sub["completed"] += 1
                    _save_all(all_tasks)
                    return sub
    return None

def reset_subtasks(task_name: str):
    all_tasks = _load_all()
    for entry in all_tasks:
        if entry["task"] == task_name:
            for sub in entry.get("subtasks", []):
                sub["completed"] = 0
            _save_all(all_tasks)
            return

def add_or_update_task(task_name: str, subtasks: List[Dict]):
    all_tasks = _load_all()
    for entry in all_tasks:
        if entry["task"] == task_name:
            entry["subtasks"] = subtasks
            _save_all(all_tasks)
            return
    all_tasks.append({"task": task_name, "subtasks": subtasks})
    _save_all(all_tasks)
