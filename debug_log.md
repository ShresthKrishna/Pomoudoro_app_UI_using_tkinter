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
