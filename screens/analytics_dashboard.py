import tkinter as tk
from pomodoro.theme import theme
from screens.charts import (
    draw_bar_chart,
    draw_pie_chart,
    draw_stacked_bar_chart,
    draw_streak_card
)
from screens.session_viewer import render_session_history
import pandas as pd

def render_dashboard_layout(container, summaries, history_rows):
    for w in container.winfo_children():
        w.destroy()

    for col in range(3): container.columnconfigure(col, weight=1)
    for row in range(4): container.rowconfigure(row, weight=1)

    overview = tk.LabelFrame(container, text="7-Day Activity Overview", font=theme['label_font'], bg=theme["bg_color"])
    overview.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
    overview.columnconfigure(0, weight=1); overview.rowconfigure(0, weight=1)

    top_tasks = tk.LabelFrame(container, text="Top Tasks by Time", font=theme['label_font'], bg=theme["bg_color"])
    top_tasks.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
    top_tasks.columnconfigure(0, weight=1); top_tasks.rowconfigure(0, weight=1)

    task_freq = tk.LabelFrame(container, text="Task Frequency", font=theme['label_font'], bg=theme["bg_color"])
    task_freq.grid(row=1, column=2, rowspan=2, sticky="nsew", padx=10, pady=10)
    task_freq.columnconfigure(0, weight=1); task_freq.rowconfigure(0, weight=1)

    curr = tk.LabelFrame(container, text="Current Streak", font=theme['label_font'], bg=theme["bg_color"])
    curr.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
    curr.columnconfigure(0, weight=1); curr.rowconfigure(0, weight=1)

    longest = tk.LabelFrame(container, text="Longest Streak", font=theme['label_font'], bg=theme["bg_color"])
    longest.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
    longest.columnconfigure(0, weight=1); longest.rowconfigure(0, weight=1)

    history = tk.LabelFrame(container, text="Session History", font=theme["label_font"], bg=theme["bg_color"])
    history.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
    history.columnconfigure(0, weight=1); history.rowconfigure(0, weight=1)

    time_dist = tk.LabelFrame(container, text="Time Distribution", font=theme['label_font'], bg=theme["bg_color"])
    time_dist.grid(row=3, column=2, sticky="nsew", padx=10, pady=10)
    time_dist.columnconfigure(0, weight=1); time_dist.rowconfigure(0, weight=1)

    container.after(50, lambda: draw_stacked_bar_chart(overview, summaries["recent"], use_blit=True))
    container.after(100, lambda: draw_bar_chart(top_tasks, pd.DataFrame(summaries["per_task_time"]),
                                                x_key="task", y_key="total_minutes", title="", use_blit=True))
    container.after(150, lambda: draw_pie_chart(task_freq, pd.DataFrame(summaries["task_frequency"]),
                                                label_key="task", value_key="count", title="", use_blit=True))
    container.after(200, lambda: draw_streak_card(curr, "Current Streak", summaries["streaks"]["current_streak"]))
    container.after(250, lambda: draw_streak_card(longest, "Longest Streak", summaries["streaks"]["longest_streak"]))
    container.after(300, lambda: render_session_history(history, history_rows, theme))
    container.after(350, lambda: draw_pie_chart(time_dist, pd.DataFrame(summaries["per_type"]), title="", use_blit=True))
