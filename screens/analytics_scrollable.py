import tkinter as tk
from tkinter import ttk
from pomodoro.theme import theme
from screens.charts import (
    draw_bar_chart,
    draw_pie_chart,
    draw_line_chart,
    draw_streak_card
)
from screens.session_viewer import render_session_history
from pomodoro.analytics import summarize_daily_for_tasks
import pandas as pd

def render_scrollable_layout(container, summaries, history_rows, full_history=None):
    for w in container.winfo_children():
        w.destroy()

    container.columnconfigure(0, weight=1)
    container.columnconfigure(1, weight=1)

    # 0: Sessions per Day
    per_day = tk.LabelFrame(container, text="Sessions per Day",
                            font=theme["label_font"], bg=theme["bg_color"])
    per_day.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
    per_day.rowconfigure(0, weight=1)
    per_day.columnconfigure(0, weight=1)
    draw_bar_chart(per_day, summaries["per_day"], use_blit=True)

    # 1: Time Distribution
    pie = tk.LabelFrame(container, text="Time Distribution",
                        font=theme["label_font"], bg=theme["bg_color"])
    pie.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
    pie.rowconfigure(0, weight=1)
    pie.columnconfigure(0, weight=1)
    draw_pie_chart(pie, summaries["per_type"], use_blit=True)

    # 2: Streak Cards
    streaks = tk.LabelFrame(container, text="Your Streaks",
                            font=theme["label_font"], bg=theme["bg_color"])
    streaks.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
    streaks.rowconfigure(0, weight=1)
    streaks.columnconfigure(0, weight=1)
    streaks.columnconfigure(1, weight=1)

    for i, (k, v) in enumerate(summaries["streaks"].items()):
        card = tk.Frame(streaks, bg=theme["bg_color"])
        card.grid(row=0, column=i, sticky="nsew", padx=5, pady=5)
        card.rowconfigure(0, weight=1)
        card.columnconfigure(0, weight=1)
        draw_streak_card(card, k.replace("_", " ").title(), v)

    # 3: 7-Day Activity Line Chart with Dropdown
    recent_frame = tk.LabelFrame(container, text="7-Day Activity Overview",
                                 font=theme["label_font"], bg=theme["bg_color"])
    recent_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
    recent_frame.rowconfigure(1, weight=1)
    recent_frame.columnconfigure(0, weight=1)

    df_type = summaries["daily_by_type"]
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

    options = ["Work", "Short Break", "Long Break"] + \
              [d["task"] for d in summaries["task_frequency"]]

    sel_frame = tk.Frame(recent_frame, bg=theme["bg_color"])
    sel_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(5, 0))
    tk.Label(sel_frame, text="Show Trends:", font=theme["label_font"], bg=theme["bg_color"]).pack(side="left")

    combo = ttk.Combobox(sel_frame, values=options, state="readonly")
    combo.pack(side="left", padx=5)
    combo.set("Work")

    def on_select(evt):
        choice = combo.get()
        for w in recent_frame.grid_slaves(row=1):
            w.destroy()

        if choice in ("Work", "Short Break", "Long Break"):
            draw_line_chart(
                recent_frame, df=df_type,
                x_key="date",
                y_keys=[choice],
                labels=[choice],
                title=f"Weekly {choice} Trend",
                use_blit=True
            )
        else:
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
    top_tasks_frame = tk.LabelFrame(container, text="Top Tasks by Time",
                                    font=theme["label_font"], bg=theme["bg_color"])
    top_tasks_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
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
    freq_frame = tk.LabelFrame(container, text="Task Frequency Breakdown",
                               font=theme["label_font"], bg=theme["bg_color"])
    freq_frame.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
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

    # 6: Session History + Expand Button
    history = tk.LabelFrame(container, text="Session History",
                            font=theme["label_font"], bg=theme["bg_color"])
    history.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
    history.rowconfigure(0, weight=1)
    history.columnconfigure(0, weight=1)
    render_session_history(history, history_rows, theme)

    if full_history:
        def expand():
            for w in history.winfo_children():
                w.destroy()
            render_session_history(history, full_history, theme)

        tk.Button(history, text="Show All", command=expand, bg=theme["button_color"]).grid(
            row=1, column=0, pady=5
        )
