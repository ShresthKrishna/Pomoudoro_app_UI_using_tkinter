import tkinter as tk
from pomodoro.theme import theme

def create_navigation(parent, show_frame_callback):
    top_frame = tk.Frame(parent, bg=theme["bg_color"])
    top_frame.grid(row=0, column=0, sticky="ew", pady=10)
    top_frame.columnconfigure((0, 1, 2), weight=1)

    for i, label in enumerate(["Home", "Settings", "Analytics"]):
        tk.Button(
            top_frame,
            text=label,
            bg=theme["button_color"],
            font=theme["button_font"],
            command=lambda name=label.lower(): show_frame_callback(name)
        ).grid(row=0, column=i, padx=20, sticky="ew")


def create_bottom_controls(parent, manager):
    bottom_frame = tk.Frame(parent, bg=theme["bg_color"])
    bottom_frame.grid(row=2, column=0, sticky="ew", pady=10)
    bottom_frame.columnconfigure((0, 1, 2), weight=1)

    def toggle():
        manager.toggle_pause(pause_btn)

    start_btn = tk.Button(
        bottom_frame, text="Start",
        bg=theme["accent_color"], font=theme["button_font"],
        command=manager.on_start
    )
    pause_btn = tk.Button(
        bottom_frame, text="Pause",
        bg=theme["button_color"], font=theme["button_font"],
        command=toggle
    )
    reset_btn = tk.Button(
        bottom_frame, text="Reset",
        bg=theme["button_color"], font=theme["button_font"],
        command=manager.reset_session
    )

    start_btn.grid(row=0, column=0, padx=10, sticky="ew")
    pause_btn.grid(row=0, column=1, padx=10, sticky="ew")
    reset_btn.grid(row=0, column=2, padx=10, sticky="ew")
