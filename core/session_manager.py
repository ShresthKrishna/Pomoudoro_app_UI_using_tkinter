import tkinter as tk
from datetime import datetime
from tkinter import messagebox
from pomodoro.timer_engine import TimerEngine
from pomodoro.logger import log_session
from pomodoro.timer_state_manager import save_timer_state, load_timer_state, clear_timer_state
from pomodoro.task_memory import get_all_tasks, update_task_memory
from utils.storage import load_user_settings, save_user_settings
from pomodoro.theme import theme
from pomodoro.subtask_engine import mark_subtask_progress, get_active_subtask

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
        self.set_start_button_state = lambda state: None  # will be assigned later
        self._tick_loop_id = None
        self._tick_loop_running = False

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
        duration = round((completed_at - self.session_start_time).total_seconds() / 60
                         if self.session_start_time else 0)
        self.session_counts[prev_session] += 1

        task = self.task_var.get().strip()
        subtask = None

        # ✅ Track subtask if Work session and a task is set
        if prev_session == "Work" and task:
            subtask = mark_subtask_progress(task)

        log_session(prev_session, completed_at,
                    self.session_counts[prev_session],
                    duration,
                    task=task,
                    subtask=subtask)

        if prev_session == "Work":
            self.work_sessions_completed += 1
            next_session = "Long Break" if self.work_sessions_completed % 4 == 0 else "Short Break"

            # ✅ Check if all subtasks are done
            if task and not get_active_subtask(task):
                self._pause_for_task_decision(next_session)
                return

            # Fallback to regular task session logic
            self.task_session_goal.set(self.task_session_goal.get() - 1)
            if self.task_session_goal.get() <= 0:
                self._pause_for_task_decision(next_session)
                return
        else:
            next_session = "Work"

        self._resume_post_task(next_session)

    def _pause_for_task_decision(self, next_session):
        from tkinter import Toplevel, Label, Button, Spinbox

        self.stop_tick_loop()
        dialog = Toplevel(self.root)
        dialog.title("Task Completed")
        dialog.configure(bg=theme["bg_color"])
        dialog.grab_set()
        dialog.geometry("600x300")

        def on_close_dialog():
            dialog.destroy()
            self._resume_post_task(next_session)

        dialog.protocol("WM_DELETE_WINDOW", on_close_dialog)

        Label(dialog, text="You've completed your planned sessions for this task.",
              bg=theme["bg_color"], font=theme["label_font"]).pack(pady=(10, 5))

        def new_task():
            self.task_var.set("")
            self.task_session_goal.set(1)
            self._just_cleared_task = True
            dialog.destroy()

            # Fully reset timer state and UI
            self.timer_engine.reset()
            clear_timer_state()
            self.session_type_var.set("Work")
            if self.session_label:
                self.session_label.config(text="Work Session 1")
            self.set_start_button_state("start")
            self.timer_engine.update_durations({
                k: self.duration_vars[k].get() * 60 for k in self.duration_vars
            })

            initial_mins = self.duration_vars["Work"].get()
            if self.timer_label:
                self.timer_label.config(text=f"{initial_mins:02d}:00")
                self.frames["home"].update_idletasks()

            self.start_tick_loop()

        def continue_no_task():
            self.task_var.set("")
            self.task_session_goal.set(1)
            dialog.destroy()
            self._resume_post_task(next_session)

        def add_more():
            spin_val = int(spin.get())
            if spin_val > 0:
                self.task_session_goal.set(spin_val)
            dialog.destroy()
            self._resume_post_task(next_session)

        Button(dialog, text="Start New Task", bg=theme["button_color"],
               command=new_task).pack(fill="x", padx=20, pady=5)
        Button(dialog, text="Continue Without Task", bg=theme["button_color"],
               command=continue_no_task).pack(fill="x", padx=20, pady=5)
        Label(dialog, text="Add More Sessions:", bg=theme["bg_color"]).pack(pady=(10, 2))
        spin = Spinbox(dialog, from_=1, to=10, width=5)
        spin.pack()
        Button(dialog, text="Add", bg=theme["button_color"], command=add_more).pack(pady=5)

    def _resume_post_task(self, next_session):
        self.session_type_var.set(next_session)
        if self.session_label:
            self.session_label.config(text=f"{next_session} Session {self.session_counts[next_session] + 1}")
        self.session_start_time = datetime.now()
        clear_timer_state()
        self.timer_engine.start(next_session)
        self.start_tick_loop()

    def start_tick_loop(self):
        if self._tick_loop_running:
            return
        self._tick_loop_running = True

        def tick_once():
            if not self._tick_loop_running:
                return
            self.timer_engine.tick()
            self._tick_loop_id = self.root.after(10, tick_once)

        tick_once()

    def stop_tick_loop(self):
        self._tick_loop_running = False
        if self._tick_loop_id is not None:
            self.root.after_cancel(self._tick_loop_id)
            self._tick_loop_id = None
        self.timer_engine.pause()

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
        self.set_start_button_state("start")

    def resume_if_possible(self):
        state = load_timer_state()
        if not state:
            return False

        remaining = state["remaining_seconds"]
        mins, secs = divmod(remaining, 60)
        summary = f"{state['session_type']} – {mins}:{secs:02} remaining on '{state['task']}'"

        if messagebox.askyesno("Resume Session?", f"Resume your last session:\n{summary}?"):
            self.task_session_goal.set(state["task_sessions_remaining"])
            self.session_type_var.set(state["session_type"])
            for k in state["session_counts"]:
                self.session_counts[k] = state["session_counts"][k]
            self.frames["home"].update_idletasks()
            self.timer_engine.start_from(remaining, state["session_type"])
            return True
        else:
            # ✅ Fix typing bug after declining resume
            self.task_var.set("")  # fully reset binding
            self.frames["home"].update_idletasks()
            return False

    def end_session(self):
        end_time = datetime.now()

        if not self.session_start_time:
            duration = 0
        else:
            duration = round((end_time - self.session_start_time).total_seconds() / 60)

        session_type = self.session_type_var.get()
        self.session_counts[session_type] += 1  # ✅ increment session number here

        log_session(
            session_type,
            end_time,
            self.session_counts[session_type],
            duration,
            task=self.task_var.get().strip(),
            completed=False
        )

        self.reset_session()
