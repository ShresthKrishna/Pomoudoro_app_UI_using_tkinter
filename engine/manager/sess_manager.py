from engine.manager.session_base import SessionBase
from engine.manager.session_settings import SessionSettings
from engine.manager.session_timer import SessionTimer
from engine.manager.session_tasks import SessionTasks
from engine.manager.session_router import SessionRouter
from engine.manager.session_subtasks import SessionSubtasks
from engine.manager.session_dialogs import SessionDialogs
class SessionManager(
        SessionBase,
        SessionSettings,
        SessionTimer,
        SessionTasks,
        SessionRouter,
        SessionSubtasks,
        SessionDialogs):
    def __init__(self, root):
        SessionBase.__init__(self, root)
        SessionSettings.__init__(self)
        SessionTimer.__init__(
            self,
            self.update_display_cb,
            self.session_complete_cb,
            {k: self.duration_vars[k].get() * 60 for k in self.duration_vars}
        )
        self.on_manual_session_required = lambda: self.frames["home"].show_paused_state()
