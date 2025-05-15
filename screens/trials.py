

def render_dashboard_placeholders(container, colors):
    """
    3-col × 4-row dashboard placeholders—using grid exclusively:
      Row 0: 7-Day Activity Overview (col 0–2)
      Row 1: Top Tasks by Time (col 0), Time Distribution (col 1), Task Frequency (col 2)
      Row 2: Current Streak (col 0), Longest Streak (col 1), (col 2 reserved)
      Row 3: Session History (col 0–2)
    """
    # 1) Clear existing widgets
    for w in container.winfo_children():
        w.destroy()

    # 2) Configure grid: 3 columns and 4 rows
    container.columnconfigure(0, weight=2)
    container.columnconfigure(1, weight=1)
    container.columnconfigure(2, weight=1)
    container.rowconfigure(0, weight=2)   # Overview tall
    container.rowconfigure(1, weight=1)   # KPIs row
    container.rowconfigure(2, weight=0)   # Streaks compact
    container.rowconfigure(3, weight=2)   # History tall

    frames = {}

    # Row 0: 7-Day Activity Overview
    overview = tk.Frame(container, bg=colors["overview"])
    overview.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=10, pady=10)
    overview.columnconfigure(0, weight=1)
    overview.rowconfigure(0, weight=1)
    lbl = tk.Label(overview, text="7-Day Activity Overview",
                   bg=colors["overview"], fg="white")
    lbl.grid(row=0, column=0, sticky="nsew")
    frames["overview"] = overview

    # Row 1, Col 0: Top Tasks by Time
    top_tasks = tk.Frame(container, bg=colors["top_tasks"])
    top_tasks.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
    top_tasks.columnconfigure(0, weight=1)
    top_tasks.rowconfigure(0, weight=1)
    lbl = tk.Label(top_tasks, text="Top Tasks by Time",
                   bg=colors["top_tasks"], fg="white")
    lbl.grid(row=0, column=0, sticky="nsew")
    frames["top_tasks"] = top_tasks

    # Row 1, Col 1: Time Distribution
    time_dist = tk.Frame(container, bg=colors["time_distribution"])
    time_dist.grid(row=3, column=2, sticky="nsew", padx=10, pady=10)
    time_dist.columnconfigure(0, weight=1)
    time_dist.rowconfigure(0, weight=1)
    lbl = tk.Label(time_dist, text="Time Distribution",
                   bg=colors["time_distribution"], fg="white")
    lbl.grid(row=0, column=0, sticky="nsew")
    frames["time_distribution"] = time_dist

    # Row 1, Col 2: Task Frequency
    task_freq = tk.Frame(container, bg=colors["task_freq"])
    task_freq.grid(row=1, column=2, rowspan=2, sticky="nsew", padx=10, pady=5)
    task_freq.columnconfigure(0, weight=1)
    task_freq.rowconfigure(0, weight=1)
    lbl = tk.Label(task_freq, text="Task Frequency",
                   bg=colors["task_freq"], fg="white")
    lbl.grid(row=0, column=0, rowspan=1, sticky="nsew")
    frames["task_freq"] = task_freq

    # Row 2, Col 0: Current Streak
    curr = tk.Frame(container, bg=colors["current_streak"])
    curr.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
    curr.columnconfigure(0, weight=1)
    curr.rowconfigure(0, weight=1)
    lbl = tk.Label(curr, text="Current Streak",
                   bg=colors["current_streak"], fg="white")
    lbl.grid(row=0, column=0, sticky="nsew")
    frames["current_streak"] = curr

    # Row 2, Col 1: Longest Streak
    longest = tk.Frame(container, bg=colors["longest_streak"])
    longest.grid(row=2, column=1, sticky="nsew", padx=10, pady=5)
    longest.columnconfigure(0, weight=1)
    longest.rowconfigure(0, weight=1)
    lbl = tk.Label(longest, text="Longest Streak",
                   bg=colors["longest_streak"], fg="white")
    lbl.grid(row=0, column=0, sticky="nsew")
    frames["longest_streak"] = longest

    # Row 3: Session History
    history = tk.Frame(container, bg=colors["history"])
    history.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
    history.columnconfigure(0, weight=1)
    history.rowconfigure(0, weight=1)
    lbl = tk.Label(history, text="Session History",
                   bg=colors["history"], fg="white")
    lbl.grid(row=0, column=0, sticky="nsew")
    frames["history"] = history

    return frames
