import tkinter as tk
from tkinter import ttk
from pomodoro.theme import theme
from pomodoro.analytics import generate_all_summaries, get_recent_sessions
from screens.charts import draw_bar_chart, draw_pie_chart, draw_stacked_bar_chart, draw_streak_card
from screens.session_viewer import render_session_history

def render_analytics_screen(parent_frame, use_mock=False):
    # Configure parent frame to expand fully
    parent_frame.rowconfigure(0, weight=1)
    parent_frame.columnconfigure(0, weight=1)

    canvas = tk.Canvas(parent_frame, bg=theme["bg_color"], highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    scrollbar = tk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)

    scrollable_frame = tk.Frame(canvas, bg=theme["bg_color"])
    scroll_window = canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    def on_canvas_configure(event):
        canvas.itemconfig(scroll_window, width=event.width)
    canvas.bind("<Configure>", on_canvas_configure)
    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    scrollable_frame.columnconfigure(0, weight=1)

    summaries = generate_all_summaries(use_mock=use_mock)

    # Sessions per Day
    per_day_frame = tk.LabelFrame(scrollable_frame, text="Sessions per Day (Last 30 Days)",
                                  font=theme["label_font"], bg=theme["bg_color"])
    per_day_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
    per_day_frame.columnconfigure(0, weight=1)
    if not summaries["per_day"].empty:
        draw_bar_chart(per_day_frame, summaries["per_day"], "Sessions per Day")

    # Time Distribution
    per_type_frame = tk.LabelFrame(scrollable_frame, text="Time Distribution",
                                   font=theme["label_font"], bg=theme["bg_color"])
    per_type_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
    per_type_frame.columnconfigure(0, weight=1)
    if not summaries["per_type"].empty:
        draw_pie_chart(per_type_frame, summaries["per_type"])

    # Streaks
    streak_frame = tk.LabelFrame(scrollable_frame, text="Your Streaks",
                                 font=theme["label_font"], bg=theme["bg_color"])
    streak_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")
    streak_frame.columnconfigure((0, 1), weight=1)
    streak_frame.rowconfigure(0, weight=1)

    streaks = summaries["streaks"]

    for i, (key, value) in enumerate(streaks.items()):
        label_text = key.replace("_", " ").title()

        card_frame = tk.LabelFrame(
            streak_frame,
            text=label_text,
            font=theme["label_font"],
            bg=theme["bg_color"]
        )
        card_frame.grid(row=0, column=i, padx=10, pady=10, sticky="nsew")
        card_frame.rowconfigure(0, weight=1)
        card_frame.columnconfigure(0, weight=1)

        draw_streak_card(card_frame, label=label_text, value=value)
    # 7-Day Activity
    recent_frame = tk.LabelFrame(scrollable_frame, text="7-Day Activity Overview",
                                 font=theme["label_font"], bg=theme["bg_color"])
    recent_frame.grid(row=3, column=0, padx=20, pady=10, sticky="nsew")
    recent_frame.columnconfigure(0, weight=1)
    if not summaries["recent"].empty:
        draw_stacked_bar_chart(recent_frame, summaries["recent"])

    # Session History
    history_frame = tk.LabelFrame(scrollable_frame, text="Session History",
                                  font=theme["label_font"], bg=theme["bg_color"], relief="groove")
    history_frame.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
    history_frame.rowconfigure(0, weight=1)
    history_frame.columnconfigure(0, weight=1)

    rows = get_recent_sessions(n=20, use_mock=use_mock)
    render_session_history(history_frame, rows, theme)
    def force_scroll_update():
        scrollable_frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    tk.Button(parent_frame, text="Fix Height", command=force_scroll_update).grid(row=1, column=0, pady=5)
    parent_frame.rowconfigure(1, weight=0)
