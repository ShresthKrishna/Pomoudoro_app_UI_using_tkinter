
# 🎮 Gamified Analytics Unlocking – Design Document

## 🎯 Purpose
Transform the analytics screen from a static dashboard into a progressive, gamified experience that rewards user engagement and encourages consistency.

---

## 🔓 Unlock Tiers Based on Sessions Completed

| Sessions Completed | Unlock Message | Feature Unlocked |
|---------------------|----------------|------------------|
| == 0 | “Start your first session to begin tracking your progress!” | 🔒 All analytics locked |
| == 1 | “🎉 Great job! Your activity timeline is now unlocked.” | ✅ 7-day Activity Chart |
| >= 3 | “📈 You’ve been consistent! ‘Sessions per Day’ is now available.” | ✅ Sessions per Day Chart |
| >= 5 | “🧠 Time Master! See how your time is split by focus type.” | ✅ Pie chart: Time Distribution |
| >= 7 | “🔥 Streak mode unlocked! Track your productivity streaks.” | ✅ Current & Longest Streak Cards |

---

## 🧠 Backend Logic

- Add `count_logged_sessions()` in `analytics.py` to read the number of rows in `session.csv`
- Pass session count to `render_analytics_screen()`
- Conditionally render each section based on unlock criteria

```python
def count_logged_sessions():
    df = read_session_data()
    return len(df)
```

---

## 🎨 UI Behavior

- Locked sections display dimmed chart placeholders with unlock messages
- Use icons (e.g., 🔒) or shaded backgrounds for visual feedback
- Unlock messages should be positive, motivational, and progressive

---

## 🔄 Future Enhancements

- Add sounds or subtle animations when unlocking new sections
- Add badges (e.g., "5-Day Streak Master")
- Display “Your next unlock in X sessions” notice

---

## 🏁 Milestone Tag: `v1.2.1`
> Sub-milestone goal: Activate progressive analytics feedback loop via real-time data.

We can also, make trees, like actual visual trees, user can plant the seed and then as they work on that task, the tree grows