import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pomodoro.theme import theme

def draw_bar_chart(frame, df, title="", size=None, use_blit=False):
    if size is None:
        size = theme["chart_size_tall"]
    fig, ax = plt.subplots(figsize=size)
    ax.bar(df["date"].astype(str), df["count"], color=theme["accent_color"])
    ax.set_title(title)
    ax.set_xticks([])
    ax.set_ylabel("Count")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
    if use_blit:
        # Use blitting for faster redraws: draw static background once
        fig.canvas.draw()
        canvas.draw_idle()
    plt.close(fig)  # prevent memory bloat

def draw_pie_chart(frame, df, size=None, use_blit=False):
    if size is None:
        size = theme["chart_size_small"]
    fig, ax = plt.subplots(figsize=size)
    ax.pie(
        df["total_minutes"],
        labels=df["type"],
        autopct="%1.1f%%",
        colors=[theme["button_color"], "#aec6cf", theme["accent_color"]],
        textprops={"fontsize": 10}
    )

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
    if use_blit:
        fig.canvas.draw()
        canvas.draw_idle()
    plt.close(fig)  # prevent memory bloat

def draw_stacked_bar_chart(frame, df, size=None, use_blit=False):
    if size is None:
        size = theme["chart_size_tall"]
    pivot = df.pivot(index="date", columns="type", values="count").fillna(0)
    fig, ax = plt.subplots(figsize=size)
    pivot.plot(kind="bar", stacked=True, ax=ax, colormap=theme["default_colormap"])
    ax.set_xticks([])

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
    if use_blit:
        fig.canvas.draw()
        canvas.draw_idle()
    plt.close(fig)  # prevent memory bloat


def draw_streak_card(frame, label, value):
    import tkinter as tk
    card = tk.Label(
        frame,
        text=str(value),
        font=theme["timer_font"],
        bg=theme["button_color"],
        relief="groove",
        pady=10
    )
    card.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    return card
