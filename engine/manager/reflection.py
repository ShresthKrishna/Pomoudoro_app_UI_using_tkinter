# engine/session_manager/reflection.py

import tkinter as tk
from tkinter import Toplevel, Label, Button, Entry

def maybe_trigger_intent(manager):
    """
    Called by SessionManager.on_start().
    If it's a Work session and no intent has been set yet this launch, prompts user.
    """
    session_type = manager.session_type_var.get()
    if session_type == "Work" and not manager.has_prompted_intent:
        show_intent_prompt(manager)
    else:
        _begin_session(manager)


def show_intent_prompt(manager):
    """
    Pops up an intent-capture dialog before starting a Work session.
    """
    root = manager.root

    modal = Toplevel(root)
    modal.title("Set Your Intent")
    modal.geometry("350x150")
    modal.transient(root)
    modal.grab_set()

    Label(modal, text="What will you focus on this session?", pady=10).pack()

    entry = Entry(modal, width=40)
    entry.pack(pady=5)
    entry.focus()

    def submit():
        intent = entry.get().strip()
        if intent:
            print(f"[DEBUG] Intent submitted: {intent}")
        else:
            print(f"[DEBUG] Intent skipped.")

        manager.has_prompted_intent = True
        modal.destroy()
        _begin_session(manager)

    Button(modal, text="Start Session", command=submit, width=25).pack(pady=10)
    root.wait_window(modal)


def _begin_session(manager):
    """
    Starts the actual timer logic after intent (or immediately if bypassed).
    """
    print("[DEBUG] Starting session")
    manager.session_start_time = manager.session_start_time or manager.timer_engine.start_time or None
    manager.timer_engine.start(manager.session_type_var.get())
    manager.start_tick_loop()
    manager.set_start_button_state("end")
    manager.is_paused = False
    manager.was_resumed = False
    manager.was_interrupted = False
    manager.set_subtask_editable(False)

    if hasattr(manager, "task_entry_widget"):
        manager.task_entry_widget.configure(state="disabled")
