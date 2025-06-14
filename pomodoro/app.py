import tkinter as tk
from pomodoro.theme import theme
from pomodoro.timer_state_manager import save_timer_state
from screens.navigation import create_navigation, create_bottom_controls
from screens.layout import create_all_screens
from engine.session_manager import SessionManager
from datetime import datetime


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

    def on_close():
        # Save minimal state if session is active
        if session_manager.timer_engine.is_running:
            save_timer_state({
                "active": True,
                "session_type": session_manager.session_type_var.get(),
                "remaining_seconds": session_manager.timer_engine.remaining,
                "session_counts": session_manager.session_counts,
                "task": session_manager.task_var.get().strip(),
                "task_sessions_remaining": session_manager.task_session_goal.get(),
                "timestamp": session_manager.session_start_time.isoformat()
                if session_manager.session_start_time else datetime.now().isoformat(),
                "interrupted": True
            })

        # ✅ Track daily focus time before quitting
        session_manager.log_daily_focus_summary()

        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_close)


    root.mainloop()



if __name__ == "__main__":
    run_app()
