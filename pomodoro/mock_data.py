import pandas as pd
import random
from pathlib import Path
from faker import Faker
from datetime import datetime, timedelta

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MOCK_DATA_FILE = PROJECT_ROOT / "data" / "mock_data.csv"
Faker.seed(123)
fake = Faker()

def generate_and_save_mock_data(n_days=130, max_sessions_per_day=10):
    tasks = [
        "Write Report", "Debug UI", "Design Slides", "Read Docs",
        "Email Review", "Database Cleanup", "Refactor Code", "Code Review",
        "Client Call", "Test Features", "Brainstorm Ideas"
    ]
    session_types = ["Work", "Short Break", "Long Break"]
    rows = []

    # === 1. Generate sessions across last `n_days` ===
    for i in range(n_days):
        date = datetime.now().date() - timedelta(days=i)
        sessions_today = random.randint(5, max_sessions_per_day)
        for j in range(sessions_today):
            session_type = random.choices(session_types, weights=[0.6, 0.3, 0.1])[0]
            task = random.choice(tasks) if session_type == "Work" else ""
            duration = {
                "Work": random.randint(25, 45),
                "Short Break": random.randint(4, 7),
                "Long Break": random.randint(10, 20)
            }[session_type]
            completed_at = datetime.combine(date, datetime.min.time()) + timedelta(minutes=random.randint(0, 1439))

            rows.append({
                "type": session_type,
                "completed_at": completed_at.strftime("%Y-%m-%d %H:%M:%S"),
                "session_number": j + 1,
                "duration_minutes": duration,
                "task": task
            })

    # === 2. Guarantee 2–3 active days in last 7 (for analytics dashboard) ===
    recent_days = [datetime.now().date() - timedelta(days=i) for i in range(2)]
    for date in recent_days:
        for j in range(random.randint(4, 7)):  # 4–7 sessions
            session_type = random.choices(session_types, weights=[0.6, 0.3, 0.1])[0]
            task = random.choice(tasks) if session_type == "Work" else ""
            duration = {
                "Work": random.randint(25, 45),
                "Short Break": random.randint(4, 7),
                "Long Break": random.randint(10, 20)
            }[session_type]
            completed_at = datetime.combine(date, datetime.min.time()) + timedelta(minutes=random.randint(0, 1439))
            rows.append({
                "type": session_type,
                "completed_at": completed_at.strftime("%Y-%m-%d %H:%M:%S"),
                "session_number": j + 1,
                "duration_minutes": duration,
                "task": task
            })

    df = pd.DataFrame(rows)
    MOCK_DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(MOCK_DATA_FILE, index=False)
    print(f"[DEBUG] Mock dataset created with {len(df)} rows across {n_days} days.")
    return df


def get_mock_session_rows():
    if not MOCK_DATA_FILE.exists():
        df = generate_and_save_mock_data()
    else:
        df = pd.read_csv(MOCK_DATA_FILE)

    return df.to_dict(orient="records")
def get_mock_summary_data():
    if not MOCK_DATA_FILE.exists():
        generate_and_save_mock_data()
    df = pd.read_csv(MOCK_DATA_FILE)
    df["completed_at"] = pd.to_datetime(df["completed_at"])
    df["date"] = df["completed_at"].dt.date

    per_day = df.groupby("date").size().reset_index(name="count")
    per_type = df.groupby("type")["duration_minutes"].sum().reset_index(name="total_minutes")

    streaks = {
        "current_streak": 5,
        "longest_streak": 12
    }

    recent = df[df["completed_at"] >= datetime.now() - timedelta(days=7)]
    recent_summary = recent.groupby(["date", "type"]).size().reset_index(name="count")

    per_task_time = (
        df[df["task"] != ""]
        .groupby("task")["duration_minutes"]
        .sum()
        .reset_index(name="total_minutes")
        .to_dict(orient="records")
    )

    task_frequency = (
        df[df["task"] != ""]
        .groupby("task")
        .size()
        .reset_index(name="count")
        .to_dict(orient="records")
    )

    return {
        "per_day": per_day,
        "per_type": per_type,
        "streaks": streaks,
        "recent": recent_summary,
        "daily_by_type": recent_summary,
        "per_task_time": per_task_time,
        "task_frequency": task_frequency,
        "raw_sessions": df.to_dict(orient="records")
    }