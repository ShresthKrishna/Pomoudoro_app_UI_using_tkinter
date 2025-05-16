import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from pomodoro.timer_engine import TimerEngine
from pomodoro.logger import log_session
from pomodoro.timer_state_manager import save_timer_state, load_timer_state, clear_timer_state
from pomodoro.task_memory import get_all_tasks, update_task_memory
from utils.storage import load_user_settings, save_user_settings
from pomodoro.theme import theme

class SessionManager:
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

        # Load persistent task memory list
        self.all_tasks = get_all_tasks()

        # Timer engine setup
        self.timer_engine = TimerEngine(
            self.update_display_cb,
            self.session_complete_cb,
            {k: self.duration_vars[k].get() * 60 for k in self.duration_vars}
        )

        # Placeholders for UI labels
        self.timer_label = None
        self.session_label = None

    def register_screens(self, frames_dict):
        self.frames = frames_dict

    def show_frame(self, name):
        self.frames[name].tkraise()

    def update_display_cb(self, mins, secs):
        if self.timer_label:
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")

    def session_complete_cb(self, prev_session, count):
        completed_at = datetime.now()
        duration = round((completed_at - self.session_start_time).total_seconds() / 60 if self.session_start_time else 0)
        self.session_counts[prev_session] += 1

        log_session(prev_session, completed_at, self.session_counts[prev_session], duration, task=self.task_var.get().strip())

        if prev_session == "Work":
            self.work_sessions_completed += 1
            next_session = "Long Break" if self.work_sessions_completed % 4 == 0 else "Short Break"
            if self.task_session_goal.get() <= 1:
                self.task_var.set("")
                self.task_session_goal.set(1)
            else:
                self.task_session_goal.set(self.task_session_goal.get() - 1)
        else:
            next_session = "Work"

        self.session_type_var.set(next_session)
        if self.session_label:
            self.session_label.config(text=f"{next_session} Session {self.session_counts[next_session] + 1}")

        clear_timer_state()
        self.session_start_time = datetime.now()
        self.timer_engine.start(next_session)

    def start_tick_loop(self):
        self.timer_engine.tick()
        self.root.after(10, self.start_tick_loop)

    def save_settings(self):
        save_user_settings({k: self.duration_vars[k].get() for k in self.duration_vars})
        self.timer_engine.update_durations({k: self.duration_vars[k].get() * 60 for k in self.duration_vars})

    def on_start(self):
        # Record start time
        self.session_start_time = datetime.now()
        # Persist task memory
        task_name = self.task_var.get().strip()
        if task_name:
            update_task_memory(task_name)
            self.all_tasks = get_all_tasks()

        session_type = self.session_type_var.get()
        self.timer_engine.update_durations({k: self.duration_vars[k].get() * 60 for k in self.duration_vars})
        self.timer_engine.start(session_type)
        save_timer_state({
            "active": True,
            "session_type": session_type,
            "remaining_seconds": self.timer_engine.remaining,
            "session_counts": self.session_counts,
            "task": task_name,
            "task_sessions_remaining": self.task_session_goal.get(),
            "timestamp": datetime.now().isoformat()
        })

    def toggle_pause(self, pause_button):
        save_timer_state({
            "active": True,
            "session_type": self.timer_engine.session_type,
            "remaining_seconds": self.timer_engine.remaining,
            "session_counts": self.session_counts,
            "task": self.task_var.get().strip(),
            "task_sessions_remaining": self.task_session_goal.get(),
            "timestamp": datetime.now().isoformat()
        })

        if self.is_paused:
            self.timer_engine.resume()
            pause_button.config(text="Pause")
        else:
            self.timer_engine.pause()
            pause_button.config(text="Resume")
        self.is_paused = not self.is_paused

    def reset_session(self):
        self.timer_engine.reset()
        for key in self.session_counts:
            self.session_counts[key] = 0
        self.work_sessions_completed = 0
        self.session_type_var.set("Work")
        self.task_var.set("")
        self.task_session_goal.set(1)
        if self.session_label:
            self.session_label.config(text="Work Session 1")
        clear_timer_state()

    def resume_if_possible(self):
        state = load_timer_state()
        if not state:
            return False

        remaining = state["remaining_seconds"]
        mins, secs = divmod(remaining, 60)
        summary = f"{state['session_type']} – {mins}:{secs:02} remaining on '{state['task']}'"

        if messagebox.askyesno("Resume Session?", f"Resume your last session:\n{summary}?"):
            self.task_var.set(state["task"])
            self.task_session_goal.set(state["task_sessions_remaining"])
            self.session_type_var.set(state["session_type"])
            for k in state["session_counts"]:
                self.session_counts[k] = state["session_counts"][k]
            self.timer_engine.start_from(remaining, state["session_type"])
            return True
        return False