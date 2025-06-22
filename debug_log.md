# 📜 Debug Log
### 🐞 [April 30, 2025] – Frame Layout & Label Glitch
- **Issue**: Labels not scaling, frames not raising on button click
- **Fix**: Used `.grid()` layout with `tkraise()` logic inside `show_frame()` to enable navigation and responsiveness

### 🐞 [May 3, 2025] – Feature Flow Disruption from Learning Chat
- **Issue**: Learning chat introduced premature logic (timer, session dropdown) that conflicted with UI/UX design plans.
- **Fix**: Preserved functional logic but began UI cleanup by refactoring layout, especially control buttons and screen alignment. Realigned with planned workflow.
## 🐞 [May 3, 2025]

### ✅ Fixed: Start Button Glitch
- Issue: Pressing “Start” multiple times triggered overlapping `after()` loops.
- Fix: Guard added using `self.timer_id` to ensure only one countdown runs at a time.

### ✅ Fixed: Resume Function Inactive
- Issue: Clicking “Pause” halted timer, but did not resume when clicked again.
- Fix: Added `toggle_pause()` logic in `app.py` with `nonlocal` flag and `.config()` for dynamic text switch.

## ✅ Milestone: All listed bugs resolved in v1.0

## [2025-05-04] Timer Logic Refactor Debug Summary

- ✅ Timer stacking issue resolved by checking `is_running` in `start()`
- ✅ Resume now works via dedicated `resume()` method and pause toggle logic in `app.py`
- ✅ Remaining time now updates cleanly through `update_display_cb`
- ✅ Refactor allows headless testing; no Tkinter dependency in core logic

## [2025-05-04] - Session Logging Integration

### Observations
- Logging triggered cleanly at the end of each session via callback.
- `Path.mkdir(parents=True, exist_ok=True)` ensures folder existence — no FileNotFoundError.

### Tests Conducted
- Multiple sessions completed to test append behavior.
- CSV confirms consistent structure and no header duplication.

### Known Limitations
- Currently appends without limits — no cap on file size.
- Data is raw; not yet visualized or summarized in-app.

### To Revisit
- Once analytics is live, validate whether the logger output aligns with charts and summaries.


### 🐞 [May 11, 2025] – Scroll & Layout Toggle Discrepancy

**Issue**:
- Alternate version of `analytics_screen.py` added layout toggle between scroll and dashboard mode, but broke agreed GUI structure.
- Scrollbar existed but did not work — canvas height never expanded, scrollregion never updated.

**Fix**:
- Reimplemented scroll layout using correct `Canvas + Frame + Scrollbar` structure.
- Used `create_window()` and width binding.
- Reintegrated `render_scrollable_layout()` and `render_dashboard_layout()` with proper toggle logic via `parent_frame.winfo_width()`.

