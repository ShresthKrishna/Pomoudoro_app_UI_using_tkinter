#POMODORO GUI BY SHRESTH
from tkinter import *
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
CHECK = "✔"
timer = None

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)
    timer_label.config(text="Timer")
    canvas.itemconfig(timer_text, text="00:00")
    check_label.config(text="")
    global reps
    reps = 0
# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps += 1
    work_sec = WORK_MIN*60
    short_break = SHORT_BREAK_MIN * 60
    long_break = LONG_BREAK_MIN * 60
    if reps%2 != 0:
        count_down(work_sec)
        timer_label.config(text= "Work", fg= PINK)
    elif reps%2 == 0:

        if reps == 8:
            count_down(long_break)
            timer_label.config(text="Break", fg=RED)
        else:
            count_down(short_break)
            timer_label.config(text="Break", fg= GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    canvas.itemconfig(timer_text, text=f"{count//60:02}:{count%60:02}")
    if count > 0:
        global timer
        timer = window.after(100, count_down, count - 1)
    else:
        start_timer()
        if reps%2==0:
            check_label.config(text=CHECK*(reps//2))


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomoudoro")
window.config(padx=100, pady=50, bg=YELLOW)


canvas = Canvas(width= 200, height=224, bg= YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(102, 130,text= "00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(row=1, column=1)


timer_label = Label(text="Timer", font=(FONT_NAME,45, "bold"), fg= GREEN,bg= YELLOW)
timer_label.grid(row=0, column=1)

start_button = Button(text="Start", command=start_timer,highlightthickness=0)
start_button.grid(row=2, column=0)

reset_button = Button(text="Reset",highlightthickness=0,command= reset_timer)
reset_button.grid(row=2, column=2)

check_label = Label( font=(FONT_NAME,20, "bold"), fg=GREEN,bg= YELLOW)
check_label.grid(row=3, column=1)







window.mainloop()
