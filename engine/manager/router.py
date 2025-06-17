import tkinter as tk
from tkinter import Toplevel, Label, Button
from datetime import datetime
from pomodoro.subtask_engine import mark_subtask_progress, get_total_subtask_goal
from engine.manager import state

def session_complete_cb(manager, prev_session: str, count: int):
    """
    Called when a session completes.
    Logs the session and routes to the next session based on task status.
    """
    print(f"[DEBUG] Session complete: {prev_session} #{count}")

    now = datetime.now()
    task = manager.task_var.get().strip()
    session_type = prev_session
    session_count = count
    session_goal = manager.task_session_goal.get()
    session_start_time = manager.session_start_time or now
    session_end_time = now
    session_number = manager.session_counts.get(session_type, 0)

    # Log the completed session
    manager.logger.log_session_data({
        "task": task,
        "session_type": session_type,
        "session_count": session_count,
        "session_number": session_number,
        "completed": True,
        "resumed": manager.was_resumed,
        "interrupted": manager.was_interrupted,
        "start_time": session_start_time.isoformat(),
        "end_time": session_end_time.isoformat()
    })

    # Update session counts
    manager.session_counts[prev_session] = count

    # Work session extras
    if prev_session == "Work":
        manager.work_sessions_completed += 1
        manager.daily_focus_minutes += manager.timer_engine.duration / 60
        manager.focus_sessions_today += 1
        manager.was_resumed = False
        manager.was_interrupted = False

        # Progress subtask
        subtask_name = mark_subtask_progress(task)
        print(f"[DEBUG] Subtask marked complete: {subtask_name}")

    # Determine next session
    next_session = _determine_next_session(prev_session, manager.work_sessions_completed)

    # Handle task session goal completion
    if prev_session == "Work":
        remaining = get_total_subtask_goal(task)
        if remaining <= 0:
            print(f"[DEBUG] Task session goal met for '{task}'. Prompting user.")
            _pause_for_task_detection(manager, next_session)
            return

    # If not goal-complete, auto-resume next
    resume_post_task(manager, task, next_session)


def _determine_next_session(current: str, work_sessions_completed: int) -> str:
    if current == "Work":
        return "Long Break" if work_sessions_completed % 4 == 0 else "Short Break"
    return "Work"

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

def resume_if_possible(manager):
    state_data = state.load()
    if not state_data or not state_data.get("active"):
        print("[DEBUG] No active session to resume.")
        return

    print(f"[DEBUG] Resuming session: {state_data['session_type']} — {state_data['remaining_seconds']} secs left")
    print(f"[DEBUG] Original start time: {state_data['timestamp']}")

    manager.was_resumed = True
    manager.was_interrupted = False
    manager.is_paused = False

    manager.session_type_var.set(state_data["session_type"])
    manager.task_var.set(state_data.get("task", ""))
    manager.task_session_goal.set(state_data.get("task_sessions_remaining", 1))
    manager.session_counts.update(state_data.get("session_counts", {}))

    # Restore UI
    manager.on_task_fetched(manager.task_var.get())
    manager.update_session_info()
    if hasattr(manager, "task_entry_widget"):
        manager.task_entry_widget.configure(state="disabled")
    manager.set_subtask_editable(False)

    manager.session_start_time = datetime.fromisoformat(state_data["timestamp"])
    manager.timer_engine.resume(
        session_type=state_data["session_type"],
        remaining_seconds=state_data["remaining_seconds"]
    )
    manager.start_tick_loop()