**Status**:
✅ Fixed. Dynamic switching works cleanly. Both layouts follow design structure.
"""

## 📅 2025-05-13 – Dashboard & Task Plan Integration Validation

**Feature Validations:**
- Confirmed Task Plan logic correctly tracks session counts and resets appropriately.
- Ensured no logging issues with empty tasks during breaks.
- Dashboard analytics layout verified against UI proposal (row-column spanning, widget alignment).

**Debugging Notes:**
- Verified responsive layout toggle (`>=900px`) without visual glitches.
- Confirmed all new summary functions (`analytics.py`) handle mock and real data correctly.

**No critical issues or regressions identified.**

## 📅 2025-05-15 – Stability Fix Log

**Resolved Issues:**
- 🔥 [Critical] `KeyError: 'daily_by_type'` → caused by incomplete mock summaries; patched mock return values.
- 🔧 [Visual] Task entry used `ttk.Entry` → replaced with `ttk.Combobox` + dynamic filtering to prevent mistypes and encourage reuse.
- 🧠 [State Loss] Resume timer state was not syncing across UI and task memory → consolidated under `session_manager`.
- 🎯 [UI Bug] Session type dropdown and session label were overlapping → corrected via `rowconfigure(minsize)` constraints.

**Root Cause Summary:**
- Several untracked changes during Git issues led to rollback of resume, task tracking, and combobox logic. These have now been reconstructed, modularized, and documented.
## 🐞 2025-05-18 – debug_log.md

**Issue 1**: KeyError in scrollable 7-day chart  
- Cause: Summary DataFrame sometimes lacked “Work” or other session keys.  
- Fix: Chart function now pads missing columns with zero-count data.

**Issue 2**: Canvas width did not adjust on window resize  
- Cause: Width was never updated using `canvas.itemconfig()` after `create_window()`.  
- Fix: Bound canvas width to frame container and dynamically updated it on `<Configure>`.

**Issue 3**: Removed bindings during refactor  
- Cause: Scrollregion and window width weren’t updating due to missing canvas/frame binding logic.  
- Fix: Restored `on_canvas_configure` and `on_container_configure` to fix dynamic layout.

**Issue 4**: Mis-scoped debounce handler  
- Cause: `resize_job[]` handle wasn't safely scoped, leading to invalid callback errors.  
- Fix: Moved debounce logic to outer scope; now cancels and replaces cleanly.

**Issue 5**: DPI scaling unrelated to layout flow  
- Cause: Font sharpness improved via OS DPI settings, but layout size remained unaffected.  
- Fix: DPI tweaks retained, but layout corrected using proper column/row configuration.

## 🐞 2025-05-19 – Lazy Rendering Fix for Analytics Screen

**Issue**: Analytics screen blocked window expansion on launch  
- Cause: Initial rendering involved multiple charts, summary generation, and heavy Matplotlib operations inside `render_analytics_screen()`, which delayed root layout expansion.
- Fix: Deferred rendering until navigation to the Analytics screen using a lazy load trigger. Layout now initializes fully before rendering begins.

**Result**:
- All screens now allow proper width and height expansion on drag.
- Slight delay on first Analytics load is acceptable and non-blocking.
- No regressions observed in navigation, DPI scaling, or layout responsiveness.

## 🐞 [May 21, 2025] – Session Lifecycle & CSV Logging Integration

**Issue**: No way to log manually ended (incomplete) sessions  
- Fix: Added `end_session()` method to `SessionManager`  
- Result: Captures accurate `start_time`, `end_time`, and `completed=False` flag on early session termination

**Issue**: CSV missing proper session completion status  
- Fix: Updated `log_session()` to accept `completed` flag and write it as `1` or `0`  
- Result: Sessions now properly marked as completed or interrupted in `session.csv`

**Issue**: session.csv file was logging to incorrect path  
- Cause: `Path("data")` resolved relative to module execution path  
- Fix: Introduced `PROJECT_ROOT` using `Path(__file__).resolve().parent.parent` to ensure correct output location

**Tests Conducted**:
- Verified session logging with debug prints after Start, End, and Reset flows
- Confirmed file size increments after each write
- Confirmed column values match expected output (e.g., `completed=0` on End Session)

**Status**: Session lifecycle logging is now structurally sound and location-safe
## 🐞 [May 23, 2025] – Task Completion Flow & Tick Loop Fixes

**Issue**: Timer tick loop was called recursively
- Cause: Used `after(..., tick_once())` instead of `after(..., tick_once)`
- Fix: Passed correct function reference; added `_tick_loop_running` flag to prevent overlaps

**Issue**: Timer label not refreshing after task reset
- Fix: Manually called `timer_label.config(...)` and `.update_idletasks()` to ensure redraw

**Issue**: Durations did not update after changing task/session type
- Fix: Explicit call to `update_durations()` inside `new_task()` to apply user settings

**Feature Bug**: Timer resumed automatically after task completion
- Fix: Session continuation now halted by default; requires user action from the dialog

**Validated**:
- Dialog blocks session flow until response
- Label and timer state refresh correctly post-selection
- Additional sessions correctly update task goal

## 🐞 [May 23, 2025] – Subtask Planner Integration

**Issue**: `user_tasks.json` was not being saved correctly  
- Cause: Used `parents[2]` in path resolution, which exited project scope  
- Fix: Adjusted to `parents[1]` to correctly point to `Pomodoro/data/`

**Issue**: Subtask panel overlapped with timer UI  
- Fix: Moved subtask container to `row=5` in `home_screen.py`

**Issue**: `render_subtask_panel()` returned `None`  
- Fix: Explicitly returned the frame container from function

**Issue**: JSON structure mismatch — expected list of dicts, got flat list  
- Fix: Enforced proper format via `add_or_update_task()` in `subtask_engine.py`

**Other Validations:**
- Confirmed session_manager does not interfere with subtask state
- Bound `task_var` to active subtask lookups successfully
- Verified read-only panel renders cleanly under all DPI modes

## 🐞 [May 26, 2025] – Subtask Engine and Session Flow Integration

**Issue**: Subtask logic not yet integrated into session completion  
- Fix: `mark_subtask_progress()` now called inside `session_complete_cb()`  
- Result: Active subtask is progressed, and `completed` count is updated in JSON

**Issue**: No subtask field in logger output  
- Fix: `logger.log_session()` updated to accept and log `subtask` name  
- Result: `session.csv` now includes optional `subtask` field per row

**Issue**: JSON not saving correctly with complex nesting  
- Fix: Created atomic `_save_all()` with debug instrumentation for path writes  
- Added guards for duplicate subtask names per task

**Validation**:
- Subtask progress correctly incremented after Work sessions
- Final subtask triggers session pause + task completion dialog
- Logger and session state updates are in sync with user flow

## 🐞 [May 26, 2025] – Subtask Engine and Session Flow Integration

**Issue**: Subtask logic not yet integrated into session completion  
- Fix: `mark_subtask_progress()` now called inside `session_complete_cb()`  
- Result: Active subtask is progressed, and `completed` count is updated in JSON

**Issue**: No subtask field in logger output  
- Fix: `logger.log_session()` updated to accept and log `subtask` name  
- Result: `session.csv` now includes optional `subtask` field per row

**Issue**: JSON not saving correctly with complex nesting  
- Fix: Created atomic `_save_all()` with debug instrumentation for path writes  
- Added guards for duplicate subtask names per task

**Validation**:
- Subtask progress correctly incremented after Work sessions
- Final subtask triggers session pause + task completion dialog
- Logger and session state updates are in sync with user flow

# Debug Log – Subtask Planner Phase 3 (v1.4.2)
## Date Range: 27–30 May 2025

---

### 🐛 Subtask goal included completed subtasks
- **Issue:** Task session goal increased even when all subtasks were already completed
- **Debug Method:** Print statements inside `get_total_subtask_goal()`
- **Resolution:** Filtered subtasks by `completed < goal`

---

### 🐛 Task/subtask labels not updating correctly
- **Issue:** Session labels on Home screen remained static or mismatched
- **Debug Method:** Manual testing + breakpoint in `update_session_info()`
- **Resolution:** Added `get_current_subtask_name()` helper; ensured update calls on every session switch

---

### 🐛 Label resizing caused layout jump
- **Issue:** Dynamic session labels caused timer section to shift on screen
- **Debug Method:** UI stress test using varying label content lengths
- **Resolution:** Created fixed-width `info_frame` and locked label widths with `width=40` and `anchor="center"`

---

### 🐛 Subtask edit UI not rendering updates
- **Issue:** Editing subtasks didn’t reflect changes until full refresh
- **Debug Method:** Visual inspection + tracing `populate()` flow
- **Resolution:** Centralized UI rebuild inside `populate()`; connected edit field with manager sync

---

### 🐛 Subtasks not cleared on new task selection
- **Issue:** When starting a new task, subtasks from previous task persisted
- **Debug Method:** Session logs showed mismatch; UI reflected stale subtasks
- **Resolution:** Added `reset_subtasks(task_name)` call in `_pause_for_task_decision()`

---

### 🐛 Editing main task name mid-session caused sync loss
- **Issue:** If the user edited the task name while session was running, logs became disconnected
- **Debug Method:** Observed broken logs and lost session mappings
- **Resolution:** Disabled task name editing once session starts

---

### 🐛 Fallback logic on non-subtask tasks triggered premature session end
- **Issue:** Tasks without subtasks were triggering session pause prematurely
- **Debug Method:** Controlled test of session lifecycle with and without subtasks
- **Resolution:** Guarded subtask checks in `session_complete_cb()` and clarified fallback condition

---
## [2025-06-02] — Honest Intent Prompt Integration

- Bug: Prompt reappeared on every Work session start.
  • Fix: Scoped `has_prompted_intent = False` to global app state.
  • Validation: Only shows once per app launch, not per task.

- Bug: Timer started in background before prompt was resolved.
  • Fix: Session start callback delayed until user confirms intent.
  • Validation: Timer now starts only after Start button is clicked.

- Bug: Modal layout caused frame overlap with timer section.
  • Fix: Fixed-width layout and centralized alignment using grid.
  • Validation: UI remains visually stable during prompt display.

## 🐞 [June 5, 2025] – Session Continuation & Resume Tracking

**Issue**: Session resume lost original start time  
- Fix: `session_manager.py` now restores `start_time` from `timer_state.json`  
- Result: Accurate durations are preserved across app restarts

**Issue**: App exit did not mark sessions as interrupted  
- Fix: Hooked into `WM_DELETE_WINDOW` inside `app.py`  
- Result: If timer is active, `interrupted = True` is saved in state

**Issue**: Resumed sessions did not show metadata in logs  
- Fix: `logger.py` updated to accept and write `resumed` and `interrupted` flags  
- Result: All relevant session rows in `session.csv` now include correct flags

**Validation**:  
- App closes mid-session → `interrupted = True` stored  
- On reopen + resume → `resumed = True`, same `start_time` restored  
- Logs now reflect accurate session continuity markers  

## 🐞 [June 5, 2025] – Session Count Sync + Task Selection Recovery

**Issue**: Timer didn’t start next Work session after Break  
- Fix: Called `_resume_post_task(task, "Work")` inside `session_complete_cb()`  
- Result: Timer auto-continues through session cycles

**Issue**: Timer restored state but tick loop didn’t restart  
- Fix: Added `start_tick_loop()` after `start_from(...)` in `resume_if_possible()`  
- Result: Countdown resumes visually and logically after resume

**Issue**: `_resume_post_task()` call failed due to missing argument  
- Fix: Updated all call sites to pass both task and next_session string  
- Result: Prevented crash on session transitions

**Issue**: Selecting old tasks didn’t sync session count with subtasks  
- Fix: Added `on_task_fetched()` in SessionManager to recompute and apply correct count  
- Result: Session goal reflects actual remaining subtasks

**Issue**: Session goal inflated on task scroll and never reset  
- Fix: Sync logic now sets task goal = sum of (subtask.goal - completed) or 1  
- Result: Goal always matches real subtask demand

**Validation**:  
- Task selection updates session count in real time  
- Timer transitions correctly across Work–Break cycles  
- Session resumes include visual + logical state recovery  

## 🐞 [June 15, 2025] – Task Session Sync & Resume Integration

**Issue**: Session timer did not continue from Break to Work automatically  
- Fix: Added `_resume_post_task(task, "Work")` inside `session_complete_cb()`  
- Result: Sessions transition automatically through the cycle when goals allow

**Issue**: App resume did not restore tick loop or visual countdown  
- Fix: Ensured `start_tick_loop()` is triggered after loading timer state  
- Result: Timer and labels visually reflect resumed session

**Issue**: Session count inflated when browsing past tasks  
- Fix: Introduced `on_task_fetched()` to recompute session goal from subtasks  
- Result: Session goal resets to match uncompleted subtasks (or 1 if none exist)

**Issue**: `_resume_post_task()` signature mismatch  
- Fix: Updated all call sites to use `task, next_session` format  
- Result: Avoids argument error during session flow transitions

**Validation**:  
- Resume retains correct `start_time`  
- CSV logs `resumed=True`, `interrupted=True` as expected  
- Task dropdown refresh updates session goal immediately  

## 🐞 [June 17, 2025] – Full Modularization of Session Flow

**Issue**: SessionManager was overloaded with mixed concerns  
- Fix: Refactored lifecycle routing (`pause`, `resume`, `complete`) into `router.py`  
- Result: SessionManager now handles only UI state and delegates all logic

**Issue**: Modal prompts tied to Tkinter directly  
- Fix: Moved intent prompt into `reflection.py` with conditional logic  
- Result: Prompts show only before first Work session, maintaining minimal friction

**Issue**: Repeating logic across pause and resume points  
- Fix: Centralized `resume_post_task()` and `pause_for_task_decision()` logic  
- Result: Simplified code reuse and routing clarity

**Validation**:
- Intent prompt shows once per app launch before first Work session
- Subtask controls locked/unlocked on session start via reflection module
- Labels update dynamically and route state cleanly
- All lifecycle transitions tested with UI stubs and internal prints

## 🐞 [June 18, 2025] – Intent + Reflection Prompt Integration

**Issue**: Intent prompt logic was hardwired into UI  
- Fix: Extracted into `reflection.maybe_trigger_intent()` with one-time condition  
- Result: Clean separation of pre-session logic with conditional invocation

**Issue**: No post-session feedback system  
- Fix: Added `show_reflection_prompt()` after Work sessions only  
- Captures user’s perceived focus and any notes for analytics

**Issue**: UI bloated with business logic  
- Fix: Moved `session_complete_cb()` to `router.py`; `on_start()` to `reflection.py`  
- Result: All routing and prompting now UI-agnostic

**Validation**:
- Reflection prompt shows after Work sessions only
- Focus rating, session notes, and success value saved to `session.csv`
- Subtask lock verified at session start
- Verified flags `_last_focus_rating`, `_last_session_success` reset correctly on new task
- Logger correctly includes optional fields when reflection is active

### 🐞 [June 22, 2025] – Missing update_display_cb in modular mixin
- **Issue**: App crashed on startup with `AttributeError: 'SessionManager' object has no attribute 'update_display_cb'` when initializing `TimerEngine`.  
- **Fix**: Added original `update_display_cb(mins, secs)` method into `session_timer.py` mixin to replicate legacy behavior.

### 🐞 [June 22, 2025] – Missing get_all_task_names in session_tasks mixin
- **Issue**: Home screen dropdown failed with `AttributeError: 'SessionManager' object has no attribute 'get_all_task_names'`.  
- **Fix**: Implemented `get_all_task_names()` in `session_tasks.py`, returning `get_all_tasks()` as in legacy code.

### 🐞 [June 22, 2025] – Absent set_subtask_editable integration
- **Issue**: Calls to `self.set_subtask_editable()` were no-ops; mixins lacked that method.  
- **Fix**: Created `SessionSubtasks` mixin (`session_subtasks.py`) with `set_subtask_editable(editable: bool)` invoking `set_subtask_controls_enabled`.