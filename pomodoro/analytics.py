import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

DEFAULT_LOG_PATH = Path('data/session.csv')

def read_session(filepath=DEFAULT_LOG_PATH) -> pd.DataFrame:
    if not filepath.exists() or filepath.stat().st_size==0:
        return pd.DataFrame(columns=["type", "completed_at", "session_number", "duration_minutes"])
    df = pd.read_csv(filepath)
    expected_columns = ["type", "completed_at", "session_number", "duration_minutes"]
    if expected_columns not in df.columns:
        return pd.DataFrame(columns=expected_columns)
    df.dropna(subset=["type", "completed_at"])
    pd.to_datetime(df["completed_at"], errors="coerce")
    df.dropna(subset=["completed_at"])
    df["date"] = df["completed_at"].dt.date
    return df


def get_total_sessions_per_day(df: pd.DataFrame) -> pd.DataFrame:
    pass

def summarize_time_per_type(df: pd.DataFrame) -> pd.DataFrame:
    pass

def get_streaks(df: pd.DataFrame) -> pd.DataFrame:
    pass

def summarize_recent_days(df: pd.DataFrame) -> pd.DataFrame:
    pass