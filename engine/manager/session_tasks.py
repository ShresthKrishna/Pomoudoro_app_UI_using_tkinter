# engine/manager/session_tasks.py

from pomodoro.subtask_engine import (
    has_any_subtask,
    mark_subtask_progress,
    get_active_subtask,
    reset_subtasks,
    get_current_subtask_name
)
from pomodoro.task_memory import get_all_tasks


class SessionTasks:
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

    def get_all_task_names(self):
        """
        Return the list of task names for the home-screen dropdown.
        """
        try:
            return get_all_tasks()
        except Exception as e:
            print(f"[DEBUG] Failed to load tasks: {e}")
            return []