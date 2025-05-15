import tkinter as tk
from tkinter import ttk


def render_session_history(frame, rows, theme):
    style = ttk.Style()
    style.configure("Treeview", font=theme["label_font"],
                    rowheight=theme["treeview_row_height"],
                    background=theme["bg_color"],
                    fieldbackground=theme["bg_color"])
    style.configure("Treeview.Heading", background=theme["button_color"])
    style.map("Treeview", background=[("selected", theme["accent_color"])])

    columns = ("#1", "#2", "#3", "#4", "#5")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)

    for i, h in enumerate(["Session #", "Type", "Completed At", "Duration", "Task"]):
        tree.heading(f"#{i + 1}", text=h)

    tree.column("#1", width=80, anchor="center")
    tree.column("#2", width=100, anchor="w")
    tree.column("#3", width=160)
    tree.column("#4", width=80)
    tree.column("#5", width=120)
    tree.grid(row=0, column=0, sticky="nsew")

    sb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    sb.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=sb.set)

    if not rows:
        tk.Label(frame, text="No sessions yet — your history will appear here.",
                 font=theme["label_font"], bg=theme["bg_color"]).grid(row=0, column=0, padx=20, pady=20)
    else:
        for r in rows:
            tree.insert("", "end", values=[
                r["session_number"],
                r["type"],
                r["completed_at"],
                f"{r['duration_minutes']} min",
                r.get("task", "")
            ])
