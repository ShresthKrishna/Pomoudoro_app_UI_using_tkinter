import tkinter as tk
from tkinter import ttk
from pomodoro.theme import theme
from screens.subtask_ui import render_subtask_panel

def render_home_screen(frame, manager):
    # --- Configure grid with explicit heights ---
    frame.rowconfigure(0, weight=0, minsize=30)  # Session Type label
    frame.rowconfigure(1, weight=0, minsize=40)  # Dropdown
    frame.rowconfigure(2, weight=1, minsize=100)  # Timer (expands)
    frame.rowconfigure(3, weight=0, minsize=30)  # Session label
    frame.rowconfigure(4, weight=0, minsize=100)  # Task Plan
    frame.rowconfigure(5, weight=0, minsize=100)  # Subtask panel ← ADD this row
    frame.rowconfigure(6, weight=0, minsize=20)  # Bottom spacer

    # 0: Session Type label
    tk.Label(
        frame,
        text="Session Type",
        bg=theme["bg_color"],
        font=theme["label_font"]
    ).grid(row=0, column=0, sticky="nsew", pady=(5, 0))

    # 1: Session type dropdown (wide)
    opt = tk.OptionMenu(
        frame,
        manager.session_type_var,
        "Work", "Short Break", "Long Break"
    )
    # opt.config(width=22)
    opt.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 10))

    # 2: Timer display (centered in the expanding area)
    manager.timer_label = tk.Label(
        frame,
        text="00:00",
        font=theme["timer_font"],
        bg=theme["bg_color"]
    )
    manager.timer_label.grid(row=2, column=0, columnspan=3, pady=20)

    # 3: Session label
    info_frame = tk.Frame(frame, bg=theme["highlight_bg"])
    info_frame.grid(row=3, column=0, columnspan=3, padx=20, pady=(5, 5), sticky="ew")
    info_frame.columnconfigure(0, weight=1)

    manager.task_heading = tk.Label(
        info_frame,
        width=40,
        anchor="center",
        font=theme["heading_font"],
        bg=theme["highlight_bg"]
    )
    manager.task_heading.grid(row=0, column=0, sticky="ew", pady=(2, 0))

    manager.subtask_label = tk.Label(
        info_frame,
        width=40,
        anchor="center",
        font=theme["subheading_font"],
        bg=theme["highlight_bg"]
    )
    manager.subtask_label.grid(row=1, column=0, sticky="ew", pady=(0, 5))

    # 4: Task Plan box
    task_frame = tk.LabelFrame(
        frame,
        text="Task Plan",
        font=theme["label_font"],
        bg=theme["bg_color"]
    )
    task_frame.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
    # make two columns: labels (0) and inputs (1)
    task_frame.columnconfigure(0, weight=0)
    task_frame.columnconfigure(1, weight=1)

    #   Task Name (row 0)
    tk.Label(
        task_frame,
        text="Task Name:",
        font=theme["label_font"],
        bg=theme["bg_color"]
    ).grid(row=0, column=0, sticky="ew", padx=(10, 5), pady=5)

    task_combo = ttk.Combobox(
        task_frame,
        textvariable=manager.task_var,
        values=manager.all_tasks,
        font=theme["label_font"],
        state="normal"
    )
    manager.task_entry_widget = task_combo
    task_combo.grid(row=0, column=1, sticky="ew", padx=(0, 10), pady=5)
    # … filtering logic …
    task_combo.bind(
        "<<ComboboxSelected>>",
        lambda e: manager.on_task_fetched(manager.task_var.get())
    )
    if hasattr(manager, "_just_cleared_task") and manager._just_cleared_task:
        task_combo.focus_set()
        manager._just_cleared_task = False

    # 5: Subtask panel (optional)
    subtask_container = render_subtask_panel(frame, manager)
    subtask_container.grid(row=5, column=0, sticky="nsew")  # ✅ Move it down

    # filter on each key release
    def _filter(evt=None):
        q = manager.task_var.get().lower()
        matches = [t for t in manager.all_tasks if t.lower().startswith(q)]
        task_combo["values"] = matches[:6]

    task_combo.bind("<KeyRelease>", _filter)

    #   Sessions spinbox
    tk.Label(
        task_frame,
        text="Sessions:",
        font=theme["label_font"],
        bg=theme["bg_color"]
    ).grid(row=1, column=0, sticky="ew", padx=(10, 5), pady=5)
    tk.Spinbox(
        task_frame,
        from_=1, to=10,
        textvariable=manager.task_session_goal,

    ).grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=5)
