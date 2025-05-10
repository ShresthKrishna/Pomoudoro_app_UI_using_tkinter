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

### 🐞 [May 9, 2025] – Scroll Area Not Expanding

- **Issue**: Analytics screen scrollbar worked, but canvas height was stuck in a small container. User couldn’t see full visualizations.
- **Symptoms**:
  - Treeview was hidden
  - Resizing the window had no effect
- **Root Cause**:
  - `canvas.create_window()` not bound to `event.width`
  - `parent_frame.rowconfigure()` missing weight for canvas expansion
- **Fix (by partner)**:
  - Bound canvas width using `canvas.itemconfig()` on `<Configure>`
  - Updated layout weights and grid logic
  - Confirmed scroll works end-to-end across all analytics sections

### 🐞 [May 10, 2025] – Session Label Count Bug & Long Break Logic

**Issue 1:**
- Session label incorrectly displayed global count (e.g., "Short Break Session 2" on first break)

**Root Cause:**
- Was using `timer_engine.completed_session`, which counts every session, not per-type

**Fix:**
- Introduced `session_counts` dictionary to track session numbers per type
- Updated session label logic in both Start and Complete callbacks

---

**Issue 2:**
- Long Break never triggered

**Root Cause:**
- Logic was based on global `completed_session` which included breaks

**Fix:**
- Added `work_sessions_completed` counter
- Long Break now triggers every 4 Work sessions
