from pathlib import Path
import csv
import os

PROJECT_ROOT = Path(__file__).resolve().parent.parent
LOG_FILE = PROJECT_ROOT / "data" / "session.csv"

def log_session(session_type, completed_at, session_number, duration_minutes, task="", completed=True):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    write_header = not LOG_FILE.exists() or LOG_FILE.stat().st_size == 0

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["type", "completed_at", "session_number", "duration_minutes", "task", "completed"]
        )
        if write_header:
            writer.writeheader()
        writer.writerow({
            "type": session_type,
            "completed_at": completed_at.strftime("%Y-%m-%d %H:%M:%S"),
            "session_number": session_number,
            "duration_minutes": duration_minutes,
            "task": task,
            "completed": int(completed)
        })
        print("[DEBUG] Written to:", LOG_FILE.resolve())
