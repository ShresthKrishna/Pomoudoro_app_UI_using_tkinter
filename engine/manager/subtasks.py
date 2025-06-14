from pomodoro.subtask_engine import get_total_subtask_goal, get_current_subtask_name

def fetch_subtask_data(task_name: str, session_type: str, session_counts: dict) -> dict:
    goal = get_total_subtask_goal(task_name)
    session_count = session_counts.get(session_type, 0) + 1
    subtask_name = get_current_subtask_name(task_name) if task_name else None

    return {
        "goal": goal if goal > 0 else 1,
        "subtask": subtask_name,
        "session_label": f"{session_type} Session {session_count}"
    }