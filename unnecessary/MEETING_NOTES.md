# 📝 Meeting Notes – Milestone v1.2 Planning

**Date:** 2025-05-08
**Meeting Title:** Milestone v1.2 – Share & Act Strategy Planning
**Host:** Mother Chat
**Project Lead:** Apurv Krishna
**Attendees:** Code Development Team, Analytics Team, GUI/UX Team, Git Support (noted)

---

## 🎯 Project Vision

> Build a complete productivity system—not just a Pomodoro app. Track personalized study habits, visualize effort by focus area, and guide users through smart, low-friction feedback loops.

---

## ✅ Outcomes by Team

### 👨‍💻 Code Development Team

* **Settings Persistence**:

  * Store durations and preferences in `user_settings.json`
  * Utility functions for `save_user_settings()` and `load_user_settings()`

* **Dynamic Session Typing**:

  * Add `session_label` alongside `session_category` (e.g., Work, DSA)
  * Replace static session types with user-defined labels
  * Store user tasks in `user_tasks.json`

* **Proposed**:

  * Modularize config handling to `utils/storage.py`
  * Plan a “feature engine” for goals/tags later

---

### 📊 Analytics Team

* Support `session_label` as new grouping dimension

* Extend summaries:

  * Time per discipline
  * Consistency streak per label

* Plan for:

  * Daily heatmaps (future)
  * Smart insights (e.g., skipped goals)

* Suggest modular param-based functions for label aggregation

---

### 🎨 GUI / UX Team

* Replace session type dropdown with a searchable task selector
* Allow users to add tasks via button (no manual typing)
* Style with theme-aware colors/fonts
* Make analytics screen scrollable/responsive
* Future: implement theme preview and theme switching
* Propose `gui_utils.py` for reusable layout helpers

---

## 🗂 File-Level Changes (Expected)

* `analytics.py`, `logger.py`, `app.py`, `analytics_screen.py`
* `user_settings.json`, `user_tasks.json`
* New: `gui_utils.py`, `utils/storage.py`
* Theme hooks in `theme.py` and `theme_manager.py`

---

## 🧭 Next Steps / Assignments

| Task                       | Assigned To           |
| -------------------------- | --------------------- |
| Save/load settings         | Code Team             |
| Task selector interface    | GUI Team              |
| Group analytics by label   | Analytics Team        |
| Modular GUI helpers        | GUI Team              |
| Schema support + migration | Code + Git (optional) |

---

## ✅ Agreed Focus of v1.2

* Real session label tracking
* Responsive and user-friendly analytics screen
* Persistent user configuration
* Modular polish to enable upcoming features like sharing, reminders, insights

---

**Meeting Adjourned** – Apurv to greenlight implementation per finalized plan. All teams standing by.
### 🧩 UI Rationalization – "Sessions per Day" vs. "7-Day Activity Overview"
**Date:** 12 May 2025  
**Raised by:** Human Lead  
**Logged by:** Mother Chat 3.0

**Discussion:**  
The "Sessions per Day" chart (total sessions per calendar day) appears redundant alongside the "7-Day Activity Overview" (stacked chart by session type). Why keep both?

**Insights:**
- "Sessions per Day" gives quick insight into consistency over time — fewer details, easier to interpret at a glance.
- "7-Day Activity Overview" is more diagnostic and complex, ideal for experienced users.
- Useful for progressive unlocking/gamification: e.g., show "Sessions per Day" first, unlock detailed 7-day view later.
- Also valuable for compact layouts or mobile adaptation.

**Outcome:**
Keep both for now. Consider UI toggle or layout consolidation in later iterations.

**Suggested Actions:**
- Possible chart toggle UI (`[● Total] [○ By Type]`)
- Optional conversion of “Sessions per Day” to a summary KPI card

### 🤝 Task Analytics Handoff – Coordination Summary  
**Date:** 12 May 2025  
**Logged by:** Mother Chat 3.0  
**Participants:** Code Chat, Analytics Chat, UI/UX Chat  

---

**Milestone:** Task Plan logging now live — real `task` values written to `session.csv` during Work sessions.

---

**Analytics Team Response:**  
✅ `get_recent_sessions()` already compatible with task column  
✅ Treeview will add new “Task” column (width=100, stretch=True)  
✅ `generate_all_summaries()` to be extended with:

- `summarize_time_per_task()` → total minutes per task
- `count_sessions_per_task()` → frequency per task
- (Optional) `daily_task_timeline()` for stacked view or Gantt-style display

All functions will handle missing/empty task values without failure.

---

**UI/UX Implication:**  
Task column can be added to the Session History Viewer  
Design space for a future “Top Tasks” bar chart and task-level pie chart

---

**Next Step:**  
Analytics team will send final implementations of summary functions.  
UI/UX may prepare chart containers under their modular layout system.

### 🧭 Persistent Task System Design + Execution Plan  
**Date:** 14 May 2025  
**Logged by:** Mother Chat 3.0  
**Context:** Product design discussion initiated by Human Lead to plan how multi-task tracking, subtasks, and resume functionality should be logically and professionally implemented for recruiter-visible project depth.

---

## 🧠 User Need

> Users want to log focused tasks, possibly with subtasks, and resume work reliably across sessions.  
> Must support unexpected interruptions (app closes) without data loss.

---

## 🎯 Guiding Principle
- Implement reliable **resume timer and task state memory** before building subtask layers
- Ensure the app behaves like a real productivity assistant, not just a stopwatch

---

## 🔂 Feature Order & Reasoning

| Step | Feature | Purpose |
|------|---------|---------|
| 1 | **Resume Timer + State File** | Enables app to recover timer/task if closed mid-session |
| 2 | **Persistent Task Memory** | Saves user-defined tasks across launches for auto-suggest |
| 3 | **Subtask Planning** | Allows structured task breakdown (e.g., 3 subtasks for 6 Pomodoros) |
| 4 | **Subtask Completion Handling** | Option to finish early, reassign Pomodoros, or mark complete |
| 5 | **Visual Task Progress** | Progress bars, daily indicators, streaks per task |

---

## 📦 Data File Design (for resume state)
```json
{
  "active": true,
  "session_type": "Work",
  "remaining_seconds": 912,
  "session_counts": {"Work": 3, "Short Break": 2},
  "task": "Write Report",
  "task_sessions_remaining": 2,
  "timestamp": "2025-05-14T16:10:00"
}
