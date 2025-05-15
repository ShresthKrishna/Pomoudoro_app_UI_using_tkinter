"""
 A modular, UI-agnostic timer engine.

 Args:
     update_display_cb (function): Called every second to update the timer display (min, sec).
     session_complete_cb (function): Called when a session ends.
     durations (dict): Dictionary of durations in seconds: {"Work": 1500, "Short Break": 300, ...}
 """


class TimerEngine:

    def __init__(self, update_display_cb, session_complete_cb, durations):
        self.update_display_cb = update_display_cb
        self.session_complete_cb = session_complete_cb
        self.durations = durations

        self.remaining = 0
        self.session_type = "Work"
        self.is_running = False
        self.is_paused = False
        self.completed_session = 0

    def start(self, session_type="Work"):
        if self.is_running:
            return
        self.session_type = session_type
        self.remaining = self.durations.get(session_type, 1500)
        self.is_running = True
        self.is_paused = False
        self.tick()

    def update_durations(self, new_durations):
        self.durations = new_durations

    def tick(self):
        if self.is_paused or not self.is_running:
            return
        mins, secs = divmod(self.remaining, 60)
        self.update_display_cb(mins, secs)
        if self.remaining > 0:
            self.remaining -= 1
        else:
            self.completed_session += 1
            self.is_running = False
            self.session_complete_cb(self.session_type, self.completed_session)

    def pause(self):
        if self.is_running:
            self.is_paused = True

    def resume(self):
        if self.is_paused and self.is_running:
            self.is_paused = False

    def reset(self):
        self.is_running = False
        self.is_paused = False
        self.remaining = 0
        self.completed_session = 0
        self.session_type = "Work"
        self.update_display_cb(0, 0)

    def start_from(self, seconds, session_type):
        self.remaining = seconds
        self.is_running = True
        self.is_paused = False
        self.session_type = session_type
        self.tick()