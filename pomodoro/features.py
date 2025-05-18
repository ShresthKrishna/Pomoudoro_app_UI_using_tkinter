# features.py

features = {
    "Core Timer Engine": {
        "Pomodoro session loop": True,
        "Start / Pause / Resume / Reset": True,
        "Auto-switching (Work → Break)": True,
        "Tick logic via after()": True,
        "TimerEngine class (UI-agnostic logic)": True
    },

    "Settings & Customization": {
        "User-defined durations": True,
        "Save/load user settings": True,
        "Theme manager (light/dark/minimalist)": False,
        "Audio alerts / ambient music support": False,
        "Background wallpapers / ambient mode": False
    },

    "Session Logging": {
        "Log completed sessions to CSV": True,
        "Log duration (minutes)": True,
        "Track task/subject (e.g. 'Math')": False,   # Task selector UI is pending
        "Log session start + end timestamps": True,
        "Log incomplete / manually-ended sessions": False,
        "Log user productivity rating (1–5)": False
    },

    "Analytics Dashboard": {
        "Sessions per Day chart": True,
        "Time spent by session type": True,
        "Streak tracking": True,
        "7-day activity summary": True,
        "Task-specific breakdown": False,  # Depends on task tracking being implemented
        "Pie / bar / line chart visuals": True,
        "Load fallback mock data for dev mode": True,
        "Switch to real data after first session": False,
        "Show placeholder message when no data exists": False,
        "Productivity vs Time heatmap (hour-wise)": False  # NEW IDEA
    },

    "UI & Navigation": {
        "Multi-screen layout": True,
        "Navigation via top buttons": True,
        "Modular screen loading via show_frame()": True,
        "Session history viewer": True,  # ✅ Implemented and live as Treeview
        "Clean theme layout (grid-based)": True
    },

    "Persistence & State": {
        "Save settings to JSON": True,
        "Restore settings on launch": True,
        "Save/resume timer state across app closes": False
    },

    "Gamified Analytics Unlocking": {
        "Unlock activity timeline after 1 session": False,
        "Unlock sessions/day chart after 3 sessions": False,
        "Unlock pie chart after 5 sessions": False,
        "Unlock streak tracker after 7 sessions": False,
        "Locked views with motivational placeholders": False,
        "Unlock messages and gamified progress cues": False
    },

    "Vision & Product Goals": {
        "Year-end summary (like Spotify Wrapped)": False,
        "Custom themes (light/dark/modern)": False,
        "Multi-task tracking & productivity tags": False,
        "Encourage deep focus & flow state UX": False,
        "Built-in productivity music engine": False,
        "User profiles or workspace presets": False,
        "Mood-enhancing UI for comfort & focus": False
    }
}
