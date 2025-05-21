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

## [2025-05-14] - v1.3 Final Dashboard Layout & Task Analytics Integration

**Added:**
- Line chart: 7-Day Activity Overview (session type trends)
- Dropdown for task trend overlay using `summarize_daily_for_tasks()`
- Task analytics visuals:
  - Top Tasks by Time (bar)
  - Task Frequency Breakdown (pie)
- `draw_line_chart()` function in `charts.py` for reusable multi-line trends

**Changed:**
- Finalized 3×4 dashboard layout with improved grid placement
- `Task Frequency` chart now spans 2 rows for visual balance
- Scrollable layout updated to match dashboard structure and interactivity

**Fixed:**
- All charts now handle empty/mock data cleanly
- Ensured layout toggle between scrollable and dashboard is seamless

## [2025-05-15] – Codebase Modularization & Resume Logic Fixes

**Added:**
- Modular file structure (split `app.py` into reusable modules)
- `task_memory.py` for persistent task tracking
- `session_manager.py` to centralize resume + session state handling
- Modular bottom controls (start/pause/reset)

**Changed:**
- Task input is now a live-filtering `ttk.Combobox`
- All charts now fail-safe against missing pivot columns
- Visual layout rebuilt with consistent row configs

**Fixed:**
- Crashes from missing keys (`daily_by_type`) in mock summaries
- Task memory no longer appends unlimited entries
- UI glitches around timer/task/session label stacking resolved

## [v1.4-pre] – 2025-05-18

**Added**
- Full-width and height resizing support for analytics screen layouts.
- DPI scaling integration for better display on high-resolution screens.
- Unified selector for toggling between session type and task trends in 7-day chart.

**Changed**
- The 7-day activity chart now pads missing session types to ensure consistent rendering.
- Layout switching logic now uses proper debounce to avoid redundant redraws.

**Fixed**
- `KeyError` when summary data omitted session types in trend charts.
- Canvas and inner frame width mismatch resolved with proper window bindings.
- Restored dynamic scrollregion resizing after missing `<Configure>` events were re-bound.
- Prevented layout flicker during resize by stabilizing debounce and redraw order.

## 🐞 2025-05-19 – Lazy Rendering Fix for Analytics Screen

**Issue**: Analytics screen blocked window expansion on launch  
- Cause: Initial rendering involved multiple charts, summary generation, and heavy Matplotlib operations inside `render_analytics_screen()`, which delayed root layout expansion.
- Fix: Deferred rendering until navigation to the Analytics screen using a lazy load trigger. Layout now initializes fully before rendering begins.

**Result**:
- All screens now allow proper width and height expansion on drag.
- Slight delay on first Analytics load is acceptable and non-blocking.
- No regressions observed in navigation, DPI scaling, or layout responsiveness.

## [v1.4-pre] – 2025-05-21

### Added
- Unified Start/End session button with dynamic label and style based on session state
- New `completed` column in `session.csv` to distinguish full vs manually ended sessions
- `end_session()` function to handle early termination and proper logging

### Fixed
- File path issue in session logging resolved using `PROJECT_ROOT`
- Confirmed CSV file write behavior and schema consistency across manual and automatic ends

### Notes
- Logging now fully supports session duration and intent integrity
- Button visual behavior is consistent with task state and timer phase
