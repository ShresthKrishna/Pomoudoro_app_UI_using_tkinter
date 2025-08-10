# engine/manager/session_settings.py
from datetime import date

from utils.storage import load_user_settings, save_user_settings, read_json_file, write_json_file
import tkinter as tk

class SessionSettings:
    def __init__(self):
        # Duration settings
        self.duration_vars = {
            "Work": tk.IntVar(value=25),
            "Short Break": tk.IntVar(value=5),
            "Long Break": tk.IntVar(value=15)
        }
        saved = load_user_settings()
        for k in self.duration_vars:
            if k in saved:
                self.duration_vars[k].set(saved[k])
        self.auto_session_switch =True

    def save_settings(self):
        save_user_settings({k: self.duration_vars[k].get() for k in self.duration_vars})
        self.timer_engine.update_durations({
            k: self.duration_vars[k].get() * 60 for k in self.duration_vars
        })

    def log_daily_focus_summary(self):
        today_str = date.today().isoformat()
        log_path = "E:/Github Projects/Pomodoro/data/daily_focus_log.json"

        try:
            existing_data = read_json_file(log_path)
        except Exception:
            existing_data = {}

        if today_str not in existing_data:
            existing_data[today_str] = {
                "total_focus_minutes": 0,
                "sessions": 0
            }

        existing_data[today_str]["total_focus_minutes"] += round(self.daily_focus_minutes, 2)
        existing_data[today_str]["sessions"] += self.focus_sessions_today

        write_json_file(log_path, existing_data)
