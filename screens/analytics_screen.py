import tkinter as tk
from tkinter import ttk
from pomodoro.theme import theme
from pomodoro.analytics import (
    generate_all_summaries,
    get_recent_sessions,
    summarize_daily_for_tasks
)
from screens.charts import (
    draw_bar_chart,
    draw_pie_chart,
    draw_stacked_bar_chart,
    draw_streak_card,
    draw_line_chart
)
from screens.session_viewer import render_session_history
import pandas as pd


def render_dashboard_layout(container, summaries, history_rows):
    # Clear existing widgets
    for w in container.winfo_children():
        w.destroy()

    # Grid setup: 3 columns × 4 rows
    for col in range(3):
        container.columnconfigure(col, weight=1)
    for row in range(4):
        container.rowconfigure(row, weight=1)

    # === Prepare Layout First ===

    # Row 0: 7-Day Activity Overview (colspan 3)
    overview = tk.LabelFrame(container, text="7-Day Activity Overview",
                             font=theme['label_font'], bg=theme["bg_color"])
    overview.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
    overview.columnconfigure(0, weight=1)
    overview.rowconfigure(0, weight=1)

    # Row 1: Top Tasks by Time (col 0–1)
    top_tasks = tk.LabelFrame(container, text="Top Tasks by Time",
                              font=theme['label_font'], bg=theme["bg_color"])
    top_tasks.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
    top_tasks.columnconfigure(0, weight=1)
    top_tasks.rowconfigure(0, weight=1)

    # Row 1: Task Frequency (col 2, rowspan 2)
    task_freq = tk.LabelFrame(container, text="Task Frequency",
                              font=theme['label_font'], bg=theme["bg_color"])
    task_freq.grid(row=1, column=2, rowspan=2, sticky="nsew", padx=10, pady=10)
    task_freq.columnconfigure(0, weight=1)
    task_freq.rowconfigure(0, weight=1)

    # Row 2: Current Streak (col 0)
    curr = tk.LabelFrame(container, text="Current Streak",
                         font=theme['label_font'], bg=theme["bg_color"])
    curr.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
    curr.columnconfigure(0, weight=1)
    curr.rowconfigure(0, weight=1)

    # Row 2: Longest Streak (col 1)
    longest = tk.LabelFrame(container, text="Longest Streak",
                            font=theme['label_font'], bg=theme["bg_color"])
    longest.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
    longest.columnconfigure(0, weight=1)
    longest.rowconfigure(0, weight=1)

    # Row 3: Session History (col 0–1)
    history = tk.LabelFrame(container, text="Session History",
                            font=theme["label_font"], bg=theme["bg_color"])
    history.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
    history.columnconfigure(0, weight=1)
    history.rowconfigure(0, weight=1)

    # Row 3: Time Distribution (col 2)
    time_dist = tk.LabelFrame(container, text="Time Distribution",
                              font=theme['label_font'], bg=theme["bg_color"])
    time_dist.grid(row=3, column=2, sticky="nsew", padx=10, pady=10)
    time_dist.columnconfigure(0, weight=1)
    time_dist.rowconfigure(0, weight=1)

    # === Deferred Chart Rendering ===

    container.after(50, lambda: draw_stacked_bar_chart(overview, summaries["recent"], use_blit=True))
    container.after(100, lambda: draw_bar_chart(
        top_tasks,
        df=pd.DataFrame(summaries["per_task_time"]),
        x_key="task", y_key="total_minutes",
        title="", use_blit=True
    ))
    container.after(150, lambda: draw_pie_chart(
        task_freq,
        df=pd.DataFrame(summaries["task_frequency"]),
        label_key="task", value_key="count",
        title="", use_blit=True
    ))
    container.after(200, lambda: draw_streak_card(curr, "Current Streak", summaries["streaks"]["current_streak"]))
    container.after(250, lambda: draw_streak_card(longest, "Longest Streak", summaries["streaks"]["longest_streak"]))
    container.after(300, lambda: render_session_history(history, history_rows, theme))
    container.after(350, lambda: draw_pie_chart(
        time_dist, pd.DataFrame(summaries["per_type"]), title="", use_blit=True
    ))

