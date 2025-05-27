import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pomodoro.theme import theme
import matplotlib as mpl


def draw_bar_chart(frame, df, title="", x_key="date", y_key="count", size=None, use_blit=False):
    if size is None:
        size = theme["chart_size_tall"]
    mpl.rcParams['figure.dpi'] = 120  # or 150
    mpl.rcParams['savefig.dpi'] = 120
    fig, ax = plt.subplots(figsize=size)

    # Plot the data using provided keys
    ax.bar(df[x_key].astype(str), df[y_key], color=theme["accent_color"])
    ax.set_title(title)
    ax.set_xticks(range(len(df)))
    ax.set_xticklabels(df[x_key].astype(str), rotation=30, ha="right", fontsize=8)
    ax.set_ylabel(y_key.replace("_", " ").title())

    fig.tight_layout()
    fig.subplots_adjust(bottom=0.2)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
    if use_blit:
        fig.canvas.draw()
        canvas.draw_idle()
    plt.close(fig)

def draw_pie_chart(frame, df, title="", label_key="type", value_key="total_minutes", size=None, use_blit=False):
    if size is None:
        size = theme["chart_size_tall"]
    mpl.rcParams['figure.dpi'] = 120  # or 150
    mpl.rcParams['savefig.dpi'] = 120
    fig, ax = plt.subplots(figsize=size)

    ax.pie(
        df[value_key],
        labels=df[label_key],
        autopct="%1.1f%%",
        colors=[theme["button_color"], "#aec6cf", theme["accent_color"],"yellow"],
        textprops={"fontsize": 10}
    )
    ax.set_title(title)

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
    if use_blit:
        fig.canvas.draw()
        canvas.draw_idle()
    plt.close(fig)


def draw_stacked_bar_chart(frame, df, size=None, use_blit=False):
    if size is None:
        size = theme["chart_size_tall"]
    if df.empty or "count" not in df.columns:
        print("[DEBUG] Skipping stacked bar chart — no count data.")
        return

    pivot = df.pivot(index="date", columns="type", values="count").fillna(0)
    mpl.rcParams['figure.dpi'] = 120  # or 150
    mpl.rcParams['savefig.dpi'] = 120
    fig, ax = plt.subplots(figsize=size)

    pivot.plot(kind="bar", stacked=True, ax=ax, colormap=theme["default_colormap"])
    ax.set_xticks(range(len(pivot.index)))
    ax.set_xticklabels(pivot.index.astype(str), rotation=45, ha="right", fontsize=8)
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().grid(row=0, column=0, sticky="nsew")
    if use_blit:
        fig.canvas.draw()
        canvas.draw_idle()
    plt.close(fig)  # prevent memory bloat


def draw_streak_card(frame, label, value):
    import tkinter as tk

    # Label text at the top
    title = tk.Label(
        frame,
        text=label,
        font=theme["label_font"],
        bg=theme["bg_color"]
    )
    title.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nsew")

    # Value displayed below
    value_label = tk.Label(
        frame,
        text=str(value),
        font=theme["timer_font"],
        bg=theme["button_color"],
        relief="groove",
        pady=10
    )
    value_label.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="nsew")

    return value_label

def draw_line_chart(frame, df, x_key="date", y_keys=None, labels=None,
                    title="", size=None, use_blit=False):
    """
    Plots one or more lines.
    - df: DataFrame with an x_key column plus one column per y_key.
    - y_keys: list of column names to plot.
    - labels: optional list of labels for each line.
    """
    if size is None:
        size = theme["chart_size_tall"]
    if not y_keys:
        return

    mpl.rcParams['figure.dpi'] = 120  # or 150
    mpl.rcParams['savefig.dpi'] = 120
    fig, ax = plt.subplots(figsize=size)
    x = df[x_key].astype(str)
    for i, yk in enumerate(y_keys):
        ax.plot(x, df[yk], marker="o", label=(labels[i] if labels else yk))

    ax.set_title(title)
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x, rotation=45, ha="right", fontsize=8)
    ax.legend(fontsize=8)
    ax.grid(True, linestyle="--", alpha=0.3)

    fig.tight_layout()
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.get_tk_widget().grid(row=1, column=0, sticky="nsew")
    if use_blit:
        fig.canvas.draw()
        canvas.draw_idle()
    plt.close(fig)