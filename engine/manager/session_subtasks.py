# engine/manager/session_subtasks.py


class SessionSubtasks:
    """
    Controls enabling/disabling of your subtask UI widgets.
    """

    def set_subtask_editable(self, editable=True):
        if hasattr(self, "_subtask_controls"):
            for widget in self._subtask_controls.values():
                try:
                    state = "normal" if editable else "disabled"
                    widget.configure(state=state)
                except Exception as e:
                    print(f"[DEBUG] Subtask widget toggle failed: {e}")
