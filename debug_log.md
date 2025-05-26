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
