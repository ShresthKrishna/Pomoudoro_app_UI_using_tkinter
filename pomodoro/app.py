import tkinter as tk
from tkinter import ttk
from pomodoro.timer_engine import TimerEngine
from datetime import datetime
from pomodoro.logger import log_session
from pomodoro.theme import theme
from screens.analytics_screen import render_analytics_screen
from utils.storage import save_user_settings, load_user_settings
from pomodoro.task_memory import get_all_tasks, update_task_memory


def run_app():
    root = tk.Tk()
    root.title("Pomodoro Productivity Timer")
    root.geometry("400x600")
    root.minsize(300, 400)
    root.config(bg=theme["bg_color"])

    # Layout configuration
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)

    # Top navigation
    top_frame = tk.Frame(root, bg=theme["bg_color"])
    top_frame.grid(row=0, column=0, sticky="ew", pady=10)
    top_frame.columnconfigure((0, 1, 2), weight=1)

    home_btn = tk.Button(
        top_frame, text="Home",
        bg=theme["button_color"], font=theme["button_font"],
        command=lambda: show_frame("home")
    )
    settings_btn = tk.Button(
        top_frame, text="Settings",
        bg=theme["button_color"], font=theme["button_font"],
        command=lambda: show_frame("settings")
    )
    analytics_btn = tk.Button(
        top_frame, text="Analytics",
        bg=theme["button_color"], font=theme["button_font"],
        command=lambda: show_frame("analytics")
    )
    home_btn.grid(row=0, column=0, sticky="ew", padx=20)
    settings_btn.grid(row=0, column=1, sticky="ew", padx=20)
    analytics_btn.grid(row=0, column=2, sticky="ew", padx=20)

    # Middle frame for screens
    middle_frame = tk.Frame(root, bg=theme["bg_color"])
    middle_frame.grid(row=1, column=0, sticky="nsew", pady=10)
    middle_frame.rowconfigure(0, weight=1)
    middle_frame.columnconfigure(0, weight=1)

    # Shared state
    timer_label = None
    session_label = None
    session_type_var = tk.StringVar(value="Work")
    task_var = tk.StringVar(value="")
    task_session_goal = tk.IntVar(value=1)
    session_counts = {"Work": 0, "Short Break": 0, "Long Break": 0}
    session_start_time = None
    use_mock_data = True
    current_task = ""
    task_session_remaining = 0

    duration_vars = {
        "Work": tk.IntVar(value=25),
        "Short Break": tk.IntVar(value=5),
        "Long Break": tk.IntVar(value=15)
    }

    def on_save_settings():
        save_user_settings({
            "Work": duration_vars["Work"].get(),
            "Short Break": duration_vars["Short Break"].get(),
            "Long Break": duration_vars["Long Break"].get()
        })
        timer_engine.update_durations({
            key: duration_vars[key].get() * 60 for key in duration_vars
        })

    saved = load_user_settings()
    for k in duration_vars:
        if k in saved:
            duration_vars[k].set(saved[k])

    # Prepare frames
    frames = {}
    for screen in ("home", "settings", "analytics"):
        frame = tk.Frame(middle_frame, bg=theme["bg_color"])
        frame.grid(row=0, column=0, sticky="nsew")
        if screen == "analytics":
            frame.rowconfigure(0, weight=1)
        else:
            frame.rowconfigure((0, 1, 2, 3, 4,5), weight=1)
        frame.columnconfigure(0, weight=1)

        if screen == "home":
            # Session type selector
            tk.Label(
                frame, text="Session Type",
                bg=theme["bg_color"], font=theme["label_font"]
            ).grid(row=0, column=0, sticky="ew", padx=20, pady=5)
            tk.OptionMenu(
                frame, session_type_var, "Work", "Short Break", "Long Break"
            ).grid(row=1, column=0, padx=20, sticky="ew")

            # Timer display
            timer_label = tk.Label(
                frame, text="00:00",
                font=theme["timer_font"], bg=theme["bg_color"]
            )
            timer_label.grid(row=2, column=0, pady=10)

            # Session label
            session_label = tk.Label(
                frame, text="Work Session 1",
                font=theme["label_font"], bg=theme["bg_color"]
            )
            session_label.grid(row=3, column=0, pady=5)

            # Task entry
            all_tasks = get_all_tasks()  # Loaded once on app launch

            # Task input with suggestions
            task_frame = tk.LabelFrame(
                frame, text="Task",
                font=theme["label_font"], bg=theme["bg_color"]
            )
            task_frame.grid(row=4, column=0, sticky="ew", padx=20, pady=10)
            task_frame.columnconfigure(0, weight=1)

            task_combobox = ttk.Combobox(
                task_frame, textvariable=task_var,
                values=all_tasks, font=theme["label_font"]
            )
            task_combobox.grid(row=0, column=0, sticky="ew", padx=10, pady=5)
            task_combobox.set("")

            # Dynamic dropdown filtering
            def filter_task_suggestions(event=None):
                query = task_var.get().lower()
                matches = [t for t in all_tasks if t.lower().startswith(query)]
                task_combobox["values"] = matches[:6]

            task_combobox.bind("<KeyRelease>", filter_task_suggestions)
            # Task Plan
            task_plan_frame = tk.LabelFrame(
                frame, text="Task Plan",
                font = theme["label_font"],
                bg=theme["bg_color"]
            )
            task_plan_frame.grid(row=5, column=0, sticky="ew", padx=20, pady=(5, 10))
            task_plan_frame.columnconfigure(0, weight=1)

            tk.Label(task_plan_frame,
                     text="Planned Work Sessions:",
                     font=theme["label_font"],
                     bg=theme["bg_color"]).grid(row=0, column=0, sticky="w",
                                                padx=10, pady=5)

            tk.Spinbox(task_plan_frame,
                       from_=1, to=10,
                       textvariable = task_session_goal,
                       font=theme["label_font"],
                       width=5).grid(row=0, column=1, sticky="w", padx=10, pady=5)

        elif screen == "settings":
            frame.columnconfigure((0, 1), weight=1)
            settings_box = tk.LabelFrame(
                frame, text="Customize Durations",
                font=theme["label_font"], bg=theme["bg_color"], bd=2
            )
            settings_box.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
            settings_box.columnconfigure((0, 1), weight=1)

            labels = {
                "Work": "Work Duration (min)",
                "Short Break": "Short Break Duration (min)",
                "Long Break": "Long Break Duration (min)"
            }
            for i, key in enumerate(labels):
                tk.Label(
                    settings_box, text=labels[key],
                    font=theme["label_font"], bg=theme["bg_color"]
                ).grid(row=i, column=0, sticky="w", padx=10, pady=10)
                tk.Spinbox(
                    settings_box, from_=1, to=60,
                    textvariable=duration_vars[key],
                    font=theme["label_font"], width=8
                ).grid(row=i, column=1, sticky="e", padx=10, pady=10)

            tk.Button(
                frame, text="Save Settings",
                bg=theme["accent_color"], font=theme["button_font"],
                command=on_save_settings
            ).grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        else:  # analytics
            render_analytics_screen(frame, use_mock=use_mock_data)

        frames[screen] = frame

    # Callback to update timer display
    def update_display_cb(mins, secs):
        timer_label.config(text=f"{mins:02d}:{secs:02d}")

    # Session completion handler
    def session_complete_cb(prev_session, _):
        nonlocal session_start_time, current_task, task_session_remaining
        completed_at = datetime.now()
        duration = round((completed_at - session_start_time).total_seconds() / 60)

        # Increment count for prev_session
        session_counts[prev_session] += 1

        if prev_session == "Work" and current_task:
            task_session_remaining -=1
            log_session(prev_session, completed_at, session_counts[prev_session],
                        duration, current_task)
        else:
            log_session(prev_session, completed_at, session_counts[prev_session],
                        duration, "")

        if task_session_remaining == 0:
            task_var.set("")
            task_session_goal.set(1)
            current_task = ""

        # Determine next session type
        if prev_session == "Work":
            # every 4th work -> long break
            if session_counts["Work"] % 4 == 0:
                next_sess = "Long Break"
            else:
                next_sess = "Short Break"
        else:
            next_sess = "Work"

        # Update label for the upcoming session
        session_label.config(
            text=f"{next_sess} Session {session_counts[next_sess] + 1}"
        )

        # Start next session
        session_start_time = datetime.now()
        session_type_var.set(next_sess)
        timer_engine.start(next_sess)

    # Instantiate timer engine
    timer_engine = TimerEngine(
        update_display_cb,
        session_complete_cb,
        {k: duration_vars[k].get() * 60 for k in duration_vars}
    )

    # Start button
    def start_session():
        nonlocal session_start_time, current_task, task_session_remaining

        session_start_time = datetime.now()
        stype = session_type_var.get()

        current_task = task_var.get().strip()
        task_session_remaining = task_session_goal.get()
        if current_task:
            update_task_memory(current_task)
        session_label.config(
            text=f"{stype} Session {session_counts[stype] + 1}"
        )
        timer_engine.update_durations(
            {k: duration_vars[k].get() * 60 for k in duration_vars}
        )
        timer_engine.start(stype)

    # Tick loop
    def tick_loop():
        timer_engine.tick()
        root.after(10, tick_loop)

    # Control panel
    is_paused = False
    def toggle_pause():
        nonlocal is_paused
        if is_paused:
            timer_engine.resume()
            pause_btn.config(text="Pause")
        else:
            timer_engine.pause()
            pause_btn.config(text="Resume")
        is_paused = not is_paused

    bottom_frame = tk.Frame(root, bg=theme["bg_color"])
    bottom_frame.grid(row=2, column=0, sticky="ew", pady=10)
    bottom_frame.columnconfigure((0, 1, 2), weight=1)

    start_btn = tk.Button(
        bottom_frame, text="Start",
        bg=theme["accent_color"], font=theme["button_font"],
        command=start_session
    )
    pause_btn = tk.Button(
        bottom_frame, text="Pause",
        bg=theme["button_color"], font=theme["button_font"],
        command=toggle_pause
    )
    reset_btn = tk.Button(
        bottom_frame, text="Reset",
        bg=theme["button_color"], font=theme["button_font"],
        command=lambda: timer_engine.reset()
    )
    start_btn.grid(row=0, column=0, padx=10, sticky="ew")
    pause_btn.grid(row=0, column=1, padx=10, sticky="ew")
    reset_btn.grid(row=0, column=2, padx=10, sticky="ew")

    # Screen switching
    def show_frame(name):
        frames[name].tkraise()

    show_frame("home")
    tick_loop()
    root.mainloop()


if __name__ == "__main__":
    run_app()
