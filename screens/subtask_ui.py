import tkinter as tk
from tkinter import ttk
from pomodoro.theme import theme
from pomodoro.subtask_engine import (
    get_subtasks, add_or_update_task, mark_subtask_progress, reset_subtasks
)

def render_subtask_panel(parent, manager):
    """
    Renders a collapsible subtask panel under Task Plan.
    :param manager: provides .task_var and .task_session_goal IntVar
    :return:
    """
    container = tk.LabelFrame(parent, text="Subtasks",
                              font=theme["label_font"], bg= theme["bg_color"])
    container.columnconfigure(0, weight=1)

    #toggle
    expanded = tk.BooleanVar(value=False)

    def toggle():
        if expanded.get():
            body.grid_remove()
            btn.config(text="▶ Subtasks")
            expanded.set(False)
        else:
            populate()
            body.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
            btn.config(text="▼ Subtasks")
            expanded.set(True)

    btn = tk.Button(container, text="▶ Subtasks",
                    bg=theme["button_color"], font=theme["button_font"],
                    command=toggle)
    btn.grid(row=0, column=0, sticky="w", padx=5, pady=5)

    # body frame
    body = tk.Frame(container, bg=theme["bg_color"])

    def populate():
        for w in body.winfo_children():
            w.destroy()
        task_name = manager.task_var.get().strip()
        if not task_name:
            tk.Label(body, text="(no task)", bg=theme["bg_color"],
                     font=theme["label_font"]).grid(row=0, column=0, padx=5, pady=5)
            return
        subs = get_subtasks(task_name)

        # Header
        hdr = ("Name", "Goal", "Done")
        for c, h in enumerate(hdr):
            tk.Label(body, text=h, bg=theme["bg_color"],
                     font=theme["label_font"]).grid(row=0, column=c, padx=5)

        for r, sub in enumerate(subs, start=1):
            tk.Label(body, text=sub["name"], bg=theme["bg_color"]).grid(row=r, column=0, sticky="w", padx=5)
            tk.Label(body, text=str(sub["goal"]), bg=theme["bg_color"]).grid(row=r, column=1)
            tk.Label(body, text=str(sub["completed"]), bg=theme["bg_color"]).grid(row=r, column=2)
        add_row = len(subs) + 2

        tk.Label(body, text="New Subtask:", bg=theme["bg_color"]).grid(row=add_row, column=0, padx=5, pady=(10, 2))

        entry_name = tk.Entry(body)
        entry_name.grid(row=add_row, column=1, padx=5)

        spin_goal = tk.Spinbox(body, from_=1, to=10, width=5)
        spin_goal.grid(row=add_row, column=2, padx=5)

        def _add():
            task_name = manager.task_var.get().strip()
            if not task_name:
                return

            name = entry_name.get().strip()
            goal = int(spin_goal.get())

            existing = get_subtasks(task_name)
            existing.append({"name": name, "goal": goal, "completed": 0})
            add_or_update_task(task_name, existing)
            populate()

        tk.Button(body, text="+ Add", bg=theme["button_color"],
                  command=_add).grid(row=add_row + 1, column=1, pady=5)
    return container


