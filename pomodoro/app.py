import tkinter as tk
from pomodoro.timer_engine import TimerEngine  # Import the modular timer engine
from datetime import datetime
from pomodoro.logger import log_session
# Central theme dictionary to manage styles in one place
from pomodoro.theme import theme


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
                         command=lambda: show_frame("home"))
    settings_btn = tk.Button(top_frame,
                             text="Settings",
                             bg=theme["button_color"],
                             command=lambda: show_frame("settings"))
    analytics_btn = tk.Button(top_frame,
                              text="Analytics",
                              bg=theme["button_color"],
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

    duration_vars = {
        "Work": tk.IntVar(value=25),
        "Short Break": tk.IntVar(value=5),
        "Long Break": tk.IntVar(value=15)
     }

    # Dictionary to store the different screen frames
    frames = {}

    for screen in ("home", "settings", "analytics"):
        frame = tk.Frame(middle_frame, bg=theme["bg_color"])
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure((0, 1, 2, 3), weight=1)
        frame.columnconfigure(0, weight=1)

        if screen == "home":
            tk.Label(frame, text="Session Type", bg=theme["bg_color"], font=theme["label_font"]).grid(
                row=0, column=0, sticky="w", padx=20, pady=5
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
                "Long Break": "Long Break Duration (min)"  # renamed for clarity
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
                frame, text="Save Settings", bg=theme["accent_color"], font=theme["button_font"])
            save_btn.grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        elif screen == "analytics":
            tk.Label(frame, text="Your productivity trend will appear here!",
                     font=theme["label_font"], bg=theme["bg_color"]).grid(row=0, column=0, pady=20)

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
        log_session(prev_session, completed_at, count, duration_minutes)
        session_type_var.set(next_session)
        timer_engine.start(next_session)

    # Instantiate the timer engine
    timer_engine = TimerEngine(
        update_display_cb,
        session_complete_cb,
        {key: duration_vars[key].get() * 60 for key in duration_vars}
    )
    # Set up the recurring tick loop

    def tick_loop():
        timer_engine.tick()
        root.after(1000, tick_loop)

    tick_loop()

    is_paused = False

    def toggle_pause():
        nonlocal is_paused
        if is_paused:
            timer_engine.resume()
            pause_btn.config(text="Pause")
            is_paused = False
        else:
            timer_engine.pause()
            pause_btn.config(text="Resume")
            is_paused = True

    def start_session():
        nonlocal session_start_time
        session_start_time = datetime.now()
        timer_engine.update_durations({key: duration_vars[key].get()*60 for key in duration_vars})
        session_type_var.get()

    # Bottom control panel with Start / Pause / Reset buttons
    bottom_frame = tk.Frame(root, bg=theme["bg_color"])
    bottom_frame.grid(row=2, column=0, sticky="ew", pady=10)
    bottom_frame.columnconfigure((0, 1, 2), weight=1)

    start_btn = tk.Button(bottom_frame,
                          text="Start",
                          bg=theme["accent_color"],
                          font=theme["button_font"],
                          command=lambda: (
                              timer_engine.update_durations(
                                  {key: duration_vars[key].get() * 60 for key in duration_vars}),
                              timer_engine.start(session_type_var.get())
                          )
                          )
    pause_btn = tk.Button(bottom_frame, text="Pause", bg=theme["button_color"], font=theme["button_font"],
                          command=toggle_pause)

    reset_btn = tk.Button(bottom_frame, text="Reset", bg=theme["button_color"], font=theme["button_font"],
                          command=timer_engine.reset)

    start_btn.grid(row=0, column=0, padx=10, sticky="ew")
    pause_btn.grid(row=0, column=1, padx=10, sticky="ew")
    reset_btn.grid(row=0, column=2, padx=10, sticky="ew")

    # Function to show a screen by raising it to the front
    def show_frame(name):
        frames[name].tkraise()

    show_frame("home")
    root.mainloop()
