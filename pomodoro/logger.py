from pathlib import Path
import csv

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = PROJECT_ROOT / "data" / "session3.csv"

def log_session(
    session_type,
    completed_at,
    session_number,
    duration_minutes,
    task="",
    completed=True,
    subtask=None,
    focus_rating=None,
    intent_fulfilled=None,
    resumed=False,
    interrupted=False
):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    write_header = not LOG_FILE.exists() or LOG_FILE.stat().st_size == 0

    fieldnames = [
        "type", "completed_at", "session_number", "duration_minutes",
        "task", "subtask", "focus_rating", "intent_fulfilled",
        "resumed", "interrupted", "completed"
    ]

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        if write_header:
            writer.writeheader()

        writer.writerow({
            "type": session_type,
            "completed_at": completed_at.strftime("%Y-%m-%d %H:%M:%S"),
            "session_number": session_number,
            "duration_minutes": duration_minutes,
            "task": task or "",
            "subtask": subtask or "",
            "focus_rating": focus_rating if focus_rating is not None else "",
            "intent_fulfilled": intent_fulfilled or "",
            "resumed": int(resumed),
            "interrupted": int(interrupted),
            "completed": int(completed)
        })