def render_dashboard_layout_old(container, summaries, history_rows):
    # 1) Clear out old widgets
    for w in container.winfo_children():
        w.destroy()

    # 2) Grid config: 3 columns, 4 rows
    container.columnconfigure((0, 1, 2), weight=1)
    container.rowconfigure(0, weight=1)  # Charts row
    container.rowconfigure(1, weight=1)  # Streak cards row
    container.rowconfigure(2, weight=1)  # 7-Day overview row
    container.rowconfigure(3, weight=2)  # History row (bigger)

    # 3) Row 0, Col 0–1: Sessions per Day (Bar Chart)
    bar_frame = tk.LabelFrame(
        container,
        text="Sessions per Day",
        font=theme["label_font"],
        bg=theme["bg_color"]
    )
    bar_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=20, pady=5)
    bar_frame.columnconfigure(0, weight=1)
    bar_frame.rowconfigure(0, weight=1)
    draw_bar_chart(bar_frame, summaries["per_day"], title="Sessions per Day", use_blit=False)

    # 4) Row 0, Col 2 (rowspan=2): Time Distribution (Pie Chart)
    pie_frame = tk.LabelFrame(
        container,
        text="Time Distribution",
        font=theme["label_font"],
        bg=theme["bg_color"]
    )
    pie_frame.grid(row=0, column=2, rowspan=2, sticky="nsew", padx=20, pady=5)
    pie_frame.columnconfigure(0, weight=1)
    pie_frame.rowconfigure(0, weight=1)
    draw_pie_chart(pie_frame, summaries["per_type"], title="Time Distribution", use_blit=False)

    # 5) Row 1, Col 0–1: Streak Cards
    streaks_frame = tk.LabelFrame(
        container,
        text="Your Streaks",
        font=theme["label_font"],
        bg=theme["bg_color"]
    )
    streaks_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=20, pady=5)
    streaks_frame.columnconfigure((0, 1), weight=1)
    streaks_frame.rowconfigure(0, weight=1)
    # Current streak
    card1 = tk.Frame(streaks_frame, bg=theme["bg_color"])
    card1.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    card1.columnconfigure(0, weight=1)
    card1.rowconfigure(0, weight=1)
    draw_streak_card(card1, "Current Streak", summaries["streaks"]["current_streak"])
    # Longest streak
    card2 = tk.Frame(streaks_frame, bg=theme["bg_color"])
    card2.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    card2.columnconfigure(0, weight=1)
    card2.rowconfigure(0, weight=1)
    draw_streak_card(card2, "Longest Streak", summaries["streaks"]["longest_streak"])

    # 6) Row 2, Col 0–2: 7-Day Activity Overview (Stacked Bar)
    recent_frame = tk.LabelFrame(
        container,
        text="7-Day Activity Overview",
        font=theme["label_font"],
        bg=theme["bg_color"]
    )
    recent_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=20, pady=5)
    recent_frame.columnconfigure(0, weight=1)
    recent_frame.rowconfigure(0, weight=1)
    draw_stacked_bar_chart(recent_frame, summaries["recent"], use_blit=False)

    # 7) Row 3, Col 0–2: Session History (Table)
    history_frame = tk.LabelFrame(
        container,
        text="Session History",
        font=theme["label_font"],
        bg=theme["bg_color"]
    )
    history_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=20, pady=5)
    history_frame.columnconfigure(0, weight=1)
    history_frame.rowconfigure(0, weight=1)
    render_session_history(history_frame, history_rows, theme)
