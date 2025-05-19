import tkinter as tk
from screens.home_screen import render_home_screen
from screens.settings_screen import render_settings_screen
from screens.analytics_screen import render_analytics_screen
from pomodoro.theme import theme

def create_all_screens(parent, session_manager):
    frames = {}

    parent.rowconfigure(0, weight=1)
    parent.columnconfigure(0, weight=1)
    for name in ("home", "settings","analytics"):
        frame = tk.Frame(parent, bg=theme["bg_color"])
        frame.grid(row=0, column=0, sticky="nsew")
        # Correctly apply weight to column 0
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.grid_propagate(True)
        frames[name] = frame

    render_home_screen(frames["home"], session_manager)
    render_settings_screen(frames["settings"], session_manager)
    render_analytics_screen(frames["analytics"], use_mock=True)

    return frames
