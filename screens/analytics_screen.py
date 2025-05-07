import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pomodoro.analytics import generate_all_summaries
from pomodoro.theme import theme
import tkinter as tk

def render_analytics_screen(parent_frame):
    summaries = generate_all_summaries(use_mock=True)
    parent_frame.rowconfigure((0,1,2,3), weight=1)
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
