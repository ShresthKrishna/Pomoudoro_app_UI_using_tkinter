import json
from pathlib import Path
from datetime import datetime

TIMER_STATE_PATH = Path("data/timer_state.json")

def save_timer_state(state_dict):
    TIMER_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(TIMER_STATE_PATH, "w") as f:
        json.dump(state_dict,f, indent=2, default=str)

def load_timer_state():
    if not TIMER_STATE_PATH.exists():
        return None
    try:
        with open(TIMER_STATE_PATH, "r") as f:
            state = json.load(f)
        if state.get("active"):
            return state
    except Exception as e:
        print("Error Loading the file:",e)
    return None

def clear_timer_state():
    if TIMER_STATE_PATH.exists():
        TIMER_STATE_PATH.unlink()