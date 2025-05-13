# 📜 CHANGELOG

All notable changes to this project will be documented here.

---

## [Unreleased]
- Updating documentation files
- Preparing initial folder structure
## [Unreleased]
- Refactored UI layout to match design guidelines
- Integrated functional start button with countdown logic
- Applied centralized theming to top/mid/bottom frames
- Reorganized control buttons for cleaner bottom-frame structure
- Logged workflow deviation and restored design alignment
## [2025-05-04] - Mid-Day

### Added
- `timer.py`: Modular class `TimerController` encapsulating all timer logic.

### Changed
- `app.py`: Now imports and interacts with `TimerController` for countdown functionality.
- Integrated `Pause` and `Resume` toggle with UI feedback.

### Fixed
- Prevented multiple countdown overlaps by checking `self.timer_id` before starting.
## [v1.0] - 2025-05-04

### Added
- `timer.py` with `TimerController` class to encapsulate countdown logic
- Button wiring and toggle logic for Pause/Resume
- Dynamic UI layout using `grid()` and centralized `theme` dictionary

### Fixed
- Timer glitch when pressing Start multiple times
- Resume function not responding due to missing toggle behavior

## [v2.0-alpha] - 2025-05-04

### Changed
- Replaced `TimerController` with `TimerEngine` class in `timer_engine.py`
- Moved timer loop control out of logic class into `app.py` via `after()`

### Added
- Callback system to update UI and handle session transitions
- Toggle Pause/Resume button with internal `is_paused` flag

### Fixed
- Bug: resume functionality wasn't working
- Bug: Start button stacking multiple countdown instances

## [2025-05-04] - Added Session Logging System

### Added
- `logger.py` module under `pomodoro/` for centralized session logging.
- Logging uses CSV file format for simplicity and analysis compatibility.
- CSV file is auto-created if missing (`data/session.csv`) and includes header.

### Changed
- Modified `session_complete_cb()` in `app.py` to call `log_session()` with session type, timestamp, and number.

### Notes
- This lays the groundwork for the upcoming analytics dashboard.

## [2025-05-11] - Layout System Stabilization & Analytics Toggle Integration

### Added
- Scroll vs Dashboard toggle inside `render_analytics_screen()` using screen width detection
- `render_dashboard_layout()` now uses correct grid layout (brick wall style)
- Scroll layout uses canvas, scrollbar, dynamic region binding

### Fixed
- Scrollbar not working in third-party version due to incorrect window configuration
- Analytics layout now stable across screen sizes with automatic switching
"""
- ## [2025-05-12] - Task Plan Feature Added

**Added**
- "Task Plan" section to Home screen: task name entry + session goal spinbox
- Internal tracking of task state across multiple Pomodoros
- Auto-clearing of task field when planned sessions complete

**Changed**
- Session logging now includes task name for Work sessions

**Fixed**
- Prevented premature task resets between consecutive Pomodoros

## [2025-05-13] - Task Analytics Integration & Chart Flexibility

### **Added**
- `analytics.py`: New summarizer functions `summarize_time_per_task()` and `count_sessions_per_task()` for task-based insights.
- `mock_data.py`: Added `per_task_time` and `task_frequency` mock data to support new analytics visualizations in development mode.
- `charts.py`: Made `draw_bar_chart()` and `draw_pie_chart()` configurable with `x_key`, `y_key`, `label_key`, and `value_key` parameters.
- `analytics_screen.py`: Introduced two new chart sections in the scrollable layout:
  - **Top Tasks by Time** (horizontal bar chart)
  - **Task Frequency Breakdown** (pie chart)

### **Changed**
- `generate_all_summaries()` now includes `per_task_time` and `task_frequency` keys for downstream chart rendering.
- All chart calls in `analytics_screen.py` explicitly specify key mappings to align with flexible chart function signatures.
- Chart functions are now resilient to column mismatches and default to human-readable axis titles.

### **Fixed**
- Handled `KeyError` when mock summaries lacked expected keys for task-based charts.
- Clarified inconsistent return types in analytics helpers with updated type hints.
- Improved UI safety: pie/bar charts now fail gracefully when passed empty or malformed data.

## [2025-05-13] - Task Plan & Analytics Dashboard Update

**Added:**
- Task Plan input and session goal tracking on Home screen.
- Auto-clearing task input after planned sessions.
- Dashboard line chart for clearer 7-day session-type trends.
- New analytics summarizers: `summarize_daily_by_type()`, `summarize_daily_for_tasks()`.

**Changed:**
- Updated dashboard layout to clearly group related analytics visually.
- Enhanced placeholder structure, with vertical spanning for task frequency visuals.

**Fixed:**
- Ensured session logging schema compatibility (no breaking changes).
- Verified seamless layout-toggle logic based on screen width.
