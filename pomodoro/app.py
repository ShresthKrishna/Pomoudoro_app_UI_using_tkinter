# app.py (Post-Split)
import tkinter as tk
from pomodoro.theme import theme
from screens.navigation import create_navigation
from screens.layout import create_all_screens
from core.session_manager import SessionManager
from screens.navigation import create_bottom_controls

def run_app():
    root = tk.Tk()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    root.tk.call('tk', 'scaling', 1.5)  # ~1.5 for HiDPI
    root.title("Pomodoro Productivity Timer")
    root.geometry("400x600")
    root.minsize(300, 400)
    root.config(bg=theme["bg_color"])

    # Layout rows
    root.rowconfigure(0, weight=0)  # Top nav
    root.rowconfigure(1, weight=1)  # Middle
    root.rowconfigure(2, weight=0)  # Bottom controls

    root.columnconfigure(0, weight=1)

    top_frame = tk.Frame(root, bg=theme["bg_color"])
    top_frame.rowconfigure(0, weight=1)
    top_frame.columnconfigure(0, weight=1)
    top_frame.grid(row=0, column=0, sticky="nsew")

    middle_frame = tk.Frame(root, bg=theme["bg_color"])
    middle_frame.grid(row=1, column=0, sticky="nsew", pady=10)
    middle_frame.rowconfigure(0, weight=1)
    middle_frame.columnconfigure(0, weight=1)

    bottom_frame = tk.Frame(root, bg=theme["bg_color"])
    bottom_frame.columnconfigure(0, weight=1)
    bottom_frame.rowconfigure(0, weight=1)
    bottom_frame.grid(row=2, column=0, sticky="ew", pady=10)

    session_manager = SessionManager(root)

    top_frame.config(highlightthickness=1, highlightbackground="red")
    middle_frame.config(highlightthickness=1, highlightbackground="blue")
    bottom_frame.config(highlightthickness=1, highlightbackground="green")

    # Navigation bar (row 0)
    create_navigation(top_frame, session_manager.show_frame)
    create_bottom_controls(bottom_frame, session_manager)

    # Screens (row 1)
    frames = create_all_screens(middle_frame, session_manager)
    session_manager.register_screens(frames)

    session_manager.resume_if_possible()
    session_manager.start_tick_loop()
    session_manager.show_frame("home")

    root.mainloop()

if __name__ == "__main__":
    run_app()
