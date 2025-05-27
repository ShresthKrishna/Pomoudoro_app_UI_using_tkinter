import json
from pathlib import Path
from typing import List, Dict, Optional

# Paths and helpers
PROJECT_ROOT = Path(__file__).resolve().parents[1]
USER_TASK_FILE = PROJECT_ROOT / "data" / "user_tasks.json"


def _load_all() -> List[Dict]:
    USER_TASK_FILE.parent.mkdir(parents=True, exist_ok=True)
    if not USER_TASK_FILE.exists():
        return []
    with USER_TASK_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)


def _save_all(all_tasks: List[Dict]):
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
                if sub["completed"] < sub["goal"]:
                    sub["completed"] += 1
                    _save_all(all_tasks)
                    return sub["name"]
    return None


def reset_subtasks(task_name: str):
    all_tasks = _load_all()
    for entry in all_tasks:
        if entry["task"] == task_name:
            for sub in entry.get("subtasks", []):
                sub["completed"] = 0
            _save_all(all_tasks)
            return


def add_subtask(task_name: str, name: str, goal: int):
    name = name.strip()
    if not name:
        raise ValueError("Subtask name cannot be empty.")
    if goal <= 0:
        raise ValueError("Goal must be greater than or equal to 1.")
    all_tasks = _load_all()
    for entry in all_tasks:
        if entry["task"] == task_name:
            subtasks = entry.setdefault("subtasks", [])
            if any(s["name"].lower() == name.lower() for s in subtasks):
                raise ValueError("Duplicate subtask name.")
            subtasks.append({"name": name, "goal": goal, "completed": 0})
            _save_all(all_tasks)
            return
    all_tasks.append({"task": task_name,
    "subtasks": [{"name": name, "goal": goal, "completed": 0}]})
    _save_all(all_tasks)


def delete_subtask(task_name: str, subtask_name: str):
    all_tasks = _load_all()
    for entry in all_tasks:
        if entry["task"] == task_name:
            new_list = [s for s in entry.get("subtasks", []) if s["name"] != subtask_name]
            entry["subtasks"] = new_list
            _save_all(all_tasks)
            return


def edit_subtask(task_name: str, subtasks_name: str, new_goal: int):
    all_tasks = _load_all()
    for entry in all_tasks:
        if entry["task"]==task_name:
            for sub in entry.get("subtasks", []):
                if sub["name"] == subtasks_name:
                    sub["goal"] = max(sub["completed"], new_goal)
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
def get_total_subtask_goal(task_name: str) -> int:
    """
    Returns the total number of sessions planned across all subtasks for a task.
    """
    from pathlib import Path
    import json

    USER_TASK_FILE = Path(__file__).resolve().parents[1] / "data" / "user_tasks.json"
    if not USER_TASK_FILE.exists():
        return 0

    with open(USER_TASK_FILE, "r", encoding="utf-8") as f:
        all_tasks = json.load(f)

    for entry in all_tasks:
        if entry["task"] == task_name:
            return sum(sub.get("goal", 0) for sub in entry.get("subtasks", []))
    return 0


def sync_task_goal_if_needed(task_var, task_name: str):
    """
    Updates the task session goal (task_var) if subtasks total more than current value.
    Does NOT decrease it if subtasks reduce.
    """
    total_subtask_goal = get_total_subtask_goal(task_name)
    try:
        current_goal = int(task_var.get())
    except:
        current_goal = 0

    if total_subtask_goal > current_goal:
        task_var.set(total_subtask_goal)
        print(f"[DEBUG] Task goal updated to match subtasks: {total_subtask_goal}")