def render_scrollable_layout(container, summaries, history_rows,full_history=None):
    # Clear existing widgets
    for w in container.winfo_children():
        w.destroy()

    # Make two equal columns
    container.columnconfigure(0, weight=1)
    container.columnconfigure(1, weight=1)

    # 0: Sessions per Day
    per_day = tk.LabelFrame(container, text="Sessions per Day",
                            font=theme["label_font"], bg=theme["bg_color"])
    per_day.grid(row=0, column=0, columnspan=2,
                 sticky="nsew", padx=20, pady=10)
    per_day.rowconfigure(0, weight=1)
    per_day.columnconfigure(0, weight=1)
    draw_bar_chart(per_day, summaries["per_day"], use_blit=True)

    # 1: Time Distribution
    pie = tk.LabelFrame(container, text="Time Distribution",
                        font=theme["label_font"], bg=theme["bg_color"])
    pie.grid(row=1, column=0, columnspan=2,
             sticky="nsew", padx=20, pady=10)
    pie.rowconfigure(0, weight=1)
    pie.columnconfigure(0, weight=1)
    draw_pie_chart(pie, summaries["per_type"], use_blit=True)

    # 2: Streak Cards
    streaks = tk.LabelFrame(container, text="Your Streaks",
                            font=theme["label_font"], bg=theme["bg_color"])
    streaks.grid(row=2, column=0, columnspan=2,
                 sticky="nsew", padx=20, pady=10)
    streaks.rowconfigure(0, weight=1)
    streaks.columnconfigure(0, weight=1)
    streaks.columnconfigure(1, weight=1)
    for i, (k, v) in enumerate(summaries["streaks"].items()):
        card = tk.Frame(streaks, bg=theme["bg_color"])
        card.grid(row=0, column=i, sticky="nsew", padx=5, pady=5)
        card.rowconfigure(0, weight=1)
        card.columnconfigure(0, weight=1)
        draw_streak_card(card, k.replace("_", " ").title(), v)

    # 3: 7-Day Activity Overview
    recent_frame = tk.LabelFrame(
        container, text="7-Day Activity Overview",
        font=theme["label_font"], bg=theme["bg_color"]
    )
    recent_frame.grid(row=3, column=0, columnspan=2,
                      sticky="nsew", padx=20, pady=10)
    recent_frame.rowconfigure(1, weight=1)
    recent_frame.columnconfigure(0, weight=1)

    # 3A) Default 3-line chart
    df_type = summaries["daily_by_type"]
    # ensure all three types exist
    for col in ("Work", "Short Break", "Long Break"):
        if col not in df_type.columns:
            df_type[col] = 0

    draw_line_chart(
        recent_frame, df=df_type,
        x_key="date",
        y_keys=["Work", "Short Break", "Long Break"],
        labels=["Work", "Short Break", "Long Break"],
        title="Weekly Session-Type Trends",
        use_blit=True
    )

    # 3B) Combined dropdown
    options = ["Work", "Short Break", "Long Break"] + \
              [d["task"] for d in summaries["task_frequency"]]
    sel_frame = tk.Frame(recent_frame, bg=theme["bg_color"])
    sel_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(5, 0))
    tk.Label(sel_frame, text="Show Trends:",
             font=theme["label_font"], bg=theme["bg_color"]
    ).pack(side="left")
    combo = ttk.Combobox(sel_frame, values=options, state="readonly")
    combo.pack(side="left", padx=5)
    combo.set("Work")

    def on_select(evt):
        choice = combo.get()
        # clear old chart
        for w in recent_frame.grid_slaves(row=1):
            w.destroy()

        if choice in ("Work", "Short Break", "Long Break"):
            # single-line for that type
            draw_line_chart(
                recent_frame, df=df_type,
                x_key="date",
                y_keys=[choice],
                labels=[choice],
                title=f"Weekly {choice} Trend",
                use_blit=True
            )
        else:
            # task-specific (Work sessions only)
            df_tasks = summarize_daily_for_tasks(
                pd.DataFrame(summaries["raw_sessions"]), [choice]
            )
            draw_line_chart(
                recent_frame, df=df_tasks,
                x_key="date",
                y_keys=[choice],
                labels=[choice],
                title=f"Weekly Task Trend: {choice}",
                use_blit=True
            )

    combo.bind("<<ComboboxSelected>>", on_select)

    # 4: Top Tasks by Time
    top_tasks_frame = tk.LabelFrame(
        container, text="Top Tasks by Time",
        font=theme["label_font"], bg=theme["bg_color"]
    )
    top_tasks_frame.grid(row=4, column=0, columnspan=2,
                         sticky="nsew", padx=20, pady=10)
    top_tasks_frame.rowconfigure(0, weight=1)
    top_tasks_frame.columnconfigure(0, weight=1)
    draw_bar_chart(
        top_tasks_frame,
        df=pd.DataFrame(summaries["per_task_time"]),
        title="Top Tasks by Time",
        x_key="task",
        y_key="total_minutes",
        use_blit=True
    )

    # 5: Task Frequency Breakdown
    freq_frame = tk.LabelFrame(
        container, text="Task Frequency Breakdown",
        font=theme["label_font"], bg=theme["bg_color"]
    )
    freq_frame.grid(row=5, column=0, columnspan=2,
                    sticky="nsew", padx=20, pady=10)
    freq_frame.rowconfigure(0, weight=1)
    freq_frame.columnconfigure(0, weight=1)
    draw_pie_chart(
        freq_frame,
        df=pd.DataFrame(summaries["task_frequency"]),
        title="Task Frequency Breakdown",
        label_key="task",
        value_key="count",
        use_blit=True
    )

    # 6: Session History
    history = tk.LabelFrame(
        container, text="Session History",
        font=theme["label_font"], bg=theme["bg_color"]
    )
    history.grid(row=6, column=0, columnspan=2,
                 sticky="nsew", padx=20, pady=10)
    history.rowconfigure(0, weight=1)
    history.columnconfigure(0, weight=1)
    render_session_history(history, history_rows, theme)

    def expand():
        # Clear old history frame content
        for w in history.winfo_children():
            w.destroy()
        render_session_history(history, full_history, theme)

    tk.Button(history, text="Show All", command=expand, bg=theme["button_color"]).grid(
        row=1, column=0, pady=5
    )


def render_analytics_screen(parent_frame, use_mock=False):
    for w in parent_frame.winfo_children():
        w.destroy()

    summaries = generate_all_summaries(use_mock=use_mock)
    history_rows = get_recent_sessions(20, use_mock)

    parent_frame.rowconfigure(0, weight=1)
    parent_frame.columnconfigure(0, weight=1)

    canvas = tk.Canvas(parent_frame, bg=theme["bg_color"], highlightthickness=0)
    canvas.grid(row=0, column=0, columnspan=2, sticky="nsew")
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

    container.columnconfigure(0, weight=1)
    container.columnconfigure(1, weight=1)
    container.columnconfigure(2, weight=1)

    resize_job = [None]

    def on_resize(event=None):
        if resize_job[0]:
            parent_frame.after_cancel(resize_job[0])
        def decide():
            w = parent_frame.winfo_width()
            container.update_idletasks()
            if w >= 900:
                render_dashboard_layout(container, summaries, history_rows)
            else:
                render_scrollable_layout(container, summaries, history_rows)
        resize_job[0] = parent_frame.after(200, decide)

    parent_frame.bind("<Configure>", on_resize)

    # Trigger initial render based on actual window size
    parent_frame.after(10, on_resize)

