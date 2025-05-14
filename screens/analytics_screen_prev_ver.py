import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pomodoro.analytics import generate_all_summaries, get_recent_sessions
from pomodoro.theme import theme
import tkinter as tk
from tkinter import ttk

def render_analytics_screen(parent_frame, use_mock=False):
    summaries = generate_all_summaries(use_mock=use_mock)
    parent_frame.rowconfigure((0,1,2,3,4), weight=1)
    parent_frame.columnconfigure(0, weight=1)

    # 1. Session Per day Frame

    per_day_frame = tk.LabelFrame(parent_frame,
                                  text="Sessions per Day (Last 30 Days)",
                                  font= theme["label_font"],
                                  bg=theme["bg_color"])
    per_day_frame.rowconfigure(0, weight=1)
    per_day_frame.columnconfigure(0, weight=1)
    per_day_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=10)

    if not summaries["per_day"].empty:
        fig1, ax1 = plt.subplots(figsize=theme["chart_size_small"])
        ax1.bar(x= summaries["per_day"]["date"].astype(str),
                height=summaries["per_day"]["count"],
                color=theme["accent_color"])
        ax1.set_xticks([])

        canvas1 = FigureCanvasTkAgg(fig1, master=per_day_frame)
        canvas1.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    # 2. Time Distribution Chart
    per_type_frame = tk.LabelFrame(parent_frame,
                                   text="Time Distribution",
                                   font=theme["label_font"],
                                   bg=theme["bg_color"])
    per_type_frame.rowconfigure(0, weight=1)
    per_type_frame.columnconfigure(0, weight=1)
    per_type_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)

    if not summaries["per_type"].empty:
        fig2, ax2 = plt.subplots(figsize=(3.5, 2.5))
        ax2.pie(
            summaries["per_type"]["total_minutes"],
            labels=summaries["per_type"]["type"],
            autopct="%1.1f%%",
            colors=[theme["button_color"], "#aec6cf", theme["accent_color"]],
            textprops = {"fontsize": 10}
        )
        canvas2 = FigureCanvasTkAgg(fig2, master=per_type_frame)
        canvas2.get_tk_widget().grid(row=0, column=0, sticky="nsew")
    # 3. Streaks display
    streak_frame = tk.LabelFrame(parent_frame,
                                 text="Your Streaks",
                                 font= theme["label_font"],
                                 bg= theme["bg_color"])
    streak_frame.rowconfigure(0, weight=1)
    streak_frame.columnconfigure(0, weight= 1)
    streak_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
    for i,(label, value) in enumerate(summaries["streaks"].items()):
        tk.Label(streak_frame,
                 text=f"{label.replace('_', ' ').title()}: {value}",
                 font=theme["button_font"],
                 bg=theme["button_color"],
                 relief="groove",
                 padx=10,
                 pady=5
                 ).grid(row=i,
                        column=0,
                        sticky="ew",
                        padx=10,
                        pady=5)
 # Last 7 days bar chart data
    recent_frame = tk.LabelFrame(parent_frame,
                                 text="7-Day Activity Overview",
                                 font=theme["label_font"],
                                 bg=theme["bg_color"])
    recent_frame.rowconfigure(0, weight=1)
    recent_frame.columnconfigure(0, weight=1)
    recent_frame.grid(row=3, column=0, sticky="nsew", padx=20, pady=10)
    if not summaries["recent"].empty:
        pivot = summaries["recent"].pivot(index="date", columns="type", values="count").fillna(0)
        fig3, ax3 = plt.subplots(figsize=theme["chart_size_small"])
        pivot.plot(kind="bar", stacked=True, ax=ax3, colormap=theme["default_colormap"])
        ax3.set_xticks([])
        canvas3 = FigureCanvasTkAgg(fig3, master=recent_frame)
        canvas3.get_tk_widget().grid(row=0, column=0, sticky="nsew")

    # 5. Session History Table
    history_frame = tk.LabelFrame(parent_frame,
                                  text="Session History",
                                  font=theme["label_font"],
                                  bg=theme["bg_color"],
                                  relief="groove")
    history_frame.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")
    history_frame.rowconfigure(0, weight=1)
    history_frame.columnconfigure(0, weight=1)

    columns = ("#1", "#2", "#3", "#4", "#5")
    tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=8)
    tree.grid(row=0, column=0, sticky="nsew")

    # Set column headers
    tree.heading("#1", text="Session #")
    tree.heading("#2", text="Type")
    tree.heading("#3", text="Completed At")
    tree.heading("#4", text="Duration")
    tree.heading("#5", text="Task")

    tree.column("#1", width=80, anchor="center")
    tree.column("#2", width=100, anchor="w")
    tree.column("#3", width=160)
    tree.column("#4", width=80)
    tree.column("#5", width=120)

    # Scrollbar
    scrollbar = ttk.Scrollbar(history_frame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    rows = get_recent_sessions(n=20, use_mock=use_mock)
    if not rows:
        tk.Label(history_frame,
                 text="No sessions yet — your session history will appear here.",
                 font=theme["label_font"],
                 bg=theme["bg_color"]
                 ).grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    for row in rows:
        tree.insert("", "end", values=[
            row["session_number"],
            row["type"],
            row["completed_at"],
            f"{row['duration_minutes']} min",
            row.get("task", "")
        ])