import pandas as pd
from datetime import datetime, timedelta


def get_mock_summary_data():
    today = datetime.now().date()
    dates = [today - timedelta(days=i) for i in reversed(range(7))]

    # Daily session count
    per_day = pd.DataFrame({
        "date": dates,
        "count": [2, 3, 1, 4, 2, 0, 3]
    })

    # Time spent per session type
    per_type = pd.DataFrame({
        "type": ["Work", "Short Break", "Long Break"],
        "total_minutes": [125, 25, 15]
    })

    # Active streaks
    streaks = {
        "current_streak": 3,
        "longest_streak": 7
    }

    # Activity by session type across recent days
    recent = pd.DataFrame({
        "date": dates * 2,
        "type": ["Work"] * 7 + ["Short Break"] * 7,
        "count": [1, 1, 1, 2, 1, 0, 1, 1, 0, 1, 2, 1, 0, 1]
    })

    # Time spent per task
    per_task_time = [
        {"task": "Write Report", "total_minutes": 75},
        {"task": "Debug UI", "total_minutes": 45},
        {"task": "Email Review", "total_minutes": 30},
        {"task": "Refactor Code", "total_minutes": 20},
    ]

    # Task frequency (count of Work sessions)
    task_frequency = [
        {"task": "Write Report", "count": 3},
        {"task": "Debug UI", "count": 2},
        {"task": "Email Review", "count": 1},
        {"task": "Refactor Code", "count": 1},
    ]

    # daily_by_type pivot for line chart
    daily_by_type = recent.pivot(index="date", columns="type", values="count").fillna(0).reset_index()

    # Raw sessions — used for line chart filtering
    raw_sessions = get_mock_session_rows()

    return {
        "per_day": per_day,
        "per_type": per_type,
        "streaks": streaks,
        "recent": recent,
        "per_task_time": per_task_time,
        "task_frequency": task_frequency,
        "daily_by_type": daily_by_type,
        "raw_sessions": raw_sessions
    }


def get_mock_session_rows():
    base_time = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
    mock_rows = []
    tasks = ["Write Report", "Debug UI", "Email Review", "Refactor Code"]
    for i in range(7):  # 7 days
        day = base_time - timedelta(days=i)
        for j in range(i % 3 + 1):  # 1–3 sessions per day
            session_type = "Work"
            task = tasks[(i + j) % len(tasks)]
            duration = 25
            timestamp = day + timedelta(minutes=j * 30)
            mock_rows.append({
                "type": session_type,
                "completed_at": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "session_number": j + 1,
                "duration_minutes": duration,
                "task": task
            })
    return mock_rows
