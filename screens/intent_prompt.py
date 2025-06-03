# pomodoro/focus_prompt.py

import tkinter as tk
from tkinter import ttk
from pomodoro.theme import theme

# Global session flag (should ideally move to SessionManager if modularized)
has_prompted_intent = False
user_intent = ""

def show_intent_prompt(root, on_start_callback):
    global has_prompted_intent, user_intent

    if has_prompted_intent:
        on_start_callback()
        return

    dialog = tk.Toplevel(root)
    dialog.title("Set Your Intent")
    dialog.configure(bg=theme["bg_color"])
    dialog.geometry("460x250")
    dialog.grab_set()
    dialog.resizable(False, False)

    # Title
    tk.Label(
        dialog,
        text="What's Your Focus?",
        font=theme["heading_font"],
        bg=theme["bg_color"],
        pady=10
    ).pack()

    # Prompt
    tk.Label(
        dialog,
        text="Briefly describe what you're aiming to accomplish.",
        font=theme["label_font"],
        bg=theme["bg_color"]
    ).pack(pady=(0, 10))

    # Entry field
    entry_var = tk.StringVar()
    entry = ttk.Entry(dialog, textvariable=entry_var, font=theme["entry_font"], width=40)
    entry.pack(pady=5)
    entry.focus_set()

    # Buttons
    button_frame = tk.Frame(dialog, bg=theme["bg_color"])
    button_frame.pack(pady=15)

    start_btn = ttk.Button(button_frame, text="Start ▶", state="disabled")
    cancel_btn = ttk.Button(button_frame, text="Cancel ✕", command=lambda: (dialog.destroy(), on_start_callback()))
    start_btn.grid(row=0, column=0, padx=10)
    cancel_btn.grid(row=0, column=1, padx=10)

    def validate_input(*args):
        val = entry_var.get()
        if 0 < len(val.strip()) <= 100:
            entry.config(foreground="black")
            start_btn.config(state="normal")
        elif len(val) > 100:
            entry.config(foreground="red")
            start_btn.config(state="disabled")
        else:
            start_btn.config(state="disabled")

    def on_start():
        global user_intent, has_prompted_intent
        user_intent = entry_var.get().strip()
        has_prompted_intent = True
        dialog.destroy()
        on_start_callback()

    entry_var.trace_add("write", validate_input)
    start_btn.config(command=on_start)
    dialog.bind("<Return>", lambda e: on_start() if start_btn['state'] == "normal" else None)
    dialog.bind("<Escape>", lambda e: cancel_btn.invoke())
