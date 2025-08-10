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
## [v1.4-pre] – 2025-05-23

### Added
- New Task Completion Dialog: When planned sessions for a task are finished, users can now:
  - Start a new task
  - Add more sessions to the current task
  - Continue without any task

### Fixed
- Timer tick loop no longer runs multiple instances due to incorrect `after()` syntax
- Timer label and duration state now correctly update after manual task reset
- Session continuation logic paused automatically after task plan completes

### Improved
- Manual End Session and Task Completion now integrated smoothly
- User control over session lifecycle has been fully implemented
## [v1.4.1-pre] – 2025-05-23

### Added
- Subtask Planner scaffolding and UI rendering
- New files: `subtask_engine.py`, `subtask_ui.py`
- Users can define subtasks under a task, each with its own goal and progress counter
- Subtasks are displayed in a collapsible panel under the Task Plan

### Changed
- Session logger updated to support optional `subtask` column in `session.csv`

### Fixed
- File path bug in subtask save logic (incorrect path traversal resolved)
- Panel placement bug causing overlap with timer resolved
- Return value added to `render_subtask_panel()` for integration stability
- JSON structure validation added to subtask entry system

## [v1.4.1-pre] – 2025-05-26

### Added
- Full subtask engine logic with persistent CRUD support:
  - `add_subtask`, `edit_subtask`, `delete_subtask`, `reset_subtasks`
- `mark_subtask_progress()` tracks and auto-advances current subtask
- Logger updated to support optional `subtask` field in `session.csv`
- Session completion callback now integrates with subtask engine

### Changed
- Subtasks are now auto-tracked in parallel to task session goals
- Work session completion conditionally pauses only if all subtasks are complete

### Fixed
- Guard added to prevent duplicate subtask names under a single task
- Debug logging added for JSON path traces and per-session subtask increments

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

## [v1.4.2] — 2025-05-29
### Added
- Subtask-to-Task Session Goal Sync:
  • Tasks now auto-adjust goal upward to match subtask total
  • Task goal never decreases automatically

- Session Context Mirror UI:
  • Replaced static session labels with task + subtask info
  • New dynamic label layout in `info_frame` below timer

### Improved
- Subtask session updates now visible in real time
- `reset_subtasks()` clears completed progress when switching tasks
- Visual consistency in layout via fixed width & grid anchor

## [v1.4.2] — 2025-05-30
### Added
- Subtask-Driven Task Goal Enforcement
  • Task session goals auto-raise to match only remaining subtask load
  • Manual goal input disabled when subtasks exist
  • Tooltip: “Goal is controlled by subtasks.”

- Session Context Mirror
  • Live dynamic display of Task + Subtask below timer
  • Updates at start/end/switch across session lifecycle
  • Special Break label: “Break – Next: [Subtask]”

- Subtask Editing Support
  • Subtask rows now editable inline (✎ button)
  • Allowed when session is paused or not started

### Fixed
- Task goal inflation from already completed subtasks
- Session label shifting on varying content lengths
- Session hang on subtaskless tasks with leftover sync
- Editing lock added for task name mid-session

## [v1.4.3-pre] — 2025-06-02

### Added
- One-time Honest Intent Prompt
  - Triggered before the first Work session per app run.
  - Captures short motivational statement (max 100 characters).
  - Integrated modal UI with dimmed overlay and theme styling.
  - Guarded with `has_prompted_intent` flag to prevent repeated display.
  - Integrated into `session_manager.py → start_session()`.

### Changed
- N/A

### Fixed
- N/A

## [v1.4.3-pre] — 2025-06-05

### Added
- Session resume tracking with original start time recovery
- `resumed` and `interrupted` flags in `session.csv` for better behavioral insights
- Hook into `WM_DELETE_WINDOW` to detect mid-session exits
- Timer state now preserves minimal recovery data if session is active on close

### Changed
- Resume flow now uses session metadata to ensure consistency across runs
- Logger accepts and logs behavioral flags alongside core session fields

### Fixed
- Session resume inconsistency: previously started new session instead of resuming
- Edge case where logs were missing interruption/resume data

## [v1.4.3-pre] — 2025-06-05

### Added
- Auto-resume logic after Break → Work transition
- New method `on_task_fetched(task_name)` to sync subtask progress and update session goals

### Changed
- `session_complete_cb()` now uses `_resume_post_task(task, session_type)` for cleaner session chaining
- Task selection from dropdown now dynamically updates Work session count based on subtasks

### Fixed
- Timer tick loop not resuming after state recovery
- Session goal not updating when past task was selected
- Crash caused by missing arg to `_resume_post_task(...)`

## [v1.4.3] – June 15, 2025

