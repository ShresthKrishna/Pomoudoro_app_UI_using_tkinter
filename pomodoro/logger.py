from pathlib import Path
import csv
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = PROJECT_ROOT / "data" / "session_trial.csv"

# New schema columns (strict order)
FIELDNAMES = [
    "session_type", "start_time", "end_time", "duration_minutes",
    "task", "subtask", "completed", "resumed",
    "focus_rating", "intent_fulfilled", "interrupted"
]

def _get_next_session_number(session_type: str) -> int:
    if not LOG_FILE.exists():
        return 1

    with LOG_FILE.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if "session_number" not in reader.fieldnames:
            print("[DEBUG] session_number column missing — returning 1")
            return 1

        session_numbers = [
            int(row["session_number"])
            for row in reader
            if row["session_type"] == session_type and row["session_number"].isdigit()
        ]
    return max(session_numbers, default=0) + 1


def log_session(
    session_type,
    start_time,
    end_time,
    duration_minutes,
    task="",
    subtask=None,
    focus_rating=None,
    intent_fulfilled=None,
    resumed=False,
    interrupted=False,
    completed=False,
    session_number=None
):
    if session_number is None:
        session_number = _get_next_session_number(session_type)

    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    write_header = not LOG_FILE.exists() or LOG_FILE.stat().st_size == 0

    row = {
        "session_type": session_type,
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S") if start_time else "",
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S"),
        "duration_minutes": duration_minutes,
        "task": task or "",
        "subtask": subtask or "",
        "completed": int(bool(completed)),
        "resumed": int(bool(resumed)),
        "focus_rating": focus_rating if focus_rating is not None else "",
        "intent_fulfilled": intent_fulfilled or "",
        "interrupted": int(bool(interrupted))
    }

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)

        if write_header:
            writer.writeheader()

        writer.writerow(row)
