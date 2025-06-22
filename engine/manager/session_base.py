# engine/manager/session_base.py

import tkinter as tk
from datetime import datetime, date
from tkinter import messagebox
from pomodoro.task_memory import get_all_tasks, update_task_memory
from pomodoro.theme import theme

class SessionBase:
    def __init__(self, root):
        self.root = root
        self.frames = {}

        # UI state variables
        self.session_type_var = tk.StringVar(value="Work")
        self.task_var = tk.StringVar()
        self.task_session_goal = tk.IntVar(value=1)
        self.session_counts = {"Work": 0, "Short Break": 0, "Long Break": 0}
        self.work_sessions_completed = 0
        self.session_start_time = None
        self.is_paused = False
        self.set_start_button_state = lambda state: None
        self._tick_loop_id = None
        self._tick_loop_running = False
        self.has_prompted_intent = False
        self.last_focus_rating = None
        self.last_intent_fulfilled = None
        self.was_resumed = False
        self.was_interrupted = False
        self.daily_focus_minutes = 0.0
        self.focus_sessions_today = 0

        self.all_tasks = get_all_tasks()
        self.timer_label = None
        self.session_label = None

    def register_screens(self, frames_dict):
        self.frames = frames_dict

    def show_frame(self, name):
        self.frames[name].tkraise()

    def get_active_task(self) -> str:
        return self.task_var.get().strip()
