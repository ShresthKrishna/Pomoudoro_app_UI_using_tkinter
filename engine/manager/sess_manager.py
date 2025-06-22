from engine.manager.session_base import SessionBase
from engine.manager.session_settings import SessionSettings
from engine.manager.session_timer import SessionTimer
from engine.manager.session_tasks import SessionTasks
from engine.manager.session_router import SessionRouter
from engine.manager.session_subtasks import SessionSubtasks  # ← new
from engine.manager.session_dialogs import SessionDialogs
class SessionManager(
        SessionBase,
        SessionSettings,
        SessionTimer,
        SessionTasks,
        SessionRouter,
        SessionSubtasks,
        SessionDialogs):            # ← include here
    def __init__(self, root):
        SessionBase.__init__(self, root)
        SessionSettings.__init__(self)
        SessionTimer.__init__(
            self,
            self.update_display_cb,
            self.session_complete_cb,
            {k: self.duration_vars[k].get() * 60 for k in self.duration_vars}
        )
