import tkinter as tk
from pomodoro.timer import TimerController  # Importing the timer logic

# Central theme dictionary to manage styles in one place
theme = {
    "bg_color": '#f7f5dd',
    "button_color": "#9bdeac",
    "font_name": "Courier",
    "button_font": ("Courier", 12, "bold"),
    "label_font": ("Courier", 14),
    "timer_font": ("Courier", 36, "bold"),
    "accent_color": "#e2979c"
}

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

    home_btn = tk.Button(top_frame, text="Home", bg=theme["button_color"], command=lambda: show_frame("home"))
    settings_btn = tk.Button(top_frame, text="Settings", bg=theme["button_color"], command=lambda: show_frame("settings"))
    analytics_btn = tk.Button(top_frame, text="Analytics", bg=theme["button_color"], command=lambda: show_frame("analytics"))

    home_btn.grid(row=0, column=0, sticky="ew", padx=20)
    settings_btn.grid(row=0, column=1, sticky="ew", padx=20)
    analytics_btn.grid(row=0, column=2, sticky="ew", padx=20)

    # Middle frame displays the currently active screen
    middle_frame = tk.Frame(root, bg=theme["bg_color"])
    middle_frame.grid(row=1, column=0, sticky="nsew", pady=10)
    middle_frame.rowconfigure(0, weight=1)
    middle_frame.columnconfigure(0, weight=1)

    # Shared state variables
    timer_label = None
    session_type_var = tk.StringVar(value="Work")

    # Dictionary to store the different screen frames
    frames = {}

    # Create each screen (home, settings, analytics)
    for screen in ("home", "settings", "analytics"):
        frame = tk.Frame(middle_frame, bg=theme["bg_color"])
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure((0, 1, 2, 3, 4), weight=1)
        frame.columnconfigure(0, weight=1)

        if screen == "home":
            # Home screen layout: session dropdown, timer label, session label
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
            options = ["Work Duration (min)", "Break Duration (min)", "Long Break Frequency"]
            for i, label_text in enumerate(options):
                tk.Label(frame, text=label_text, font=theme["label_font"], bg=theme["bg_color"]).grid(
                    row=i, column=0, pady=5, sticky="w", padx=20
                )
                tk.Spinbox(frame, from_=1, to=60, width=5).grid(row=i, column=1, padx=10, pady=5)

        elif screen == "analytics":
            tk.Label(frame, text="Your productivity trend will appear here!",
                     font=theme["label_font"], bg=theme["bg_color"]).grid(row=0, column=0, pady=20)

        frames[screen] = frame

    # Create an instance of the timer logic class
    timer = TimerController(root, timer_label, session_type_var)

    # Bottom control panel with Start / Pause / Reset buttons
    bottom_frame = tk.Frame(root, bg=theme["bg_color"])
    bottom_frame.grid(row=2, column=0, sticky="ew", pady=10)
    bottom_frame.columnconfigure((0, 1, 2), weight=1)

    is_paused = False  # Toggle flag

    def toggle_pause():
        nonlocal is_paused
        if is_paused:
            timer.resume()
            pause_btn.config(text="Pause")
            is_paused = False
        else:
            timer.pause()
            pause_btn.config(text="Resume")
            is_paused = True

    start_btn = tk.Button(bottom_frame, text="Start", bg=theme["accent_color"], font=theme["button_font"],
                          command=timer.start_countdown)
    pause_btn = tk.Button(bottom_frame, text="Pause", bg=theme["button_color"], font=theme["button_font"],
                          command=toggle_pause)
    reset_btn = tk.Button(bottom_frame, text="Reset", bg=theme["button_color"], font=theme["button_font"],
                          command=timer.reset)

    start_btn.grid(row=0, column=0, padx=10, sticky="ew")
    pause_btn.grid(row=0, column=1, padx=10, sticky="ew")
    reset_btn.grid(row=0, column=2, padx=10, sticky="ew")

    # Function to show a screen by raising it to the front
    def show_frame(name):
        frames[name].tkraise()

    show_frame("home")
    root.mainloop()
