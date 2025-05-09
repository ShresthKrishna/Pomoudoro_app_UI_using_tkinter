
import pandas as pd
from datetime import datetime, timedelta

def get_mock_summary_data():
    today = datetime.now().date()
    dates = [today - timedelta(days=i) for i in reversed(range(7))]

    per_day = pd.DataFrame({
        "date": dates,
        "count": [2, 3, 1, 4, 2, 0, 3]
    })

    per_type = pd.DataFrame({
        "type": ["Work", "Short Break", "Long Break"],
        "total_minutes": [125, 25, 15]
    })

    streaks = {
        "current_streak": 3,
        "longest_streak": 7
    }

    recent = pd.DataFrame({
        "date": dates * 2,
        "type": ["Work"] * 7 + ["Short Break"] * 7,
        "count": [1, 1, 1, 2, 1, 0, 1, 1, 0, 1, 2, 1, 0, 1]
    })

    return {
        "per_day": per_day,
        "per_type": per_type,
        "streaks": streaks,
        "recent": recent
    }
def get_mock_session_rows():
    return [
        {"session_number": 1, "type": "Work", "completed_at": "2025-05-01 10:30", "duration_minutes": 25, "task": "Write Report"},
        {"session_number": 2, "type": "Short Break", "completed_at": "2025-05-01 10:55", "duration_minutes": 5, "task": ""},
        {"session_number": 3, "type": "Work", "completed_at": "2025-05-01 11:00", "duration_minutes": 25, "task": "Debug UI"},
        {"session_number": 4, "type": "Long Break", "completed_at": "2025-05-01 11:30", "duration_minutes": 15, "task": ""},
        {"session_number": 5, "type": "Work", "completed_at": "2025-05-02 09:00", "duration_minutes": 25, "task": "Email Review"},
    ]