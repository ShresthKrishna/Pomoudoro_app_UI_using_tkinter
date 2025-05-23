# 📚 ASK Phase - Pomodoro Productivity and Analytics App

## Topic
Personal productivity and learning efficiency using time tracking.

## Problem
Lack of proper session tracking leads to unfocused learning effort.

## Metrics
- Total Focus Time
- Task-specific Focus Time
- Daily, Weekly, Monthly Analysis
- Year-End Summary

## Stakeholders
- Primary: User (Learner)
- Secondary: Recruiters/Reviewers

## Audience and Impact
User-focused, clean graphical insights to aid in decision making and motivation.

## How Data Helps
Allows better planning, reflection, and goal setting based on real effort data.
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
