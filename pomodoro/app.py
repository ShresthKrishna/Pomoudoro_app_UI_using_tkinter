import tkinter as tk
from pomodoro.timer_engine import TimerEngine  # Import the modular timer engine
from datetime import datetime
from pomodoro.logger import log_session
# Central theme dictionary to manage styles in one place
from pomodoro.theme import theme
from screens.analytics_screen import render_analytics_screen
from utils.storage import save_user_settings, load_user_settings


def run_app():
    # --- Setup root window ---
    root = tk.Tk()
    root.title("Pomodoro Productivity Timer")
    root.geometry("400x600")
    root.minsize(300, 400)
    root.config(bg=theme["bg_color"])
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)

    # --- Top navigation bar ---
    top_frame = tk.Frame(root, bg=theme["bg_color"])
    top_frame.grid(row=0, column=0, sticky="ew", pady=10)
    top_frame.columnconfigure((0, 1, 2), weight=1)

    home_btn = tk.Button(top_frame, text="Home", bg=theme["button_color"],
                         font=theme["button_font"], command=lambda: show_frame("home"))
    settings_btn = tk.Button(top_frame, text="Settings", bg=theme["button_color"],
                             font=theme["button_font"], command=lambda: show_frame("settings"))
    analytics_btn = tk.Button(top_frame, text="Analytics", bg=theme["button_color"],
                              font=theme["button_font"], command=lambda: show_frame("analytics"))

    home_btn.grid(row=0, column=0, padx=20, sticky="ew")
    settings_btn.grid(row=0, column=1, padx=20, sticky="ew")
    analytics_btn.grid(row=0, column=2, padx=20, sticky="ew")

    # --- Middle container for active screen ---
    middle_frame = tk.Frame(root, bg=theme["bg_color"])
    middle_frame.grid(row=1, column=0, sticky="nsew", pady=10)
    middle_frame.rowconfigure(0, weight=1)
    middle_frame.columnconfigure(0, weight=1)

    # --- Shared state and configuration ---
    global timer_label
    timer_label = None
    session_type_var = tk.StringVar(value="Work")
    session_start_time = None
    use_mock_data = True

    # Per-type session counters
    session_counts = {"Work": 0, "Short Break": 0, "Long Break": 0}
    work_sessions_completed = 0

    # Timer durations
    duration_vars = {
        "Work": tk.IntVar(value=25),
        "Short Break": tk.IntVar(value=5),
        "Long Break": tk.IntVar(value=15)
    }

    # --- Load saved user settings if available ---
    saved_settings = load_user_settings()
    for key in duration_vars:
        if key in saved_settings:
            duration_vars[key].set(saved_settings[key])

    def on_save_settings():
        save_user_settings({k: duration_vars[k].get() for k in duration_vars})
        timer_engine.update_durations({k: duration_vars[k].get() * 60 for k in duration_vars})

    # --- Create all app screens: home, settings, analytics ---
    frames = {}
    for screen in ("home", "settings", "analytics"):
        frame = tk.Frame(middle_frame, bg=theme["bg_color"])
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0 if screen == "analytics" else (0, 1, 2, 3), weight=1)
        frame.columnconfigure(0, weight=1)

        if screen == "home":
            # Dropdown to select session type
            tk.Label(frame, text="Session Type", bg=theme["bg_color"], font=theme["label_font"]).grid(
                row=0, column=0, sticky="ew", padx=20, pady=5)
            tk.OptionMenu(frame, session_type_var, "Work", "Short Break", "Long Break").grid(
                row=1, column=0, padx=20, sticky="ew")

            # Countdown timer label
            timer_label = tk.Label(frame, text="00:00", font=theme["timer_font"], bg=theme["bg_color"])
            timer_label.grid(row=2, column=0, pady=10)

            # Session label (e.g., Work Session 1)
            session_label = tk.Label(frame, text="Work Session 1", font=theme["label_font"], bg=theme["bg_color"])
            session_label.grid(row=3, column=0, pady=5)

        elif screen == "settings":
            # Settings form to customize durations
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
                tk.Label(settings_box, text=labels[key], font=theme["label_font"],
                         bg=theme["bg_color"], fg="black").grid(row=i, column=0, padx=10, pady=10, sticky="w")
                tk.Spinbox(settings_box, from_=1, to=60, textvariable=duration_vars[key],
                           font=theme["label_font"], width=8).grid(row=i, column=1, padx=10, pady=10, sticky="e")

            tk.Button(frame, text="Save Settings", bg=theme["accent_color"], font=theme["button_font"],
                      command=on_save_settings).grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        elif screen == "analytics":
            render_analytics_screen(frame, use_mock=use_mock_data)

        frames[screen] = frame

    # --- Timer update display callback ---
    def update_display_cb(mins, secs):
        timer_label.config(text=f"{mins:02d}:{secs:02d}")

    # --- Session complete callback ---
    def session_complete_cb(prev_session, count):
        nonlocal session_start_time, work_sessions_completed
        from datetime import datetime
        completed_at = datetime.now()
        duration_minutes = round((completed_at - session_start_time).total_seconds() / 60 if session_start_time else 0)

        session_counts[prev_session] += 1
        log_session(prev_session, completed_at, session_counts[prev_session], duration_minutes)

        # Decide next session type
        if prev_session == "Work":
            work_sessions_completed += 1
            next_session = "Long Break" if work_sessions_completed % 4 == 0 else "Short Break"
        else:
            next_session = "Work"

        session_type_var.set(next_session)
        session_label.config(text=f"{next_session} Session {session_counts[next_session] + 1}")
        timer_engine.start(next_session)

    # --- Initialize timer engine ---
    timer_engine = TimerEngine(
        update_display_cb,
        session_complete_cb,
        {key: duration_vars[key].get() * 60 for key in duration_vars}
    )

    # --- Main ticking loop (called every 1s) ---
    def tick_loop():
        timer_engine.tick()
        root.after(10, tick_loop)

    tick_loop()

    # --- Pause/Resume toggle logic ---
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

    def reset_session():
        nonlocal work_sessions_completed

        # Reset timer logic
        timer_engine.reset()

        # Reset all session counters
        for key in session_counts:
            session_counts[key] = 0

        # Reset work session tracker for long break logic
        work_sessions_completed = 0

        # Set back to default type
        session_type_var.set("Work")

        # Reset the label
        session_label.config(text="Work Session 1")

    # --- Bottom control buttons: Start, Pause, Reset ---
    bottom_frame = tk.Frame(root, bg=theme["bg_color"])
    bottom_frame.grid(row=2, column=0, sticky="ew", pady=10)
    bottom_frame.columnconfigure((0, 1, 2), weight=1)

    start_btn = tk.Button(bottom_frame, text="Start", bg=theme["accent_color"], font=theme["button_font"],
                          command=lambda: (
                              timer_engine.update_durations({k: duration_vars[k].get() * 60 for k in duration_vars}),
                              session_label.config(text=f"{session_type_var.get()} Session {session_counts[session_type_var.get()] + 1}"),
                              timer_engine.start(session_type_var.get())
                          ))
    pause_btn = tk.Button(bottom_frame, text="Pause", bg=theme["button_color"], font=theme["button_font"],
                          command=toggle_pause)
    reset_btn = tk.Button(
        bottom_frame,
        text="Reset",
        bg=theme["button_color"],
        font=theme["button_font"],
        command=reset_session
    )

    start_btn.grid(row=0, column=0, padx=10, sticky="ew")
    pause_btn.grid(row=0, column=1, padx=10, sticky="ew")
    reset_btn.grid(row=0, column=2, padx=10, sticky="ew")

    # --- Raise selected screen to top ---
    def show_frame(name):
        frames[name].tkraise()

    show_frame("home")
    root.mainloop()
