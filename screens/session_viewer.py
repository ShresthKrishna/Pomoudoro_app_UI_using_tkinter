import tkinter as tk
from tkinter import ttk

def render_session_history(frame, rows, theme):
    frame.rowconfigure(0, weight=1)
    frame.columnconfigure(0, weight=1)

    style = ttk.Style()
    style.configure("Treeview",
                    font=theme["label_font"],
                    rowheight=theme["treeview_row_height"],
                    background=theme["bg_color"],
                    fieldbackground=theme["bg_color"])
    style.configure("Treeview.Heading", background=theme["button_color"])
    style.map("Treeview", background=[("selected", theme["accent_color"])])

    columns = ("#1", "#2", "#3", "#4", "#5")
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)
    tree.grid(row=0, column=0, sticky="nsew")

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

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    tree.configure(yscrollcommand=scrollbar.set)

    if not rows:
        tk.Label(frame, text="No sessions yet — your session history will appear here.",
                 font=theme["label_font"], bg=theme["bg_color"]).grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
    else:
        for row in rows:
            tree.insert("", "end", values=[
                row["session_number"],
                row["type"],
                row["completed_at"],
                f"{row['duration_minutes']} min",
                row.get("task", "")
            ])