### Added
- Session continuation system with state restore (`resumed`, `interrupted`)
- Resume logic now uses original `start_time` for accurate logging
- CSV logging extended to track resumed and interrupted flags

### Changed
- `_resume_post_task()` now requires explicit `task` and `next_session`
- Timer tick loop reinitializes cleanly after state recovery

### Fixed
- Session goal inflation when scrolling through task history
- Task session count now syncs to subtask progress via `on_task_fetched()`
- Prevented type errors during session routing

## [2025-06-16] - v1.4.3 (UI-Agnostic Routing & SessionManager Refactor)

### Added
- `router.py`: Modular session routing functions `pause_for_task_decision()` and `resume_post_task()` now decoupled from `SessionManager`
- Routing logic now handles post-session decision-making cleanly across task transitions
- `manager.py`: Integrated routing callbacks and removed embedded UI/modal logic

### Changed
- SessionManager no longer presents dialogs or hardcodes transitions; all routed externally
- Session lifecycle flow now UI-safe and portable across frameworks (PySide6, Kivy)
- Task goal checks now direct routing into router-layer instead of internal logic calls

### Architecture
- Full milestone shift toward UI-agnostic design
- `engine/session_manager/` now contains five cleanly separated modules for backend session logic

## [2025-06-17] - v1.4.3 (Final PM Batch – Reflection Module & Routing Complete)

### Added
- `reflection.py`: New module to manage pre-session intent prompts and session start logic
- `maybe_trigger_intent()` determines if a reflection is needed before a Work session
- `_begin_session()` launches timer and locks subtasks after prompt

### Changed
- `SessionManager` no longer includes routing, dialog, or session transition logic
- All lifecycle flows now routed via `router.py` or `reflection.py`
- `session_complete_cb()` moved out of SessionManager to improve modularity
- UI elements are now passive receivers of backend engine logic

### Architecture
- All lifecycle phases (launch, start, tick, complete, post-task) are now UI-agnostic
- `engine/session_manager/` now contains six pure-logic modules, ready for future frontend transitions

## [v1.4.3] – 2025-06-18

### Added
- `reflection.py` module for session intent and post-session reflection prompts
- `maybe_trigger_intent()` called before first Work session
- `show_reflection_prompt()` collects user rating and notes after Work session ends
- Reflection fields: `focus_rating`, `session_notes`, and `intent_fulfilled = (rating ≥ 4)`
- Reflection data logged via `logger.log_session_data()`

### Changed
- `SessionManager.on_start()` now delegates to `reflection.py`
- `session_complete_cb()` fully moved into `router.py`
- Subtask locking logic centralized via `set_subtask_controls_enabled()` on session start
- UI state separation achieved for full session lifecycle

### Fixed
- Cleared stale reflection flags on session reset
- Prevented duplicate modal triggers from session reentry
- Logger format updated to conditionally append reflection fields

## 2025-06-22
**Work Done:**
- Split monolithic `SessionManager` into seven focused mixins:
  - `session_base`, `session_settings`, `session_timer`, `session_tasks`, `session_router`, `session_subtasks`, `session_dialogs`
- Reintroduced missing UI hooks in mixins:
  - `update_display_cb` in `session_timer`
  - `get_all_task_names` in `session_tasks`
- Added `SessionSubtasks` mixin to implement `set_subtask_editable`
- Updated `sess_manager.py` to inherit all mixins; adjusted `app.py` import to `engine.manager.sess_manager`
- Tweaked `on_task_fetched` logic to preserve manual `task_session_goal` values

**Decisions:**
- Adopt mixin-based architecture for clear separation of concerns
- Centralize all UI-related callbacks in `session_base` / `session_timer`
- Retain core routing logic in `session_router` to facilitate future extensions

**Next Steps:**
- Write unit tests for each mixin
- Remove deprecated `session_manager.py` once new modules are stable
- Update README to document new file structure
- Perform end-to-end QA on all dialog flows

## [v1.5.0-start] – 2025-08-10

### Added
- **Governance & Safety:** Began v1.5 work on branch `ui-agnostic-v1.5`; created snapshot `ui-agnostic-main-snapshot-2025-08-10`.
- **Rollback:** Tag `pre-v1.5-2025-08-10` on `main` for guaranteed return point.
- **Analytics Scope:** Plan to add `focus_rating`, `intent_text`, `reflection_notes` to `session.csv` and wire into dashboards (heatmap requires consistent `start_time`/`end_time`).

### Changed
- **Process:** Re‑enforced Logs‑First merges and “ui‑agnostic” branch naming convention.

### Notes
- No runtime behavior changes today; documentation, planning, and branch safety only.
