import tkinter as tk
from datetime import datetime
from pomodoro.timer_engine import TimerEngine
from engine.manager import logger, state, subtasks, router, reflection
from engine.manager.subtasks import set_subtask_controls_enabled


class SessionManager:
    def __init__(self, root):
        self.root = root
        self.frames = {}
        self.session_type_var = tk.StringVar(value="Work")
        self.task_var = tk.StringVar()
        self.task_session_goal = tk.IntVar(value=1)
        self.session_counts = {"Work": 0, "Short Break": 0, "Long Break": 0}
        self.work_sessions_completed = 0
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
            "Short Break": tk.IntVar(value=5),
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
    # ----------------------------------------------------

    def register_screens(self, frame_dict):
        pass

    def show_frames(self, name):
        pass

    def _load_durations(self):
        from utils.storage import load_user_settings

        saved = load_user_settings()
        for types in self.duration_vars:
            if types in saved:
                self.duration_vars[types].set(saved[types])

    # ---------------------------------------------------
    #                       Session Start/Stop
    # ----------------------------------------------------

    def on_start(self):
        """Start a session (invokes intent prompt if Work)."""
        reflection.maybe_trigger_intent(self)

    def end_session(self):
        """Log and reset a session that was interrupted mid-way."""
        pass

    def reset_session(self):
        """Clear all state and return to default idle state."""
        self.timer_engine.reset()
        self.update_session_info()
        self.set_subtask_editable(True)

        if hasattr(self, "task_entry_widget"):
            self.task_entry_widget.configure(state="normal")

        for key in self.session_counts:
            self.session_counts[key] = 0
        self.work_sessions_completed = 0
        self.session_type_var.set("Work")
        self.task_var.set("")
        self.task_session_goal.set(1)
        if self.session_label:
            self.session_label.config(text="Work Session 1")
        state.clear()
        self.set_start_button_state("start")
        self.set_subtask_editable(True)
        self.was_resumed = False
        self.was_interrupted = False

    # ---------------------------------------------------
    #                       Timer Loop Control
    # ----------------------------------------------------

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

    def toggle_pause(self, pause_button):
        state.save({
            "active": True,
            "session_type": self.timer_engine.session_type,
            "remaining_seconds": self.timer_engine.remaining,
            "session_counts": self.session_counts,
            "task": self.task_var.get().strip(),
            "task_sessions_remaining": self.task_session_goal.get(),
            "timestamp": datetime.now().isoformat()
        })

        if hasattr(self, "task_entry_widget"):
            self.task_entry_widget.configure(
                state="normal" if self.is_paused else "disabled"
            )

        if self.is_paused:
            self.timer_engine.resume()
            pause_button.config(text="Pause")
        else:
            self.timer_engine.pause()
            pause_button.config(text="Resume")

        self.is_paused = not self.is_paused
        self.set_subtask_editable(self.is_paused)

    # ---------------------------------------------------
    #                       Session Flow
    # ----------------------------------------------------
    def session_complete_cb(self, prev_session, count):
        router.session_complete_cb(self, prev_session, count)

    def _post_session_routing(self, task, next_session):
        pass

    def _resume_post_task(self, task, next_session):
        """
            Args:
                manager: The SessionManager instance.
                task: The current or new task name.
                next_session: The type of session to start next ("Work", "Short Break", etc.)
            """
        router.resume_post_task(self, task, next_session)

    # ---------------------------------------------------
    #                       Dialogs
    # ----------------------------------------------------

    def _pause_for_task_decision(self, next_session):
        router._pause_for_task_detection(self, next_session)

    # -------------------------------------------`--------
    #                       Resume + State Restore
    # ----------------------------------------------------

    def resume_if_possible(self):
        router.resume_if_possible(self)

    # ---------------------------------------------------
    #                       UI Label
    # ----------------------------------------------------

    def update_display_cb(self, mins, secs):
        if self.timer_label:
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")

    def update_session_info(self):
        task = self.task_var.get().strip()
        session_type = self.session_type_var.get()
        session_count = self.session_counts.get(session_type, 0) + 1

        subtask = None
        if task:
            from pomodoro.subtask_engine import get_current_subtask_name
            subtask = get_current_subtask_name(task)
            print(f"[DEBUG] update_session_info | Task: {task} | Session: {session_type}")
            print(f"[DEBUG] Fetched subtask: {subtask}")

        if hasattr(self, "task_heading"):
            self.task_heading.config(text=task or "(No Task Selected)")
        if hasattr(self, "subtask_label"):
            label = f"{subtask or 'No Subtask'} : {session_type} Session {session_count}"
            self.subtask_label.config(text=label)

    def set_subtask_editable(self, editable=True):
        if hasattr(self, "_subtask_controls"):
            set_subtask_controls_enabled(self._subtask_controls, editable)

    # ---------------------------------------------------
    #                       Task Logic
    # ----------------------------------------------------

    def on_task_fetched(self, task_name):
        from engine.manager.subtasks import fetch_subtask_data
        self.task_var.set(task_name)
        session_type = self.session_type_var.get()
        data = fetch_subtask_data(task_name, session_type, self.session_counts)

        self.task_session_goal.set(data["goal"])
        self.update_session_info()

        if self.session_label:
            self.session_label.config(text=data["session_label"])
        print(f"[DEBUG] on_task_fetched → Task: '{task_name}', "f"subtask={data['subtask']}, "f"goal={data['goal']}")

    def get_active_task(self) -> str:
        return self.task_var.get().strip()

    # ---------------------------------------------------
    #                       Settings
    # ----------------------------------------------------
    def save_settings(self):
        from utils.storage import save_user_settings
        durations = {k: self.duration_vars[k].get() for k in self.duration_vars}
        save_user_settings(durations)
        self.timer_engine.update_durations({k: v*60 for k, v in durations.items()})

    def log_daily_focus_summary(self):
        logger.log_daily_focus_summary(
            self.daily_focus_minutes,
            self.focus_sessions_today
        )
