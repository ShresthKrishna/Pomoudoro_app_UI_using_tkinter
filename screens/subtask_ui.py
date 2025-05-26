import tkinter as tk
from tkinter import ttk
from pomodoro.theme import theme
from pomodoro.subtask_engine import (
    get_subtasks, add_subtask, delete_subtask
)

def render_subtask_panel(parent, manager):
    container = tk.LabelFrame(parent, text="Subtasks",
                              font=theme["label_font"], bg=theme["bg_color"])
    container.columnconfigure(0, weight=1)

    expanded = tk.BooleanVar(value=False)

    body = tk.Frame(container, bg=theme["bg_color"])
    body.grid(row=1, column=0, sticky="nsew", padx=5)

    def populate():
        for w in body.winfo_children():
            w.destroy()

        task_name = manager.task_var.get().strip()
        if not task_name:
            tk.Label(body, text="(no task)", bg=theme["bg_color"],
                     font=theme["label_font"]).grid(row=0, column=0, padx=5, pady=5)
            return

        subs = get_subtasks(task_name)

        headers = ("Name", "Goal", "Done", "")
        for c, h in enumerate(headers):
            tk.Label(body, text=h, bg=theme["bg_color"], font=theme["label_font"]).grid(row=0, column=c, padx=5)

        for r, sub in enumerate(subs, start=1):
            tk.Label(body, text=sub["name"], bg=theme["bg_color"]).grid(row=r, column=0, sticky="w", padx=5)
            tk.Label(body, text=str(sub["goal"]), bg=theme["bg_color"]).grid(row=r, column=1)
            tk.Label(body, text=str(sub["completed"]), bg=theme["bg_color"]).grid(row=r, column=2)

            tk.Button(body, text="✕", bg=theme["accent_color"], fg="white",
                      command=lambda n=sub["name"]: (delete_subtask(task_name, n), populate())
                      ).grid(row=r, column=3, padx=5)

        # Row for adding new subtask
        add_row = len(subs) + 2
        tk.Label(body, text="New Subtask:", bg=theme["bg_color"]).grid(row=add_row, column=0, padx=5, pady=(10, 2))

        name_entry = tk.Entry(body)
        name_entry.grid(row=add_row, column=1, padx=5)

        spin_goal = tk.Spinbox(body, from_=1, to=10, width=5)
        spin_goal.grid(row=add_row, column=2, padx=5)

        def _add():
            name = name_entry.get().strip()
            if name:
                goal = int(spin_goal.get())
                add_subtask(task_name, name, goal)
                populate()

        tk.Button(body, text="+ Add", bg=theme["button_color"], command=_add).grid(row=add_row, column=3, pady=5)

    def toggle():
        if expanded.get():
            body.grid_remove()
            btn.config(text="▶ Subtasks")
            expanded.set(False)
        else:
            populate()
            body.grid()
            btn.config(text="▼ Subtasks")
            expanded.set(True)

    btn = tk.Button(container, text="▶ Subtasks",
                    bg=theme["button_color"], font=theme["button_font"],
                    command=toggle)
    btn.grid(row=0, column=0, sticky="w", padx=5, pady=5)

    return container
