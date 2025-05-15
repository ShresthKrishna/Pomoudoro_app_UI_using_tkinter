import pandas as pd
from datetime import datetime, timedelta

def get_mock_summary_data():
    today = datetime.now().date()
    dates = [today - timedelta(days=i) for i in reversed(range(7))]

    # Sessions per Day (bar)
    per_day = pd.DataFrame({
        "date": dates,
        "count": [2, 3, 1, 4, 2, 0, 3]
    })

    # Session Type Breakdown (pie)
    per_type = pd.DataFrame({
        "type": ["Work", "Short Break", "Long Break"],
        "total_minutes": [125, 25, 15]
    })

    # Streak Data
    streaks = {
        "current_streak": 3,
        "longest_streak": 7
    }

    # Recent Session Counts by Type per Day (for stacked chart)
    recent = pd.DataFrame({
        "date": dates * 3,
        "type": (
                ["Work"] * 7 +
                ["Short Break"] * 7 +
                ["Long Break"] * 7
        ),
        "count": (
                [1, 1, 1, 2, 1, 0, 1] +  # Work
                [1, 0, 1, 2, 1, 0, 1] +  # Short Break
                [0, 1, 0, 1, 1, 0, 0]  # Long Break
        )
    })

    # Derived: daily_by_type (pivoted line chart input)
    daily_by_type = recent.pivot(index="date", columns="type", values="count").fillna(0).reset_index()

    # Per-Task Time (bar)
    per_task_time = [
        {"task": "Write Report", "total_minutes": 75},
        {"task": "Debug UI", "total_minutes": 45},
        {"task": "Email Review", "total_minutes": 30},
        {"task": "Refactor Code", "total_minutes": 20},
    ]

    # Task Frequency (pie)
    task_frequency = [
        {"task": "Write Report", "count": 3},
        {"task": "Debug UI", "count": 2},
        {"task": "Email Review", "count": 1},
        {"task": "Refactor Code", "count": 1},
    ]

    return {
        "per_day": per_day,
        "per_type": per_type,
        "streaks": streaks,
        "recent": recent,
        "daily_by_type": daily_by_type,
        "per_task_time": per_task_time,
        "task_frequency": task_frequency
    }

def get_mock_session_rows():
    return [
        {"session_number": 1, "type": "Work", "completed_at": "2025-05-01 10:30", "duration_minutes": 25, "task": "Write Report"},
        {"session_number": 2, "type": "Short Break", "completed_at": "2025-05-01 10:55", "duration_minutes": 5, "task": ""},
        {"session_number": 3, "type": "Work", "completed_at": "2025-05-01 11:00", "duration_minutes": 25, "task": "Debug UI"},
        {"session_number": 4, "type": "Long Break", "completed_at": "2025-05-01 11:30", "duration_minutes": 15, "task": ""},
        {"session_number": 5, "type": "Work", "completed_at": "2025-05-02 09:00", "duration_minutes": 25, "task": "Email Review"},
        {"session_number": 6, "type": "Work", "completed_at": "2025-05-02 10:00", "duration_minutes": 20, "task": "Refactor Code"},
        {"session_number": 7, "type": "Work", "completed_at": "2025-05-03 08:30", "duration_minutes": 25, "task": "Write Report"},
    ]
