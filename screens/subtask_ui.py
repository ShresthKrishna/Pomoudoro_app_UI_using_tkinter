import tkinter as tk
from tkinter import ttk
from pomodoro.theme import theme
from pomodoro.subtask_engine import (
    get_subtasks,
    add_subtask,
    delete_subtask,
    sync_task_goal_if_needed
)


def render_subtask_panel(parent, manager):
    container = ttk.LabelFrame(parent, text="Subtasks", style="Subtask.TLabelframe")
    container.columnconfigure(0, weight=1)

    expanded = tk.BooleanVar(value=False)
    body = tk.Frame(container, bg=theme["bg_color"])
    body.grid(row=1, column=0, sticky="nsew", padx=5)

    def populate():
        for w in body.winfo_children():
            w.destroy()

        task_name = manager.get_active_task().strip()
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

            ttk.Button(
                body,
                text="✕",
                width=3,
                command=lambda n=sub["name"]: (delete_subtask(task_name, n), populate())
            ).grid(row=r, column=3, padx=5)

        # Row for adding new subtask
        add_row = len(subs) + 2
        tk.Label(body, text="New Subtask:", bg=theme["bg_color"]).grid(row=add_row, column=0, padx=5, pady=(10, 2))

        name_entry = ttk.Entry(body, width=20)
        name_entry.grid(row=add_row, column=1, padx=5, sticky="ew")

        spin_goal = tk.Spinbox(body, from_=1, to=99, width=5, font=theme["entry_font"])
        spin_goal.grid(row=add_row, column=2, padx=5)

        def _add():
            name = name_entry.get().strip()
            try:
                goal = int(spin_goal.get())
                add_subtask(task_name, name, goal)
                sync_task_goal_if_needed(manager.task_session_goal, task_name)
            except ValueError as e:
                print(f"[DEBUG] {e}")
                tk.messagebox.showinfo("Subtask Error", str(e))
            else:
                name_entry.delete(0, "end")
                populate()

        ttk.Button(body, text="+ Add", command=_add).grid(row=add_row, column=3, pady=5, sticky="e")

    def _delete_and_refresh(frame: tk.Frame, manager, subtask_name: str) -> None:
        task = manager.get_active_task()
        delete_subtask(task, subtask_name)
        sync_task_goal_if_needed(manager.task_session_goal, task)
        populate()


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
