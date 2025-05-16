# app.py (Post-Split)
import tkinter as tk
from pomodoro.theme import theme
from screens.navigation import create_navigation
from screens.layout import create_all_screens
from core.session_manager import SessionManager
from screens.navigation import create_bottom_controls

def run_app():
    root = tk.Tk()
    root.title("Pomodoro Productivity Timer")
    root.geometry("400x600")
    root.minsize(300, 400)
    root.config(bg=theme["bg_color"])

    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)

    # Create screen container
    middle_frame = tk.Frame(root, bg=theme["bg_color"])
    middle_frame.grid(row=1, column=0, sticky="nsew", pady=10)
    middle_frame.rowconfigure(0, weight=1)
    middle_frame.columnconfigure(0, weight=1)

    session_manager = SessionManager(root)

    # Navigation bar (row 0)
    create_navigation(root, session_manager.show_frame)
    create_bottom_controls(root, session_manager)

    # Screens (row 1)
    frames = create_all_screens(middle_frame, session_manager)
    session_manager.register_screens(frames)

    session_manager.resume_if_possible()
    session_manager.start_tick_loop()
    session_manager.show_frame("home")

    root.mainloop()

if __name__ == "__main__":
    run_app()
