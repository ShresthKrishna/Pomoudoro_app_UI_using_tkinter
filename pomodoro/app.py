import tkinter as tk
from pomodoro.theme import theme
from screens.navigation import create_navigation, create_bottom_controls
from screens.layout import create_all_screens
from core.session_manager import SessionManager

def run_app():
    root = tk.Tk()
    # DPI / HiDPI awareness:
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(2)
    except:
        pass
    root.tk.call('tk', 'scaling', 1.5)

    root.title("Pomodoro Productivity Timer")
    root.geometry("400x600")
    root.minsize(500, 800)
    root.config(bg=theme["bg_color"])

    # Allow the single column to stretch:
    root.columnconfigure(0, weight=1)
    # Layout rows: nav (fixed), main (expand), bottom (fixed)
    root.rowconfigure(0, weight=0)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=0)

    session_manager = SessionManager(root)

    # Top nav:
    top_frame = tk.Frame(root, bg=theme["bg_color"])
    top_frame.columnconfigure((0, 1, 2), weight=1)
    top_frame.rowconfigure(0, weight=1)
    top_frame.grid(row=0, column=0, sticky="ew")
    create_navigation(top_frame, session_manager.show_frame)

    # Main content:
    middle_frame = tk.Frame(root, bg=theme["bg_color"])
    middle_frame.grid(row=1, column=0, sticky="nsew", pady=10)
    middle_frame.columnconfigure(0, weight=1)
    middle_frame.rowconfigure(0, weight=1)

    # Bottom controls:
    bottom_frame = tk.Frame(root, bg=theme["bg_color"])
    bottom_frame.grid(row=2, column=0, sticky="ew", pady=10)
    bottom_frame.columnconfigure((0, 1, 2), weight=1)
    bottom_frame.rowconfigure(0, weight=1)

    create_bottom_controls(bottom_frame, session_manager)

    # Screens setup:
    frames = create_all_screens(middle_frame, session_manager)
    session_manager.register_screens(frames)

    # Resume any existing session & start the tick loop:
    session_manager.resume_if_possible()
    session_manager.start_tick_loop()
    session_manager.show_frame("home")

    root.mainloop()

if __name__ == "__main__":
    run_app()
