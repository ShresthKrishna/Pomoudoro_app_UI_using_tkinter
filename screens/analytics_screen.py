import tkinter as tk
from tkinter import ttk
from pomodoro.theme import theme
from pomodoro.analytics import generate_all_summaries, get_recent_sessions
from screens.charts import draw_bar_chart, draw_pie_chart, draw_stacked_bar_chart, draw_streak_card
from screens.session_viewer import render_session_history


def render_scrollable_layout(container, summaries, history_rows):
    # Clear existing widgets
    for w in container.winfo_children():
        w.destroy()
    # Configure columns: full width for most, two-col for streaks
    container.columnconfigure(0, weight=1)
    container.columnconfigure(1, weight=1)

    # 0: Sessions per Day (spans 2 columns)
    per_day = tk.LabelFrame(container,
                             text="Sessions per Day",
                             font=theme["label_font"],
                             bg=theme["bg_color"])
    per_day.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
    per_day.rowconfigure(0, weight=1); per_day.columnconfigure(0, weight=1)
    draw_bar_chart(per_day, summaries["per_day"], use_blit=True)

    # 1: Time Distribution (spans 2 columns)
    pie = tk.LabelFrame(container,
                        text="Time Distribution",
                        font=theme["label_font"],
                        bg=theme["bg_color"])
    pie.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
    pie.rowconfigure(0, weight=1); pie.columnconfigure(0, weight=1)
    draw_pie_chart(pie, summaries["per_type"], use_blit=True)

    # 2: Streak Cards (two columns)
    streaks = tk.LabelFrame(container,
                             text="Your Streaks",
                             font=theme["label_font"],
                             bg=theme["bg_color"])
    streaks.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
    streaks.rowconfigure(0, weight=1); streaks.columnconfigure(0, weight=1); streaks.columnconfigure(1, weight=1)
    for i, (k, v) in enumerate(summaries["streaks"].items()):
        card = tk.Frame(streaks, bg=theme["bg_color"])
        card.grid(row=0, column=i, sticky="nsew", padx=5, pady=5)
        card.rowconfigure(0, weight=1); card.columnconfigure(0, weight=1)
        draw_streak_card(card, k.replace("_", " ").title(), v)

    # 3: 7-Day Activity Overview (spans 2 columns)
    recent = tk.LabelFrame(container,
                           text="7-Day Activity Overview",
                           font=theme["label_font"],
                           bg=theme["bg_color"])
    recent.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
    recent.rowconfigure(0, weight=1); recent.columnconfigure(0, weight=1)
    draw_stacked_bar_chart(recent, summaries["recent"], use_blit=True)

    # 4: Session History (spans 2 columns)
    history = tk.LabelFrame(container,
                             text="Session History",
                             font=theme["label_font"],
                             bg=theme["bg_color"])
    history.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
    history.rowconfigure(0, weight=1); history.columnconfigure(0, weight=1)
    render_session_history(history, history_rows, theme)


def render_dashboard_layout(container, summaries, history_rows):
    # Clear any existing widgets
    for w in container.winfo_children():
        w.destroy()

    # Configure a 3x4 grid with streaks row non-expanding
    container.columnconfigure((0, 1, 2), weight=1)
    container.rowconfigure(0, weight=1)
    container.rowconfigure(1, weight=0)  # streaks minimal height
    container.rowconfigure(2, weight=1)
    container.rowconfigure(3, weight=1)

    # Row 0: Sessions per Day (col 0-1)
    bar_frame = tk.LabelFrame(container,
                               text="Sessions per Day",
                               font=theme["label_font"],
                               bg=theme["bg_color"])
    bar_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
    bar_frame.rowconfigure(0, weight=1); bar_frame.columnconfigure(0, weight=1)
    draw_bar_chart(bar_frame, summaries["per_day"], use_blit=False)

    # Row 0: Time Distribution extends into streaks row (col 2, rowspan=2)
    pie_frame = tk.LabelFrame(container,
                               text="Time Distribution",
                               font=theme["label_font"],
                               bg=theme["bg_color"])
    pie_frame.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=20, pady=10)
    pie_frame.rowconfigure(0, weight=1); pie_frame.columnconfigure(0, weight=1)
    draw_pie_chart(pie_frame, summaries["per_type"], use_blit=False)

    # Row 1: Streak Cards side-by-side (col 0-1)
    streaks = tk.LabelFrame(container,
                             text="Your Streaks",
                             font=theme["label_font"],
                             bg=theme["bg_color"])
    streaks.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
    streaks.rowconfigure(0, weight=1); streaks.columnconfigure((0, 1), weight=1)
    for i, (k, v) in enumerate(summaries["streaks"].items()):
        card = tk.Frame(streaks, bg=theme["bg_color"])
        card.grid(row=0, column=i, sticky="nsew", padx=10, pady=10)
        card.rowconfigure(0, weight=1); card.columnconfigure(0, weight=1)
        draw_streak_card(card, k.replace("_", " ").title(), v)

    # Row 2: 7-Day Activity Overview (col 0-2)
    recent = tk.LabelFrame(container,
                           text="7-Day Activity Overview",
                           font=theme["label_font"],
                           bg=theme["bg_color"])
    recent.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=20, pady=10)
    recent.rowconfigure(0, weight=1); recent.columnconfigure(0, weight=1)
    draw_stacked_bar_chart(recent, summaries["recent"], use_blit=False)

    # Row 3: Session History (col 0-2)
    history = tk.LabelFrame(container,
                             text="Session History",
                             font=theme["label_font"],
                             bg=theme["bg_color"])
    history.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=20, pady=10)
    history.rowconfigure(0, weight=1); history.columnconfigure(0, weight=1)
    render_session_history(history, history_rows, theme)
def render_analytics_screen(parent_frame, use_mock=False):
    # clear container
    for w in parent_frame.winfo_children():
        w.destroy()

    # cache data
    summaries = generate_all_summaries(use_mock=use_mock)
    history_rows = get_recent_sessions(20, use_mock)

    parent_frame.rowconfigure(0, weight=1)
    parent_frame.columnconfigure(0, weight=1)

    # scrollable canvas setup
    canvas = tk.Canvas(parent_frame, bg=theme["bg_color"], highlightthickness=0)
    canvas.grid(row=0, column=0, sticky="nsew")
    v_scroll = tk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
    v_scroll.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=v_scroll.set)

    container = tk.Frame(canvas, bg=theme["bg_color"])
    window_id = canvas.create_window((0, 0), window=container, anchor="nw")

    def on_canvas_configure(e):
        canvas.itemconfig(window_id, width=e.width)
        container.config(width=e.width)
    def on_container_configure(e):
        canvas.configure(scrollregion=canvas.bbox("all"))

    canvas.bind("<Configure>", on_canvas_configure)
    container.bind("<Configure>", on_container_configure)
    canvas.bind("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))
    canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    resize_job = [None]

    def on_resize(event=None):
        if resize_job[0]:
            parent_frame.after_cancel(resize_job[0])
        def decide():
            w = parent_frame.winfo_width()
            if w >= 900:
                render_dashboard_layout(container, summaries, history_rows)
            else:
                render_scrollable_layout(container, summaries, history_rows)
        resize_job[0] = parent_frame.after(200, decide)

    parent_frame.bind("<Configure>", on_resize)
    # initial render
    container.after(50, lambda: render_scrollable_layout(container, summaries, history_rows))
