# engine/manager/session_dialogs.py
from datetime import datetime
from tkinter import Toplevel, Label, Button, Spinbox

from pomodoro.logger import log_session
from screens.reflection_prompt import show_reflection_prompt
from pomodoro.theme import theme
from pomodoro.subtask_engine import reset_subtasks
from pomodoro.timer_state_manager import clear_timer_state

class SessionDialogs:
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

            # 🚫 Skip the generic re-fetch logic — call the legacy path:
            self._resume_post_task(self.task_var.get().strip(), next_session)

        Button(dialog, text="Add", bg=theme["button_color"], command=add_more).pack(pady=5)
        Button(dialog, text="Start New Task", bg=theme["button_color"],
               command=new_task).pack(fill="x", padx=20, pady=5)
        Button(dialog, text="Continue Without Task", bg=theme["button_color"],
               command=continue_no_task).pack(fill="x", padx=20, pady=5)
        Label(dialog, text="Add More Sessions:", bg=theme["bg_color"]).pack(pady=(10, 2))
        spin = Spinbox(dialog, from_=1, to=10, width=5)
        spin.pack()
        Button(dialog, text="Add", bg=theme["button_color"], command=add_more).pack(pady=5)
