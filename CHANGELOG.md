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

## [2025-05-09] - Scrollable Analytics Layout Implemented

### Added
- `analytics_screen.py`: Full vertical scroll implementation using Canvas + Frame
- Dynamic row placement for each analytics block: Bar, Pie, Cards, Chart, Treeview
- Fallback message added to Treeview when session list is empty

### Changed
- `app.py`: Added `use_mock` flag and passed it into `render_analytics_screen`
- UI frame structure adjusted to support expandable scrollable views

### Fixed
- Broken scroll behavior where canvas remained in a confined area
- Scrollbar now properly responds to window resizing and content height

## [2025-05-10] - Session Tracking Logic Refactor

### Changed
- Replaced global session counting with per-type session counters
- Long Break trigger logic now based on actual Work sessions completed

### Fixed
- Incorrect session label display (was showing Short Break Session 2 as first break)
- Long Breaks not appearing at all due to faulty modulo logic

### Added
- `session_counts` dictionary
- `work_sessions_completed` tracker
- Updated `reset_session()` to clean internal counters and labels
