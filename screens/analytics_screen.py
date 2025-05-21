import tkinter as tk
from pomodoro.analytics import generate_all_summaries, get_recent_sessions
from screens.analytics_dashboard import render_dashboard_layout
from screens.analytics_scrollable import render_scrollable_layout
from pomodoro.theme import theme

def render_analytics_screen(parent_frame, use_mock=False):
    for w in parent_frame.winfo_children():
        w.destroy()

    summaries = generate_all_summaries(use_mock=use_mock)
    history_rows = get_recent_sessions(20, use_mock)

    parent_frame.rowconfigure(0, weight=1)
    parent_frame.columnconfigure(0, weight=1)
    parent_frame.update_idletasks()

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

    for i in range(3): container.columnconfigure(i, weight=1)

    resize_job = [None]
    last_mode = [""]

    def on_resize(event=None):
        if resize_job[0]:
            parent_frame.after_cancel(resize_job[0])

        def decide():
            w = parent_frame.winfo_width()
            new_mode = "dashboard" if w >= 900 else "scrollable"
            if new_mode == last_mode[0]: return
            last_mode[0] = new_mode
            if new_mode == "dashboard":
                render_dashboard_layout(container, summaries, history_rows)
            else:
                render_scrollable_layout(container, summaries, history_rows)

        resize_job[0] = parent_frame.after(200, decide)

    parent_frame.bind("<Configure>", on_resize)
    parent_frame.after_idle(on_resize)


class LazyAnalyticsScreen(tk.Frame):
    def __init__(self, parent, use_mock=False, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.use_mock = use_mock
        self.has_rendered = False
        self.loading_label = tk.Label(self, text="Loading Analytics…", font=("Arial", 14))
        self.loading_label.pack(pady=20)
        self.bind("<Visibility>", self._on_visible)

    def _on_visible(self, event=None):
        if not self.has_rendered:
            self.after(100, self.render_once)

    def render_once(self):
        self.loading_label.config(text="Rendering...")
        self.update_idletasks()
        render_analytics_screen(self, use_mock=self.use_mock)
        self.has_rendered = True
