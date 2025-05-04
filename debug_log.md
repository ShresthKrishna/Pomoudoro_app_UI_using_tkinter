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
