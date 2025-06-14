import tkinter as tk
from datetime import datetime,date
from tkinter import messagebox
from pomodoro.timer_engine import TimerEngine
from pomodoro.logger import log_session
from pomodoro.timer_state_manager import save_timer_state, load_timer_state, clear_timer_state
from pomodoro.task_memory import get_all_tasks, update_task_memory
from utils.storage import load_user_settings, save_user_settings, write_json_file, read_json_file
from pomodoro.theme import theme
from pomodoro.subtask_engine import has_any_subtask, mark_subtask_progress, get_active_subtask, reset_subtasks, get_current_subtask_name
from screens.intent_prompt import show_intent_prompt
from screens.reflection_prompt import show_reflection_prompt
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
        self.has_prompted_intent = False
        self.last_focus_rating = None
        self.last_intent_fulfilled = None
        self.was_resumed = False
        self.was_interrupted = False
        self.daily_focus_minutes = 0.0
        self.focus_sessions_today = 0

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

    def update_session_info(self):
        task = self.task_var.get().strip()
        session_type = self.session_type_var.get()
        session_count = self.session_counts.get(session_type, 0) + 1

        subtask = None
        if task:
            subtask = get_current_subtask_name(task)
            print(f"[DEBUG] update_session_info | Task: {task} | Session: {session_type}")
            print(f"[DEBUG] Fetched subtask: {subtask}")

        if hasattr(self, "task_heading"):
            self.task_heading.config(text=task or "(No Task Selected)")

        if hasattr(self, "subtask_label"):
            if session_type == "Work":
                self.subtask_label.config(
                    text=f"{subtask or 'No Subtask'} : {session_type} Session {session_count}"
                )
            else:
                self.subtask_label.config(
                    text=f"{subtask or 'No Subtask'} : {session_type} Session {session_count}"
                )

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

            def after_reflection(focus_rating, intent_fulfilled):
                self.last_focus_rating = focus_rating
                self.last_intent_fulfilled = intent_fulfilled

                log_session(
                    session_type="Work",
                    start_time=self.session_start_time,
                    end_time=datetime.now(),
                    duration_minutes=round((datetime.now() - self.session_start_time).total_seconds(), 2),
                    task=self.task_var.get().strip(),
                    subtask=None,
                    focus_rating=focus_rating,
                    intent_fulfilled=intent_fulfilled,
                    resumed=getattr(self, "was_resumed", False),
                    interrupted=getattr(self, "was_interrupted", False),
                    completed=True
                )

                self._resume_post_task(self.task_var.get().strip(), next_session)

            intent_exists = hasattr(self, "last_user_intent") and bool(self.last_user_intent.strip())
            show_reflection_prompt(self.root, intent_exists, after_reflection)

        dialog.protocol("WM_DELETE_WINDOW", on_close_dialog)

        Label(dialog, text="You've completed your planned sessions for this task.",
              bg=theme["bg_color"], font=theme["label_font"]).pack(pady=(10, 5))

        def new_task():
            current_task = self.task_var.get().strip()
            if current_task:
                reset_subtasks(current_task)
            if hasattr(self, "task_entry_widget"):
                self.task_entry_widget.configure(state="normal")

            self.task_var.set("")
            self.task_session_goal.set(1)
            self._just_cleared_task = True
            dialog.destroy()

            def after_reflection(focus_rating, intent_fulfilled):
                self.last_focus_rating = focus_rating
                self.last_intent_fulfilled = intent_fulfilled
                log_session(
                    session_type="Work",
                    start_time=self.session_start_time,
                    end_time=datetime.now(),
                    duration_minutes=round((datetime.now() - self.session_start_time).total_seconds(), 2),
                    task=current_task or self.task_var.get().strip(),
                    subtask=None,
                    focus_rating=focus_rating,
                    intent_fulfilled=intent_fulfilled,
                    resumed=getattr(self, "was_resumed", False),
                    interrupted=getattr(self, "was_interrupted", False),
                    completed=True
                )

                self.timer_engine.reset()
                clear_timer_state()
                self.set_subtask_editable(True)
                self.session_type_var.set("Work")
                if self.session_label:
                    self.session_label.config(text="Work Session 1")
                self.set_start_button_state("start")
                self.timer_engine.update_durations({
                    k: self.duration_vars[k].get() * 60 for k in self.duration_vars
                })

                if self.timer_label:
                    self.timer_label.config(text=f"{self.duration_vars['Work'].get():02d}:00")
                    self.frames["home"].update_idletasks()
                self.start_tick_loop()

            intent_exists = hasattr(self, "last_user_intent") and bool(self.last_user_intent.strip())
            show_reflection_prompt(self.root, intent_exists, after_reflection)

        def continue_no_task():
            self.task_var.set("")
            self.task_session_goal.set(1)
            dialog.destroy()

            def after_reflection(focus_rating, intent_fulfilled):
                self.last_focus_rating = focus_rating
                self.last_intent_fulfilled = intent_fulfilled
                log_session(
                    session_type="Work",
                    start_time=self.session_start_time,
                    end_time=datetime.now(),
                    duration_minutes=round((datetime.now() - self.session_start_time).total_seconds(), 2),
                    task=self.task_var.get().strip(),
                    subtask=None,
                    focus_rating=focus_rating,
                    intent_fulfilled=intent_fulfilled,
                    resumed=getattr(self, "was_resumed", False),
                    interrupted=getattr(self, "was_interrupted", False),
                    completed=True
                )

                self._resume_post_task(self.task_var.get().strip(), next_session)

            intent_exists = hasattr(self, "last_user_intent") and bool(self.last_user_intent.strip())
            show_reflection_prompt(self.root, intent_exists, after_reflection)

        def add_more():
            spin_val = int(spin.get())
            if spin_val > 0:
                self.task_session_goal.set(spin_val)
            dialog.destroy()

            # 🚫 Skip reflection prompt when adding sessions to same task
            self._resume_post_task(self.task_var.get().strip(), next_session)

        Button(dialog, text="Start New Task", bg=theme["button_color"],
               command=new_task).pack(fill="x", padx=20, pady=5)
        Button(dialog, text="Continue Without Task", bg=theme["button_color"],
               command=continue_no_task).pack(fill="x", padx=20, pady=5)
        Label(dialog, text="Add More Sessions:", bg=theme["bg_color"]).pack(pady=(10, 2))
        spin = Spinbox(dialog, from_=1, to=10, width=5)
        spin.pack()
        Button(dialog, text="Add", bg=theme["button_color"], command=add_more).pack(pady=5)

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

    def set_subtask_editable(self, editable=True):
        if hasattr(self, "_subtask_controls"):
            for widget in self._subtask_controls.values():
                try:
                    state = "normal" if editable else "disabled"
                    widget.configure(state=state)
                except Exception as e:
                    print(f"[DEBUG] Subtask widget toggle failed: {e}")

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

    def on_task_fetched(self, task_name: str):

        from pomodoro.subtask_engine import get_total_subtask_goal

        # 1. Update the current task variable
        self.task_var.set(task_name)

        # 2. Compute how many subtask‐sessions are still pending
        total_subtask_goal = get_total_subtask_goal(task_name)

        if total_subtask_goal > 0:
            # If there are any incomplete subtasks, override to that sum:
            self.task_session_goal.set(total_subtask_goal)
        else:
            # Otherwise, no subtasks remain—reset back to 1
            self.task_session_goal.set(1)

        # 3. Refresh subtask/session labels on screen
        self.update_session_info()

        # 4. Update the session_label (e.g. "Work Session N")
        if self.session_label:
            sess = self.session_type_var.get()
            count = self.session_counts.get(sess, 0) + 1
            self.session_label.config(text=f"{sess} Session {count}")

        print(f"[DEBUG] on_task_fetched → Task: '{task_name}', "
              f"total_subtask_goal={total_subtask_goal}, "
              f"task_session_goal={self.task_session_goal.get()}")


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

    def get_active_task(self) -> str:
        return self.task_var.get().strip()
    