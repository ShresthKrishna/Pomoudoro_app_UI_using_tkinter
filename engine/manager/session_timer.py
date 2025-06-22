# engine/manager/session_timer.py
from datetime import datetime

from pomodoro.logger import log_session
from pomodoro.task_memory import update_task_memory, get_all_tasks
from pomodoro.timer_engine import TimerEngine
from pomodoro.timer_state_manager import save_timer_state, clear_timer_state
from screens.intent_prompt import show_intent_prompt


class SessionTimer:
    def __init__(self, update_display_cb, session_complete_cb, durations):
        self.timer_label = None
        self.timer_engine = TimerEngine(update_display_cb, session_complete_cb, durations)

    def on_start(self):
        session_type = self.session_type_var.get()
        # Lock task editing
        if hasattr(self, "task_entry_widget"):
            self.task_entry_widget.configure(state="disabled")

        def proceed_start():
            self.session_start_time = datetime.now()
            task_name = self.task_var.get().strip()

            if task_name:
                update_task_memory(task_name)
                self.all_tasks = get_all_tasks()

            self.timer_engine.update_durations({
                k: self.duration_vars[k].get() * 60 for k in self.duration_vars
            })
            self.timer_engine.start(session_type)
            self.set_subtask_editable(False)

            self.update_session_info()

            save_timer_state({
                "active": True,
                "session_type": session_type,
                "remaining_seconds": self.timer_engine.remaining,
                "session_counts": self.session_counts,
                "task": task_name,
                "task_sessions_remaining": self.task_session_goal.get(),
                "timestamp": datetime.now().isoformat()
            })

            if hasattr(self, "task_entry_widget"):
                self.task_entry_widget.configure(state="disabled")

        if session_type == "Work":
            show_intent_prompt(self.root, proceed_start)
        else:
            proceed_start()

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
        # Toggle task editing
        if hasattr(self, "task_entry_widget"):
            self.task_entry_widget.configure(state="normal" if self.is_paused else "disabled")

        if self.is_paused:
            self.timer_engine.resume()
            pause_button.config(text="Pause")
        else:
            self.timer_engine.pause()
            pause_button.config(text="Resume")
        self.is_paused = not self.is_paused
        self.set_subtask_editable(self.is_paused)

    def reset_session(self):
        self.timer_engine.reset()
        self.update_session_info()
        self.set_subtask_editable(True)

        # Re-enable task editing
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
        clear_timer_state()
        self.set_start_button_state("start")
        self.set_subtask_editable(True)
        self.was_resumed = False
        self.was_interrupted = False

    def end_session(self):
            end_time = datetime.now()

            if not self.session_start_time:
                duration = 0
            else:
                duration = round((end_time - self.session_start_time).total_seconds() / 60)

            session_type = self.session_type_var.get()
            self.session_counts[session_type] += 1  # ✅ increment session number here

            log_session(
                session_type=session_type,
                start_time=self.session_start_time,
                end_time=end_time,
                duration_minutes=duration,
                task=self.task_var.get().strip(),
                subtask=None,
                resumed=getattr(self, "was_resumed", False),
                interrupted=getattr(self, "was_interrupted", False),
                completed=False
            )
            self.reset_session()

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

    def update_display_cb(self, mins, secs):
        if self.timer_label:
            self.timer_label.config(text=f"{mins:02d}:{secs:02d}")
