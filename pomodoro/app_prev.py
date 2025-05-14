import tkinter as tk
from pomodoro.timer_engine import TimerEngine  # Import the modular timer engine
from datetime import datetime
from pomodoro.logger import log_session
# Central theme dictionary to manage styles in one place
from pomodoro.theme import theme
from screens.analytics_screen import render_analytics_screen
from utils.storage import save_user_settings, load_user_settings
from pomodoro.timer_state_manager import save_timer_state, load_timer_state, clear_timer_state
from tkinter import messagebox


def run_app():
    # Set up the main application window
    root = tk.Tk()
    root.title("Pomodoro Productivity Timer")
    root.geometry("400x600")
    root.minsize(300, 400)
    root.config(bg=theme["bg_color"])

    # Define layout structure: top, middle, and bottom rows
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)

    # Top frame holds the navigation buttons
    top_frame = tk.Frame(root, bg=theme["bg_color"])
    top_frame.grid(row=0, column=0, sticky="ew", pady=10)
    top_frame.columnconfigure((0, 1, 2), weight=1)

    home_btn = tk.Button(top_frame,
                         text="Home",
                         bg=theme["button_color"],
                         font=theme["button_font"],
                         command=lambda: show_frame("home"))
    settings_btn = tk.Button(top_frame,
                             text="Settings",
                             font=theme["button_font"],
                             bg=theme["button_color"],
                             command=lambda: show_frame("settings"))
    analytics_btn = tk.Button(top_frame,
                              text="Analytics",
                              bg=theme["button_color"],
                              font=theme["button_font"],
                              command=lambda: show_frame("analytics"))

    home_btn.grid(row=0, column=0, sticky="ew", padx=20)
    settings_btn.grid(row=0, column=1, sticky="ew", padx=20)
    analytics_btn.grid(row=0, column=2, sticky="ew", padx=20)

    # Middle frame displays the currently active screen
    middle_frame = tk.Frame(root, bg=theme["bg_color"])
    middle_frame.grid(row=1, column=0, sticky="nsew", pady=10)
    middle_frame.rowconfigure(0, weight=1)
    middle_frame.columnconfigure(0, weight=1)

    # Shared UI state variables
    global timer_label
    timer_label = None
    session_type_var = tk.StringVar(value="Work")
    session_logs = []
    session_start_time = None
    use_mock_data = True
    task_var = tk.StringVar()
    task_session_goal = tk.IntVar(value=1)

    session_counts = {
        "Work": 0,
        "Short Break": 0,
        "Long Break": 0
    }

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

    saved_settings = load_user_settings()
    for key in duration_vars:
        if key in saved_settings:
            duration_vars[key].set(saved_settings[key])
    # Dictionary to store the different screen frames
    frames = {}

    for screen in ("home", "settings", "analytics"):
        frame = tk.Frame(middle_frame, bg=theme["bg_color"])
        frame.grid(row=0, column=0, sticky="nsew")
        # frame.rowconfigure((0, 1, 2, 3), weight=1)
        if screen == "analytics":
            frame.rowconfigure(0, weight=1)  # analytics uses just 1 row
        else:
            frame.rowconfigure((0, 1, 2, 3), weight=1)  # home/settings use 4 rows
        frame.columnconfigure(0, weight=1)

        if screen == "home":
            tk.Label(frame, text="Session Type", bg=theme["bg_color"], font=theme["label_font"]).grid(
                row=0, column=0, sticky="ew", padx=20, pady=5
            )

            tk.OptionMenu(frame, session_type_var, "Work", "Short Break", "Long Break").grid(
                row=1, column=0, padx=20, sticky="ew"
            )

            timer_label = tk.Label(frame, text="00:00", font=theme["timer_font"], bg=theme["bg_color"])
            timer_label.grid(row=2, column=0, pady=10)

            session_label = tk.Label(frame, text="Work Session 1", font=theme["label_font"], bg=theme["bg_color"])
            session_label.grid(row=3, column=0, pady=5)

        elif screen == "settings":

            # Make both columns grow evenly
            frame.columnconfigure((0, 1), weight=1)
            settings_box = tk.LabelFrame(frame, text="Customize Durations", font=theme["label_font"],
                                         bg=theme["bg_color"], bd=2)
            settings_box.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
            settings_box.columnconfigure((0, 1), weight=1)

            labels = {
                "Work": "Work Duration (min)",
                "Short Break": "Break Duration (min)",
                "Long Break": "Long Break Duration (min)"
            }

            for i, key in enumerate(labels):
                # Label column
                tk.Label(settings_box, text=labels[key], font=theme["label_font"], bg=theme["bg_color"],fg="black").grid(
                    row=i, column=0, padx=10, pady=10, sticky="w"
                )
                # Spinbox column
                tk.Spinbox(
                    settings_box,
                    from_=1, to=60,
                    textvariable=duration_vars[key],
                    font=theme["label_font"],
                    width=8
                ).grid(row=i, column=1, padx=10, pady=10, sticky="e", ipady=3)

            # Save Settings button (placeholder)

            save_btn = tk.Button(
                frame, text="Save Settings",
                bg=theme["accent_color"],
                font=theme["button_font"],
                command= on_save_settings)
            save_btn.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        elif screen == "analytics":
            render_analytics_screen(frame, use_mock=use_mock_data)
        frames[screen] = frame

    # Callback: updates the timer label every second
    def update_display_cb(mins, secs):
        timer_label.config(text=f"{mins:02d}:{secs:02d}")

    # Callback: handles session completion and switching
    def session_complete_cb(prev_session, count):
        nonlocal session_start_time
        completed_at = datetime.now()
        duration_minutes = round((completed_at - session_start_time).total_seconds() / 60 if session_start_time else 0)
        session_logs.append({
            "type": prev_session,
            "completed_at": completed_at.strftime("%Y-%m-%d %H:%M:%S"),
            "session_number": count,
            "duration_minutes" : duration_minutes
        })
        if prev_session == "Work":
            next_session = "Long Break" if count % 4 == 0 else "Short Break"
        else:
            next_session = "Work"
        log_session(prev_session, completed_at, count, duration_minutes, task=task_var.get().strip())
        clear_timer_state()
        session_type_var.set(next_session)
        timer_engine.start(next_session)

    # Instantiate the timer engine
    timer_engine = TimerEngine(
        update_display_cb,
        session_complete_cb,
        {key: duration_vars[key].get() * 60 for key in duration_vars}
    )
    # Set up the recurring tick loop

    def resume_from_saved_state():
        state = load_timer_state()
        if not state:
            return False

        remaining = state["remaining_seconds"]
        mins, secs = divmod(remaining, 60)
        summary = f"{state['session_type']} – {mins}:{secs:02} remaining on '{state['task']}'"

        if messagebox.askyesno("Resume Session?", f"Resume your last session:\n{summary}?"):
            task_var.set(state["task"])
            task_session_goal.set(state["task_sessions_remaining"])
            session_type_var.set(state["session_type"])
            for k in state["session_counts"]:
                session_counts[k] = state["session_counts"][k]
            timer_engine.start_from(remaining, state["session_type"])
            return True
        return False

    def on_start():
        timer_engine.update_durations({key: duration_vars[key].get() * 60 for key in duration_vars})
        session_type = session_type_var.get()
        timer_engine.start(session_type)

        save_timer_state({
            "active": True,
            "session_type": session_type,
            "remaining_seconds": timer_engine.remaining,
            "session_counts": session_counts,
            "task": task_var.get().strip(),
            "task_sessions_remaining": task_session_goal.get(),
            "timestamp": datetime.now().isoformat()
        })

    def tick_loop():
        timer_engine.tick()
        root.after(1000, tick_loop)

    resume_from_saved_state()
    tick_loop()

    is_paused = False

    def toggle_pause():
        nonlocal is_paused
        save_timer_state({
            "active": True,
            "session_type": timer_engine.session_type,
            "remaining_seconds": timer_engine.remaining,
            "session_counts": session_counts,
            "task": task_var.get().strip(),
            "task_sessions_remaining": task_session_goal.get(),
            "timestamp": datetime.now().isoformat()
        })

        if is_paused:
            timer_engine.resume()
            pause_btn.config(text="Pause")
            is_paused = False
        else:
            timer_engine.pause()
            pause_btn.config(text="Resume")
            is_paused = True

    def on_reset():
        timer_engine.reset()
        clear_timer_state()

    # Bottom control panel with Start / Pause / Reset buttons
    bottom_frame = tk.Frame(root, bg=theme["bg_color"])
    bottom_frame.grid(row=2, column=0, sticky="ew", pady=10)
    bottom_frame.columnconfigure((0, 1, 2), weight=1)

    start_btn = tk.Button(bottom_frame,
                          text="Start",
                          bg=theme["accent_color"],
                          font=theme["button_font"],
                          command=on_start)
    pause_btn = tk.Button(bottom_frame, text="Pause", bg=theme["button_color"], font=theme["button_font"],
                          command=toggle_pause)

    reset_btn = tk.Button(bottom_frame, text="Reset", bg=theme["button_color"], font=theme["button_font"],
                          command=on_reset)

    start_btn.grid(row=0, column=0, padx=10, sticky="ew")
    pause_btn.grid(row=0, column=1, padx=10, sticky="ew")
    reset_btn.grid(row=0, column=2, padx=10, sticky="ew")

    # Function to show a screen by raising it to the front
    def show_frame(name):
        frames[name].tkraise()

    show_frame("home")
    root.mainloop()
