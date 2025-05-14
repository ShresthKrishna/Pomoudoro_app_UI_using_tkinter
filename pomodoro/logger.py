from pathlib import Path
import csv

LOG_FILE = Path("data") / "session.csv"

def log_session(session_type, completed_at, session_number, duration_minutes, task=""):
    # Ensure data directory exists
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Check if file exists *and* has content
    write_header = True
    if LOG_FILE.exists() and LOG_FILE.stat().st_size > 0:
        write_header = False

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["type", "completed_at", "session_number", "duration_minutes", "task"]
        )
        if write_header:
            writer.writeheader()
        writer.writerow({
            "type": session_type,
            "completed_at": completed_at.strftime("%Y-%m-%d %H:%M:%S"),
            "session_number": session_number,
            "duration_minutes": duration_minutes,
            "task": task
        })
