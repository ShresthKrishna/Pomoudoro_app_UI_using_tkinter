import tkinter as tk
from tkinter import ttk
from pomodoro.theme import theme
from pomodoro.analytics import generate_all_summaries, get_recent_sessions, summarize_daily_for_tasks
from screens.charts import draw_bar_chart, draw_pie_chart, draw_stacked_bar_chart, draw_streak_card, draw_line_chart
from screens.session_viewer import render_session_history
import pandas as pd

def render_scrollable_layout(container, summaries, history_rows):
    # Clear existing widgets
    for w in container.winfo_children():
        w.destroy()
    # Configure columns: full width for most, two-col for streaks
    container.columnconfigure(0, weight=1)
    container.columnconfigure(0, weight=1)

    # 0: Sessions per Day (spans 2 columns)
    per_day = tk.LabelFrame(container,
                            text="Sessions per Day",
                            font=theme["label_font"],
                            bg=theme["bg_color"])
    per_day.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
    per_day.rowconfigure(0, weight=1)
    per_day.columnconfigure(0, weight=1)
    draw_bar_chart(per_day, summaries["per_day"], use_blit=True)

    # 1: Time Distribution (spans 2 columns)
    pie = tk.LabelFrame(container,
                        text="Time Distribution",
                        font=theme["label_font"],
                        bg=theme["bg_color"])
    pie.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
    pie.rowconfigure(0, weight=1)
    pie.columnconfigure(0, weight=1)
    draw_pie_chart(pie, summaries["per_type"], use_blit=True)

    # 2: Streak Cards (two columns)
    streaks = tk.LabelFrame(container,
                            text="Your Streaks",
                            font=theme["label_font"],
                            bg=theme["bg_color"])
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

    # 3: 7-Day Activity Overview (spans 2 columns)
    recent_frame = tk.LabelFrame(
        container, text="7-Day Activity Overview",
        font=theme["label_font"], bg=theme["bg_color"]
    )
    recent_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
    recent_frame.rowconfigure(1, weight=1)
    recent_frame.columnconfigure(0, weight=1)

    # 3A) Default line chart for session types
    df_type = summaries["daily_by_type"]
    draw_line_chart(
        recent_frame, df=df_type,
        x_key="date",
        y_keys=["Work", "Short Break", "Long Break"],
        labels=["Work", "Short Break", "Long Break"],
        title="Weekly Session-Type Trends",
        use_blit=True
    )

    # 3B) Task selection UI
    tasks = [d["task"] for d in summaries["task_frequency"]][:10]  # limit to top 10
    sel_frame = tk.Frame(recent_frame, bg=theme["bg_color"])
    sel_frame.grid(row=0, column=0, sticky="w", padx=10, pady=(5, 0))
    tk.Label(sel_frame, text="Show Task Trends:", font=theme["label_font"], bg=theme["bg_color"]).pack(side="left")
    task_list = ttk.Combobox(sel_frame, values=tasks, state="readonly")
    task_list.pack(side="left", padx=5)

    def on_task_select(evt):
        chosen = [task_list.get()]
        df_tasks = summarize_daily_for_tasks(pd.DataFrame(summaries["raw_sessions"]), chosen)
        # redraw
        for w in recent_frame.grid_slaves(row=1):
            w.destroy()
        draw_line_chart(
            recent_frame, df=df_tasks,
            x_key="date",
            y_keys=chosen,
            labels=chosen,
            title=f"Weekly Trends: {chosen[0]}",
            use_blit=True
        )

    task_list.bind("<<ComboboxSelected>>", on_task_select)
    # 4: Top Tasks by Time
    top_tasks_frame = tk.LabelFrame(
        container,
        text="Top Tasks by Time",
        font=theme["label_font"],
        bg=theme["bg_color"]
    )
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
    container.rowconfigure(4, weight=1)

    # 5: Task Frequency Breakdown
    freq_frame = tk.LabelFrame(
        container,
        text="Task Frequency Breakdown",
        font=theme["label_font"],
        bg=theme["bg_color"]
    )
    freq_frame.grid(row=5, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
    freq_frame.rowconfigure(0, weight=1)
    freq_frame.columnconfigure(0, weight=1)
    freq_df = pd.DataFrame(summaries["task_frequency"])
    draw_pie_chart(
        freq_frame,
        df=freq_df,
        title="Task Frequency Breakdown",
        label_key="task",
        value_key="count",
        use_blit=True
    )

    container.rowconfigure(5, weight=1)

    # 4: Session History (spans 2 columns)
    history = tk.LabelFrame(container,
                            text="Session History",
                            font=theme["label_font"],
                            bg=theme["bg_color"])
    history.grid(row=6, column=0, columnspan=2, sticky="nsew", padx=20, pady=10)
    history.rowconfigure(0, weight=1)
    history.columnconfigure(0, weight=1)
    render_session_history(history, history_rows, theme)



def render_dashboard_layout(container, summaries, history_rows):
    for w in container.winfo_children():
        w.destroy()

    # Grid setup: 3 cols, 4 rows
    container.columnconfigure(0, weight=2)
    container.columnconfigure(1, weight=1)
    container.columnconfigure(2, weight=1)
    container.rowconfigure(0, weight=2)  # Overview
    container.rowconfigure(1, weight=1)  # Top Tasks / Task Freq
    container.rowconfigure(2, weight=1)  # Streaks
    container.rowconfigure(3, weight=2)  # History / Time Dist

    # Row 0: 7 day activity overview (colspan 3)
    overview = tk.LabelFrame(container, text="7-Day Activity Overview", font=theme['label_font'], bg=theme["bg_color"])
    overview.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
    overview.columnconfigure(0, weight=1)
    overview.rowconfigure(0, weight=1)
    draw_stacked_bar_chart(overview, summaries["recent"], use_blit=True)

    # Row 1, Col 0: Top Tasks by Time
    top_tasks = tk.LabelFrame(container, text="Top Tasks by Time", font=theme['label_font'], bg=theme["bg_color"])
    top_tasks.grid(row=1, column=0,columnspan=2, sticky="nsew", padx=10, pady=10)
    top_tasks.columnconfigure(0, weight=1)
    top_tasks.rowconfigure(0, weight=1)
    draw_bar_chart(top_tasks, pd.DataFrame(summaries["per_task_time"]), x_key="task", y_key="total_minutes", title="", use_blit=True)

    # Row 1, Col 2: Task Frequency (rowspan=2)
    task_freq = tk.LabelFrame(container, text="Task Frequency", font=theme['label_font'], bg=theme["bg_color"])
    task_freq.grid(row=1, column=2, rowspan=2, sticky="nsew", padx=10, pady=10)
    task_freq.columnconfigure(0, weight=1)
    task_freq.rowconfigure(0, weight=1)
    draw_pie_chart(task_freq, pd.DataFrame(summaries["task_frequency"]), label_key="task", value_key="count", title="", use_blit=True)

    # Row 2, Col 0: Current Streak
    curr = tk.LabelFrame(container, text="Current Streak", font=theme['label_font'], bg=theme["bg_color"])
    curr.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
    curr.columnconfigure(0, weight=1)
    curr.rowconfigure(0, weight=1)
    draw_streak_card(curr, "Current Streak", summaries["streaks"]["current_streak"])

    # Row 2, Col 1: Longest Streak
    longest = tk.LabelFrame(container, text="Longest Streak", font=theme['label_font'], bg=theme["bg_color"])
    longest.grid(row=2, column=1, sticky="nsew", padx=10, pady=10)
    longest.columnconfigure(0, weight=1)
    longest.rowconfigure(0, weight=1)
    draw_streak_card(longest, "Longest Streak", summaries["streaks"]["longest_streak"])

    # Row 3, Col 0–1: Session History
    history = tk.LabelFrame(container, text="Session History", font=theme["label_font"], bg=theme["bg_color"])
    history.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
    history.columnconfigure(0, weight=1)
    history.rowconfigure(0, weight=1)
    render_session_history(history, history_rows, theme)

    # Row 3, Col 2: Time Distribution
    time_dist = tk.LabelFrame(container, text="Time Distribution", font=theme["label_font"], bg=theme["bg_color"])
    time_dist.grid(row=3, column=2, sticky="nsew", padx=10, pady=10)
    time_dist.columnconfigure(0, weight=1)
    time_dist.rowconfigure(0, weight=1)
    draw_pie_chart(time_dist, pd.DataFrame(summaries["per_type"]), title="", use_blit=True)

def render_analytics_screen(parent_frame, use_mock=False):
    # clear container
    # colors = {
    #     "sessions": "#4CAF50",
    #     "time": "#2196F3",
    #     "top_tasks": "#FFC107",
    #     "time_distribution": "#2196F3",
    #     "task_freq": "#9C27B0",
    #     "overview": "#8BC34A",
    #     "current_streak": "#FF5722",
    #     "longest_streak": "#03A9F4",
    #     "history": "#607D8B"
    #  }
    # frames = render_dashboard_placeholders(parent_frame, colors)

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