# engine/manager/logger.py

from datetime import date, datetime
from pomodoro.logger import log_session as base_log_session
from utils.storage import read_json_file, write_json_file

DAILY_LOG_PATH = "E:/Github Projects/Pomodoro/data/daily_focus_log.json"

def log_session_data(
    session_type,
    start_time,
    end_time,
    duration_minutes,
    task,
    subtask=None,
    resumed=False,
    interrupted=False,
    completed=False,
    focus_rating=None,
    intent_fulfilled=None,
    session_number=None,
):
    base_log_session(
        session_type=session_type,
        start_time=start_time,
        end_time=end_time,
        duration_minutes=duration_minutes,
        task=task,
        subtask=subtask,
        resumed=resumed,
        interrupted=interrupted,
        completed=completed,
        focus_rating=focus_rating,
        intent_fulfilled=intent_fulfilled,
        session_number=session_number,
    )


def log_daily_focus_summary(focus_minutes: float, focus_sessions: int):
    today_str = date.today().isoformat()
    try:
        existing_data = read_json_file(DAILY_LOG_PATH)
    except Exception:
        existing_data = {}

    if today_str not in existing_data:
        existing_data[today_str] = {
            "total_focus_minutes": 0,
            "sessions": 0
        }

    existing_data[today_str]["total_focus_minutes"] += round(focus_minutes, 2)
    existing_data[today_str]["sessions"] += focus_sessions

    write_json_file(DAILY_LOG_PATH, existing_data)
