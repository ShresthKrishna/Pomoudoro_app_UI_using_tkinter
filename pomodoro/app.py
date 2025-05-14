import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from pomodoro.timer_engine import TimerEngine
from pomodoro.logger import log_session
from pomodoro.theme import theme
from screens.analytics_screen import render_analytics_screen
from utils.storage import save_user_settings, load_user_settings
from pomodoro.timer_state_manager import save_timer_state, load_timer_state, clear_timer_state

def run_app():
    root = tk.Tk()
    root.title("Pomodoro Productivity Timer")
    root.geometry("400x600")
    root.minsize(300, 400)
    root.config(bg=theme["bg_color"])
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)

    # --- Top Nav ---
    top_frame = tk.Frame(root, bg=theme["bg_color"])
    top_frame.grid(row=0, column=0, sticky="ew", pady=10)
    top_frame.columnconfigure((0, 1, 2), weight=1)

    def show_frame(name):
        frames[name].tkraise()

    tk.Button(top_frame, text="Home", bg=theme["button_color"], font=theme["button_font"], command=lambda: show_frame("home")).grid(row=0, column=0, padx=20, sticky="ew")
    tk.Button(top_frame, text="Settings", bg=theme["button_color"], font=theme["button_font"], command=lambda: show_frame("settings")).grid(row=0, column=1, padx=20, sticky="ew")
    tk.Button(top_frame, text="Analytics", bg=theme["button_color"], font=theme["button_font"], command=lambda: show_frame("analytics")).grid(row=0, column=2, padx=20, sticky="ew")

    middle_frame = tk.Frame(root, bg=theme["bg_color"])
    middle_frame.grid(row=1, column=0, sticky="nsew", pady=10)
    middle_frame.rowconfigure(0, weight=1)
    middle_frame.columnconfigure(0, weight=1)

    session_type_var = tk.StringVar(value="Work")
    task_var = tk.StringVar()
    task_session_goal = tk.IntVar(value=1)
    session_counts = {"Work": 0, "Short Break": 0, "Long Break": 0}
    work_sessions_completed = 0
    session_start_time = None

    duration_vars = {"Work": tk.IntVar(value=25), "Short Break": tk.IntVar(value=5), "Long Break": tk.IntVar(value=15)}

    saved_settings = load_user_settings()
    for key in duration_vars:
        if key in saved_settings:
            duration_vars[key].set(saved_settings[key])

    def on_save_settings():
        save_user_settings({k: duration_vars[k].get() for k in duration_vars})
        timer_engine.update_durations({k: duration_vars[k].get() * 60 for k in duration_vars})

    frames = {}
    global timer_label, session_label
    for screen in ("home", "settings", "analytics"):
        frame = tk.Frame(middle_frame, bg=theme["bg_color"])
        frame.grid(row=0, column=0, sticky="nsew")
        frame.rowconfigure(0 if screen == "analytics" else (0, 1, 2, 3, 4, 5), weight=1)
        frame.columnconfigure(0, weight=1)

        if screen == "home":
            tk.Label(frame, text="Session Type", bg=theme["bg_color"], font=theme["label_font"]).grid(row=0, column=0, sticky="ew", padx=20, pady=5)
            tk.OptionMenu(frame, session_type_var, "Work", "Short Break", "Long Break").grid(row=1, column=0, padx=20, sticky="ew")

            timer_label = tk.Label(frame, text="00:00", font=theme["timer_font"], bg=theme["bg_color"])
            timer_label.grid(row=2, column=0, pady=10)

            session_label = tk.Label(frame, text="Work Session 1", font=theme["label_font"], bg=theme["bg_color"])
            session_label.grid(row=3, column=0, pady=5)

            task_frame = tk.LabelFrame(frame, text="Task Plan", font=theme["label_font"], bg=theme["bg_color"])
            task_frame.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
            task_frame.columnconfigure(1, weight=1)

            tk.Label(task_frame, text="Task Name:", font=theme["label_font"], bg=theme["bg_color"]).grid(row=0, column=0, sticky="w")
            tk.Entry(task_frame, textvariable=task_var).grid(row=0, column=1, sticky="ew")

            tk.Label(task_frame, text="Sessions:", font=theme["label_font"], bg=theme["bg_color"]).grid(row=1, column=0, sticky="w")
            tk.Spinbox(task_frame, from_=1, to=10, textvariable=task_session_goal).grid(row=1, column=1, sticky="ew")

        elif screen == "settings":
            frame.columnconfigure((0, 1), weight=1)
            settings_box = tk.LabelFrame(frame, text="Customize Durations", font=theme["label_font"], bg=theme["bg_color"], bd=2)
            settings_box.grid(row=0, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
            settings_box.columnconfigure((0, 1), weight=1)

            labels = {"Work": "Work Duration (min)", "Short Break": "Break Duration (min)", "Long Break": "Long Break Duration (min)"}

            for i, key in enumerate(labels):
                tk.Label(settings_box, text=labels[key], font=theme["label_font"], bg=theme["bg_color"], fg="black").grid(row=i, column=0, padx=10, pady=10, sticky="w")
                tk.Spinbox(settings_box, from_=1, to=60, textvariable=duration_vars[key], font=theme["label_font"], width=8).grid(row=i, column=1, padx=10, pady=10, sticky="e")

            tk.Button(frame, text="Save Settings", bg=theme["accent_color"], font=theme["button_font"], command=on_save_settings).grid(row=1, column=0, columnspan=2, padx=20, pady=20, sticky="ew")

        elif screen == "analytics":
            render_analytics_screen(frame, use_mock=True)

        frames[screen] = frame

    def update_display_cb(mins, secs):
        timer_label.config(text=f"{mins:02d}:{secs:02d}")

    def session_complete_cb(prev_session, count):
        nonlocal session_start_time, work_sessions_completed
        completed_at = datetime.now()
        duration_minutes = round((completed_at - session_start_time).total_seconds() / 60 if session_start_time else 0)

        session_counts[prev_session] += 1
        log_session(prev_session, completed_at, session_counts[prev_session], duration_minutes, task=task_var.get().strip())

        if prev_session == "Work":
            work_sessions_completed += 1
            next_session = "Long Break" if work_sessions_completed % 4 == 0 else "Short Break"
            if task_session_goal.get() <= 1:
                task_var.set("")
                task_session_goal.set(1)
            else:
                task_session_goal.set(task_session_goal.get() - 1)
        else:
            next_session = "Work"

        session_type_var.set(next_session)
        session_label.config(text=f"{next_session} Session {session_counts[next_session] + 1}")
        clear_timer_state()
        timer_engine.start(next_session)

    timer_engine = TimerEngine(
        update_display_cb,
        session_complete_cb,
        {key: duration_vars[key].get() * 60 for key in duration_vars}
    )

    def resume_from_saved_state():
        state = load_timer_state()
        if not state:
            return False

        remaining = state["remaining_seconds"]
        mins, secs = divmod(remaining, 60)
        summary = f"{state['session_type']} – {mins}:{secs:02} remaining on '{state['task']}'"

        if messagebox.askyesno("Resume Session?", f"Resume your last session:\n{summary}?"):
            task_var.set(state["task"])
            task_session_goal.set(state["task_sessions_remaining"])
            session_type_var.set(state["session_type"])
            for k in state["session_counts"]:
                session_counts[k] = state["session_counts"][k]
            timer_engine.start_from(remaining, state["session_type"])
            return True
        return False

    def on_start():
        nonlocal session_start_time
        timer_engine.update_durations({key: duration_vars[key].get() * 60 for key in duration_vars})
        session_start_time = datetime.now()
        session_type = session_type_var.get()
        timer_engine.start(session_type)
        save_timer_state({
            "active": True,
            "session_type": session_type,
            "remaining_seconds": timer_engine.remaining,
            "session_counts": session_counts,
            "task": task_var.get().strip(),
            "task_sessions_remaining": task_session_goal.get(),
            "timestamp": datetime.now().isoformat()
        })

    def tick_loop():
        timer_engine.tick()
        root.after(100, tick_loop)

    resume_from_saved_state()
    tick_loop()

    is_paused = False

    def toggle_pause():
        nonlocal is_paused
        save_timer_state({
            "active": True,
            "session_type": timer_engine.session_type,
            "remaining_seconds": timer_engine.remaining,
            "session_counts": session_counts,
            "task": task_var.get().strip(),
            "task_sessions_remaining": task_session_goal.get(),
            "timestamp": datetime.now().isoformat()
        })

        if is_paused:
            timer_engine.resume()
            pause_btn.config(text="Pause")
        else:
            timer_engine.pause()
            pause_btn.config(text="Resume")
        is_paused = not is_paused

    def reset_session():
        nonlocal work_sessions_completed
        timer_engine.reset()
        for key in session_counts:
            session_counts[key] = 0
        work_sessions_completed = 0
        session_type_var.set("Work")
        task_var.set("")
        task_session_goal.set(1)
        session_label.config(text="Work Session 1")
        clear_timer_state()

    bottom_frame = tk.Frame(root, bg=theme["bg_color"])
    bottom_frame.grid(row=2, column=0, sticky="ew", pady=10)
    bottom_frame.columnconfigure((0, 1, 2), weight=1)

    start_btn = tk.Button(bottom_frame, text="Start", bg=theme["accent_color"], font=theme["button_font"], command=on_start)
    pause_btn = tk.Button(bottom_frame, text="Pause", bg=theme["button_color"], font=theme["button_font"], command=toggle_pause)
    reset_btn = tk.Button(bottom_frame, text="Reset", bg=theme["button_color"], font=theme["button_font"], command=reset_session)

    start_btn.grid(row=0, column=0, padx=10, sticky="ew")
    pause_btn.grid(row=0, column=1, padx=10, sticky="ew")
    reset_btn.grid(row=0, column=2, padx=10, sticky="ew")

    show_frame("home")
    root.mainloop()
