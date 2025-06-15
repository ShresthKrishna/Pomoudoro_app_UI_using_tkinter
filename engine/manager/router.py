import tkinter as tk
from tkinter import Toplevel, Label, Button

def resume_post_task(manager, task: str, next_session: str):
    """

    :param manager: The session manager instance
    :param task: The current or new task name
    :param next_session: The type of session to start next.
    :return:
    """
    print(f"[DEBUG] Resuming next sessionL {next_session} | task = '{task}'")
    manager.session_type_var.set(next_session)
    manager.task_var.set(task)
    manager.was_interrupted = False
    manager.is_paused = False

    manager.on_task_fetched(task)
    manager.update_session_info()

    if hasattr(manager, "task_entry_widget"):
        manager.task_entry_widget.configure(state="disabled")
    manager.set_subtask_editable(False)

    manager.timer_engine.start(next_session)
    manager.start_tick_loop()

def _pause_for_task_detection(manager, next_session: str):
    """
    Pauses the app and prompts user for what to do next
    after all planned sessions for a task are completed.
    :param next_session: The type of session to start next
    :return:
    """
    print(f"[DEBUG] Pausing for task decision. Next session: {next_session}")

    manager.stop_tick_loop()
    manager.timer_engine.pause()
    root = manager.root
    task = manager.task_var.get().strip()

    win = Toplevel(root)
    win.title("Session Goal Complete")
    win.geometry("320x160")
    win.transient(root)
    win.grab_set()
    Label(win, text="You've completed your planned sessions for this task!", pady=10).pack()
    Label(win, text="What would you like to do next?", pady=5).pack()

    def start_new_task():
        win.destroy()
        manager.reset_session()

    def add_more_sessions():
        win.destroy()
        manager._resume_post_task(task, next_session)

    def continue_without_task():
        win.destroy()
        manager.task_var.set("")
        manager._resume_post_task("", next_session)

    Button(win, text="Start New Task", command=start_new_task, width=25, pady=3).pack(pady=2)
    Button(win, text="Add More Sessions", command=add_more_sessions, width=25, pady=3).pack(pady=2)
    Button(win, text="Continue Without Task", command=continue_without_task, width=25, pady=3).pack(pady=2)

    root.wait_window(win)

