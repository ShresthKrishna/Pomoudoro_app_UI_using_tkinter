# timer.py

class TimerController:
    def __init__(self, root, timer_label, session_type_var):
        self.root = root
        self.timer_label = timer_label
        self.session_type_var = session_type_var

        self.work_session_completed = 0
        self.timer_id = None
        self.is_paused = False
        self.remaining_seconds = 0

        # Default durations (can be updated later)
        self.session_duration_map = {
            "Work": 25 * 60,
            "Short Break": 5 * 60,
            "Long Break": 15 * 60
        }

    def start_countdown(self):
        if self.timer_id:
            return
        session = self.session_type_var.get()
        count = self.session_duration_map.get(session, 5)
        self.countdown(count)

    def countdown(self, count):
        self.remaining_seconds = count
        mins, seconds = divmod(count, 60)
        self.timer_label.config(text=f"{mins:02d}:{seconds:02d}")

        if count > 0:
            self.timer_id = self.root.after(1000, lambda: self.countdown(count - 1))
        else:
            self.timer_id=None
            self.switch_session()

    def pause(self):
        if self.is_paused:
            self.resume()
        else:
            if self.timer_id:
                self.root.after_cancel(self.timer_id)
                self.timer_id = None
                self.is_paused = True

    def resume(self):
        if self.is_paused:
            self.countdown(self.remaining_seconds)
            self.is_paused = False

    def reset(self):
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        self.is_paused = False
        self.remaining_seconds = 0
        self.timer_label.config(text="00:00")
        self.session_type_var.set("Work")
        self.work_session_completed = 0

    def switch_session(self):
        session = self.session_type_var.get()
        if session == "Work":
            self.work_session_completed += 1
            if self.work_session_completed % 4 == 0:
                next_session = "Long Break"
            else:
                next_session = "Short Break"
        else:
            next_session = "Work"
        self.session_type_var.set(next_session)
