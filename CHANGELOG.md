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
