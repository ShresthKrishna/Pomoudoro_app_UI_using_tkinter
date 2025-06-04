import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pathlib import Path
from pomodoro.theme import theme


def show_reflection_prompt(root, intent_exists, on_submit_callback):
    dialog = tk.Toplevel(root)
    dialog.title("Session Reflection")
    dialog.configure(bg=theme["bg_color"])
    dialog.geometry("500x360")
    dialog.resizable(False, False)
    dialog.grab_set()

    base_dir = Path(__file__).parent
    icon_path_empty = base_dir / "icons" / "star.png"
    icon_path_filled = base_dir / "icons" / "star_filled.png"

    star_empty_img = Image.open(icon_path_empty).resize((32, 32))
    star_filled_img = Image.open(icon_path_filled).resize((32, 32))

    star_empty = ImageTk.PhotoImage(star_empty_img)
    star_filled = ImageTk.PhotoImage(star_filled_img)
    dialog.star_images = [star_empty, star_filled]  # prevent GC

    focus_var = tk.IntVar(value=0)
    stars = []

    def update_stars(val):
        focus_var.set(val)
        for i, btn in enumerate(stars, start=1):
            btn.config(image=star_filled if i <= val else star_empty)

    # --- Section 1: Focus Rating ---
    rating_frame = ttk.LabelFrame(dialog, text="How was your focus?", padding=10)
    rating_frame.pack(fill="x", padx=20, pady=(20, 10))

    stars_frame = tk.Frame(rating_frame, bg=theme["bg_color"])
    stars_frame.pack()

    for i in range(1, 6):
        btn = tk.Label(stars_frame, image=star_empty, bg=theme["bg_color"], cursor="hand2")
        btn.pack(side="left", padx=4)
        btn.bind("<Button-1>", lambda e, val=i: update_stars(val))
        stars.append(btn)

    # --- Section 2: Intent Fulfilled Dropdown ---
    intent_frame = ttk.LabelFrame(dialog, text="Did you fulfill your intent?", padding=10)
    intent_frame.pack(fill="x", padx=20, pady=(0, 10))

    intent_var = tk.StringVar(value="")
    intent_dropdown = ttk.Combobox(
        intent_frame,
        textvariable=intent_var,
        values=["Yes", "Partially", "No"],
        state="readonly"
    )
    intent_dropdown.pack(pady=5)

    # --- Section 3: Buttons ---
    button_frame = tk.Frame(dialog, bg=theme["bg_color"])
    button_frame.pack(pady=15)

    def submit():
        on_submit_callback(
            focus_var.get() if focus_var.get() > 0 else None,
            intent_var.get() if intent_var.get() else None
        )
        dialog.destroy()

    def skip():
        on_submit_callback(None, None)
        dialog.destroy()

    ttk.Button(button_frame, text="Submit Reflection", command=submit).pack(side="left", padx=10)
    ttk.Button(button_frame, text="Skip", command=skip).pack(side="left", padx=10)

    dialog.bind("<Return>", lambda e: submit())
    dialog.bind("<Escape>", lambda e: skip())
