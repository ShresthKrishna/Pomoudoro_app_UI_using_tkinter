# engine/manager/session_router.py

from datetime import datetime
from tkinter import messagebox

from pomodoro.logger import log_session
from pomodoro.subtask_engine import (
    has_any_subtask,
    get_active_subtask,
    mark_subtask_progress
)
from pomodoro.timer_state_manager import save_timer_state, load_timer_state, clear_timer_state
from screens.reflection_prompt import show_reflection_prompt

class SessionRouter:
    def session_complete_cb(self, prev_session, count):
        completed_at = datetime.now()
        duration = round((completed_at - self.session_start_time).total_seconds(), 2)
        self.stop_tick_loop()

        self.session_counts[prev_session] += 1
        session_number = self.session_counts[prev_session]

        task = self.task_var.get().strip()
        subtask = None

        print(f"[DEBUG] session_complete_cb → Previous session: {prev_session}")
        print(f"[DEBUG] session_complete_cb → Duration: {duration} seconds")

        if prev_session == "Work" and task:
            subtask = mark_subtask_progress(task)
            if hasattr(self, "refresh_subtask_panel"):
                self.refresh_subtask_panel()
            self.update_session_info()

        log_session(
            session_type=prev_session,
            start_time=self.session_start_time,
            end_time=completed_at,
            duration_minutes=duration,
            task=task,
            subtask=subtask,
            resumed=getattr(self, "was_resumed", False),
            interrupted=getattr(self, "was_interrupted", False),
            completed=True,
            session_number=session_number
        )
        self.was_resumed = False
        self.was_interrupted = False

        # Decide next session type
        if prev_session == "Work":
            self.work_sessions_completed += 1
            self.daily_focus_minutes += duration
            self.focus_sessions_today += 1

            next_session = "Long Break" if self.work_sessions_completed % 4 == 0 else "Short Break"
            print(f"[DEBUG] Work session completed → Next session: {next_session}")
            if task and (
                    (has_any_subtask(task) and not get_active_subtask(task)) or
                    self.task_session_goal.get() <= 1
            ):
                print("[DEBUG] Task completed — triggering task decision dialog")
                self._pause_for_task_decision(next_session)
                return
            else:
                self._post_session_routing(task, next_session)
                return

        else:
            next_session = "Work"
            print(f"[DEBUG] Break session completed → Switching to next session: {next_session}")
            task = self.task_var.get().strip()
            self._resume_post_task(task, next_session)

    def _post_session_routing(self, task, next_session):
        self.task_session_goal.set(self.task_session_goal.get() - 1)

        if task and self.task_session_goal.get() <= 0:
            self._pause_for_task_decision(next_session)
        else:
            self._resume_post_task(task, next_session)

    def _resume_post_task(self, task, next_session):
        # Set the upcoming session type (e.g., "Work" or "Short Break")
        self.session_type_var.set(next_session)
        # Refresh any on-screen labels (e.g., subtask label)
        self.update_session_info()
        # Update the session_label text if it exists
        if self.session_label:
            self.session_label.config(
                text=f"{next_session} Session {self.session_counts[next_session] + 1}"
            )

        # Reset the start time for this new session
        self.session_start_time = datetime.now()
        clear_timer_state()
        # Tell the engine to begin the new session countdown
        self.timer_engine.start(next_session)
        # While running, subtask controls should be disabled
        self.set_subtask_editable(False)
        # Kick off the periodic tick loop so the timer visibly counts down
        self.start_tick_loop()

    def resume_if_possible(self):
        state = load_timer_state()
        if not state:
            return False

        remaining = state["remaining_seconds"]
        mins, secs = divmod(remaining, 60)
        summary = f"{state['session_type']} – {mins}:{secs:02} remaining on '{state['task']}'"
        print(f"[DEBUG] Resuming session: {state['session_type']} — {remaining} secs left")
        print(f"[DEBUG] Original start time: {state['timestamp']}")

        if messagebox.askyesno("Resume Session?", f"Resume your last session:\n{summary}?"):
            # Restore saved values
            self.task_var.set(state["task"])
            self.task_session_goal.set(state["task_sessions_remaining"])
            self.session_type_var.set(state["session_type"])
            for k in state["session_counts"]:
                self.session_counts[k] = state["session_counts"][k]

            self.session_start_time = datetime.fromisoformat(state["timestamp"])
            self.was_resumed = True
            self.was_interrupted = state.get("interrupted", False)

            from pomodoro.subtask_engine import get_remaining_subtasks  # should return int
            remaining_subtasks = get_remaining_subtasks(state["task"])
            if self.task_session_goal.get() < remaining_subtasks:
                self.task_session_goal.set(remaining_subtasks)

            if hasattr(self, "task_entry_widget"):
                self.task_entry_widget.configure(state="disabled")

            self.set_subtask_editable(False)

            self.frames["home"].update_idletasks()
            self.timer_engine.start_from(remaining, state["session_type"])

            # Restore the session_label so user sees "Work Session N" etc.
            if self.session_label:
                sess = state["session_type"]
                count = self.session_counts.get(sess, 0) + 1
                self.session_label.config(text=f"{sess} Session {count}")

            # Update the timer_label to show the remaining time immediately
            if self.timer_label:
                self.timer_label.config(text=f"{mins:02d}:{secs:02d}")

            # Start the Tkinter tick loop so the countdown actually ticks
            self.start_tick_loop()
            return True

        else:
            self.task_var.set("")
            if hasattr(self, "task_entry_widget"):
                self.task_entry_widget.configure(state="normal")
            self.set_subtask_editable(True)
            self.frames["home"].update_idletasks()
            return False
