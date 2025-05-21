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

    buttons = {}

    # Start/End shared button

    def on_start():
        manager.on_start()
        set_start_button_state("end")

    def on_end():
        manager.end_session()
        set_start_button_state("start")

    def set_start_button_state(state):
        if state=="start":
            buttons["start"].config(
                text="Start",
                bg=theme["button_start"]["bg"],
                fg=theme["button_start"]["fg"],
                command=on_start
            )
        elif state=="end":
            buttons["start"].config(
                text="End",
                bg=theme["button_end"]["bg"],
                fg=theme["button_end"]["fg"],
                command=on_end

            )
    # Start
    buttons["start"] = tk.Button(
        parent,
        text="Start",
        font=theme["button_font"],
        bg=theme["button_start"]["bg"],
        fg=theme["button_start"]["fg"],
        command=on_start
    )
    buttons["start"].grid(row=0, column=0, sticky="nsew",
                          padx=10, pady=10)
    # Pause / Resume
    def _toggle():
        manager.toggle_pause(buttons["pause"])
    buttons["pause"] = tk.Button(
        parent,
        text="Pause",
        bg=theme["button_color"],
        font=theme["button_font"],
        command=_toggle
    )
    buttons["pause"].grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

    # Reset
    def _reset():
        manager.reset_session()
        set_start_button_state("start")
    buttons["reset"] = tk.Button(
        parent,
        text="Reset",
        bg=theme["button_color"],
        font=theme["button_font"],
        command= _reset
    )
    buttons["reset"].grid(row=0, column=2, sticky="nsew", padx=10, pady=10)
    manager.set_start_button_state = set_start_button_state