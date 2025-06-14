# engine/session_manager/state.py
from __future__ import annotations

from pomodoro.timer_state_manager import (
    save_timer_state as _save,
    load_timer_state as _load,
    clear_timer_state as _clear
)

def save(state_dict: dict):
    """Save current session state to disk."""
    _save(state_dict)

def load() -> dict | None:
    """Load session state from disk."""
    return _load()

def clear():
    """Clear saved session state (used after reset or new task)."""
    _clear()
