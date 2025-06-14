import tkinter as tk
from datetime import datetime
from pomodoro.timer_engine import TimerEngine
from engine.manager import logger, state, subtasks, router, reflection

class SessionManager:
    def __init__(self, root):
        self.root = root
        self.frames = {}
        self.session_type_var = tk.StringVar(value="Work")
        self.task_var = tk.StringVar()
        self.task_session_goal = tk.IntVar(value=1)
        self.session_counts = {"Work": 0, "Short Break": 0, "Long Break": 0}
        self.work_session_completed = 0
        self.session_start_time = None
        self.is_paused = False
        self.has_prompted_intent = False
        self.was_resumed = False
        self.was_interrupted = False
        self.daily_focus_minutes = 0.0
        self.focus_sessions_today = 0

        self.set_start_button_state = lambda state: None
        self.timer_label = None
        self.session_label = None

        self._tick_loop_id = None
        self._tick_loop_running = False

        self.duration_vars = {
            "Work": tk.IntVar(value=25),
            "Short Break": tk.IntVar(value = 5),
            "Long Break": tk.IntVar(value=15)
        }
        self._load_durations()

        self.timer_engine = TimerEngine(
            self.update_display_cb,
            self.session_complete_cb,
            {k: self.duration_vars[k].get()*60 for k in self.duration_vars}
        )

    # ---------------------------------------------------
    #                       UI Wiring
    #----------------------------------------------------
    def register_screens(self, frame_dict):
        pass

    def show_frames(self, name):
        pass

    def _load_durations(self):
        from utils.storage import load_user_settings

        saved = load_user_settings()
        for types  in self.duration_vars:
            if types in saved:
                self.duration_vars[types].set(saved[types])

    # ---------------------------------------------------
    #                       UI Label
    # ----------------------------------------------------

    def update_display_cb(self, mins, secs):
        if self.timer_label:
            self.timer_label.config(text=f"{mins:20d}:{secs:02d}")


    def update_session_info(self):
        pass

    def set_subtask_editable(self, editable=True):
        pass

    # ---------------------------------------------------
    #                       Settings
    # ----------------------------------------------------
    def save_settings(self):
        from utils.storage import save_user_settings
        durations = {k: self.duration_vars[k].get() for k in self.duration_vars}
        save_user_settings(durations)
        self.timer_engine.update_durations({k: v*60 for k,v in durations.items()})