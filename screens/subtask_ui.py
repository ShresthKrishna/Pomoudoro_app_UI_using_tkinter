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
    current_editing = {"name": None}
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

        headers = ("Name", "Goal", "Done", "", "Edit")
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
                command=lambda n=sub["name"]: (_delete_and_refresh(body, manager, n))
            ).grid(row=r, column=3, padx=5)

            ttk.Button(
                body,
                text="✎",
                width=3,
                command=lambda n=sub["name"], g=sub["goal"]: (
                    name_entry.delete(0, "end"),
                    name_entry.insert(0, n),
                    spin_goal.delete(0, "end"),
                    spin_goal.insert(0, g),
                    add_btn.config(text="💾 Save"),
                    current_editing.update({"name": n})
                )
            ).grid(row=r, column=4, padx=5)

        # Row for adding/editing subtask
        add_row = len(subs) + 2
        tk.Label(body, text="New Subtask:", bg=theme["bg_color"]).grid(row=add_row, column=0, padx=5, pady=(10, 2))

        name_entry = ttk.Entry(body, width=20)
        name_entry.grid(row=add_row, column=1, padx=5, sticky="ew")

        spin_goal = tk.Spinbox(body, from_=1, to=99, width=5, font=theme["entry_font"])
        spin_goal.grid(row=add_row, column=2, padx=5)

        manager._subtask_controls = {
            "name_entry": name_entry,
            "spin_goal": spin_goal
        }

        def save_or_add():
            name = name_entry.get().strip()
            try:
                goal = int(spin_goal.get())
            except ValueError:
                tk.messagebox.showinfo("Subtask Error", "Goal must be a number.")
                return

            if not name:
                return

            if current_editing["name"]:
                delete_subtask(task_name, current_editing["name"])

            add_subtask(task_name, name, goal)
            sync_task_goal_if_needed(manager.task_session_goal, task_name)

            name_entry.delete(0, "end")
            spin_goal.delete(0, "end")
            spin_goal.insert(0, "1")
            current_editing["name"] = None
            add_btn.config(text="+ Add")
            populate()

        add_btn = ttk.Button(body, text="+ Add", command=save_or_add)
        add_btn.grid(row=add_row, column=3, pady=5, sticky="e")

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

    manager.refresh_subtask_panel = populate

    return container
