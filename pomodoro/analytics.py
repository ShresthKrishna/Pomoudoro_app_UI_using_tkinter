import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from pomodoro.mock_data import get_mock_summary_data, get_mock_session_rows
from typing import List, Dict, Union


DEFAULT_LOG_PATH = Path('data') / 'session.csv'


def read_sessions(filepath=DEFAULT_LOG_PATH) -> pd.DataFrame:
    path = Path(filepath)
    if not path.exists() or path.stat().st_size == 0:
        return pd.DataFrame(columns=["type", "completed_at", "session_number", "duration_minutes"])

    df = pd.read_csv(path)
    expected_columns = ["type", "completed_at", "session_number", "duration_minutes"]
    missing = set(expected_columns) - set(df.columns)
    if missing:
        print(f"[analytics.py] Warning: Missing expected columns in CSV: {missing}")
        return pd.DataFrame(columns=expected_columns)

    df = df.dropna(subset=["type", "completed_at"])
    df["completed_at"] = pd.to_datetime(df["completed_at"], errors="coerce")
    df = df.dropna(subset=["completed_at"])
    df["date"] = df["completed_at"].dt.date
    return df


def count_sessions_per_day(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["date", "count"])
    result = df.groupby("date").size().reset_index(name="count")
    return result[["date", "count"]].sort_values("date")


def summarize_time_per_type(df: pd.DataFrame, fallback_minutes=25) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["type", "total_minutes"])

    if "duration_minutes" not in df.columns:
        print("[analytics.py] Warning: 'duration_minutes' missing. Using fallback.")
        df["duration_minutes"] = fallback_minutes

    result = df.groupby("type")["duration_minutes"].sum().reset_index(name="total_minutes")
    return result[["type", "total_minutes"]]


def get_streaks(df: pd.DataFrame) -> dict:
    if df.empty:
        return {"current_streak": 0, "longest_streak": 0}

    df = df.copy()
    df["date"] = df["completed_at"].dt.date
    active_days = sorted(df["date"].unique())

    # Longest streak
    longest = current = 1 if active_days else 0
    for i in range(1, len(active_days)):
        if (active_days[i] - active_days[i - 1]).days == 1:
            current += 1
            longest = max(longest, current)
        else:
            current = 1

    # Current streak
    today = datetime.now().date()
    streak = 0
    for i in reversed(range(len(active_days))):
        if (today - active_days[i]).days == streak:
            streak += 1
        else:
            break

    return {"current_streak": streak, "longest_streak": longest}


def summarize_recent_days(df: pd.DataFrame, n=7) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame(columns=["date", "type", "count"])

    cutoff = datetime.now() - timedelta(days=n)
    filtered = df[df["completed_at"] >= cutoff].copy()
    filtered["date"] = filtered["completed_at"].dt.date

    summary = filtered.groupby(["date", "type"]).size().reset_index(name="count")
    return summary[["date", "type", "count"]].sort_values("date")

def get_recent_sessions(n=20, use_mock=False) -> List[Dict[str, Union[str, int]]]:
    if use_mock:
        return get_mock_session_rows()[:n]
    df = read_sessions()
    if df.empty:
        return []
    df = df.copy()
    if "task" not in df.columns:
        df["task"] = ""

    df = df.sort_values("completed_at", ascending=False)
    return df.head(n).to_dict(orient="records")

def summarize_time_per_task(df: pd.DataFrame) -> dict:
    """
       Returns a list of dictionaries with total minutes per task for Work sessions.
       Example: [{"task": "Trial_1", "total_minutes": 90}, ...]
       """
    df  = df.copy()
    df = df[df["type"] == "Work"]
    df["task"] = df["task"].fillna("").replace("", "[No Task]")

    task_summary = df.groupby("task")["duration_minutes"].sum().reset_index()
    task_summary = task_summary.sort_values(by="duration_minutes", ascending=False)

    return task_summary.to_dict(orient="records")

def summarize_daily_by_type(df: pd.DataFrame) -> pd.DataFrame:
    # Pivot recent 7 days per session type
    recent = summarize_recent_days(df, n=7)
    pivot = recent.pivot(index="date", columns="type", values="count").fillna(0)
    return pivot.reset_index()

def summarize_daily_for_tasks(df: pd.DataFrame, tasks: List[str]) -> pd.DataFrame:
    """
    Return DataFrame indexed by date with one column per selected task,
    containing daily counts of Work sessions for each.
    """
    df = df[df["type"]=="Work"].copy()
    df["task"] = df["task"].fillna("[No Task]")
    df = df[df["task"].isin(tasks)]
    df["date"] = pd.to_datetime(df["completed_at"]).dt.date
    grp = df.groupby(["date","task"]).size().reset_index(name="count")
    pivot = grp.pivot(index="date", columns="task", values="count").fillna(0)
    # ensure all last 7 days are present
    all_dates = pd.date_range(end=datetime.now().date(), periods=7).date
    pivot = pivot.reindex(all_dates, fill_value=0)
    return pivot.reset_index().rename(columns={"index":"date"})


def count_sessions_per_task(df: pd.DataFrame) -> dict:
    """
    Returns a list of dictionaries with count of Work sessions per task.
    Example: [{"task": "Trial_1", "count": 4}, ...]
    """
    df = df.copy()
    df = df[df["type"] == "Work"]
    df["task"] = df["task"].fillna("").replace("", "[No Task]")

    task_counts = df.groupby("task").size().reset_index(name="count")
    task_counts = task_counts.sort_values(by="count", ascending=False)

    return task_counts.to_dict(orient="records")


def generate_all_summaries(df=None, use_mock=False):
    """
    Returns a dictionary of all summaries needed for analytics screen.
    If use_mock is True, loads static mock data from mock_data.py.
    """
    if use_mock:
        return get_mock_summary_data()

    if df is None:
        df = read_sessions()

    return {
        "per_day": count_sessions_per_day(df),
        "per_type": summarize_time_per_type(df),
        "streaks": get_streaks(df),
        "recent": summarize_recent_days(df),
        "per_task_time": summarize_time_per_task(df),
        "task_frequency": count_sessions_per_task(df),
        "daily_by_type": summarize_daily_by_type(df),
        "per_task_daily": summarize_time_per_task(df)
    }
