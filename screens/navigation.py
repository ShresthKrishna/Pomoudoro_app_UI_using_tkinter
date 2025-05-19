import tkinter as tk
from pomodoro.theme import theme

def create_navigation(parent, show_frame_callback):
    # parent is already the top_frame you grid’ed in app.py
    parent.rowconfigure(0, weight=1)
    parent.columnconfigure(0, weight=1)

    for i, label in enumerate(["Home", "Settings","Analytics"]):
        btn = tk.Button(
            parent,
            text=label,
            bg=theme["button_color"],
            font=theme["button_font"],
            command=lambda name=label.lower(): show_frame_callback(name)
        )
        btn.grid(row=0, column=i, sticky="nsew", padx=20, pady=10)


def create_bottom_controls(parent, manager):
    parent.rowconfigure(0, weight=1)
    parent.columnconfigure(0, weight=1)
    # we need a stable ref for the Pause button so toggle_pause can update its text
    pause_btn = None

    # Start
    start_btn = tk.Button(
        parent,
        text="Start",
        bg=theme["accent_color"],
        font=theme["button_font"],
        command=manager.on_start
    )
    start_btn.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Pause / Resume
    def _toggle():
        manager.toggle_pause(pause_btn)
    pause_btn = tk.Button(
        parent,
        text="Pause",
        bg=theme["button_color"],
        font=theme["button_font"],
        command=_toggle
    )
    pause_btn.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # Reset
    reset_btn = tk.Button(
        parent,
        text="Reset",
        bg=theme["button_color"],
        font=theme["button_font"],
        command=manager.reset_session
    )
    reset_btn.grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
