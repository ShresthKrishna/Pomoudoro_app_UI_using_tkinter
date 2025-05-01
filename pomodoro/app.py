import tkinter as tk

theme = {
    "bg_color": '#f7f5dd',
    "button_color": "#9bdeac",
    "font_name": "Courier"
}

def run_app():
    # 1. Create Tkinter root window
    root = tk.Tk()

    # 2. Set title, geometry, minimum size
    root.title("Pomodoro Productivity Timer")
    root.geometry("400x600")
    root.minsize(300, 400)
    root.config(bg=theme["bg_color"])

    # 3. Configure grid (rows, columns)
    root.rowconfigure(index=1, weight=1)
    root.columnconfigure(index=0, weight=1)

    # 4. Create Top Frame (for Work/Break settings)
    top_frame = tk.Frame(root, bg=theme["bg_color"])
    top_frame.grid(row=0, column=0, sticky="ew", pady=10)

    # 4.1 Create Buttons in the Top Frame
    home_btn = tk.Button(top_frame, text="Home", bg=theme["button_color"], command=lambda: show_frame("home"))
    settings_btn = tk.Button(top_frame, text="Settings", bg=theme["button_color"], command=lambda: show_frame("settings"))
    analytics_button = tk.Button(top_frame, text="Analytics", bg=theme["button_color"], command=lambda: show_frame("analytics"))

    home_btn.pack(side="left", expand=True, padx=5)
    settings_btn.pack(side="left", expand=True, padx=5)
    analytics_button.pack(side="left", expand=True, padx=5)

    # 5. Create Middle Frame (for Timer + Tomato)
    middle_frame = tk.Frame(root, bg=theme["bg_color"])
    middle_frame.grid(row=1, column=0, sticky="nsew", pady=10)
    middle_frame.rowconfigure(0, weight=1)
    middle_frame.columnconfigure(0, weight=1)

    # 5.1 Sub-Frames
    frames = {}
    for screen in ("home", "settings", "analytics"):
        frame = tk.Frame(middle_frame, bg=theme["bg_color"])
        frame.rowconfigure(0, weight=1)
        frame.columnconfigure(0, weight=1)

        label = tk.Label(
            frame,
            text=f"This is the {screen.capitalize()} Screen",
            font=(theme["font_name"], 20),
            bg=theme["bg_color"],
            anchor="center",
            justify="center"
        )
        label.grid(row=0, column=0, sticky="nsew")

        frame.grid(row=0, column=0, sticky="nsew")
        frames[screen] = frame

    # 6. Create Bottom Frame (for Start/Pause/Reset and Checkmarks)
    bottom_frame = tk.Frame(root, bg=theme["bg_color"])
    bottom_frame.grid(row=2, column=0, sticky="ew", pady=10)
    tk.Label(bottom_frame, text="(bottom area)", bg=theme["bg_color"]).pack()

    # 7. Function to raise the appropriate frame
    def show_frame(name):
        frames[name].tkraise()

    # 8. Start Tkinter mainloop
    show_frame("home")
    root.mainloop()
