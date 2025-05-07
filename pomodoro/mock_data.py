
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
