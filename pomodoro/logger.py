from pathlib import Path
import csv

LOG_FILE = Path("data/session.csv")


def log_session(session_type, completed_at, session_number):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    file_exists = LOG_FILE.exists()

    with open(LOG_FILE, 'a', newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["type", "completed_at", "session_number"])
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "type": session_type,
                "completed_at": completed_at,
                "session_number": session_number
            }
        )