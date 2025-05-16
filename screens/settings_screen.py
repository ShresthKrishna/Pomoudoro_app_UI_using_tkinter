import tkinter as tk
from pomodoro.theme import theme

def render_settings_screen(frame, manager):
    frame.columnconfigure((0, 1), weight=1)

    settings_box = tk.LabelFrame(
        frame, text="Customize Durations",
        font=theme["label_font"], bg=theme["bg_color"], bd=2
    )
    settings_box.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
    settings_box.columnconfigure((0, 1), weight=1)

    labels = {
        "Work": "Work Duration (min)",
        "Short Break": "Break Duration (min)",
        "Long Break": "Long Break Duration (min)"
    }

    for i, key in enumerate(labels):
        tk.Label(settings_box, text=labels[key], font=theme["label_font"], bg=theme["bg_color"], fg="black")\
            .grid(row=i, column=0, padx=10, pady=10, sticky="w")
        tk.Spinbox(settings_box, from_=1, to=60, textvariable=manager.duration_vars[key],
                   font=theme["label_font"], width=8)\
            .grid(row=i, column=1, padx=10, pady=10, sticky="e")

    tk.Button(frame, text="Save Settings", bg=theme["accent_color"], font=theme["button_font"],
              command=manager.save_settings)\
        .grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
