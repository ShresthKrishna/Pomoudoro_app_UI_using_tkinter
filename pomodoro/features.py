features = {
    # ------------------------------------------------------------------
    #  CORE ENGINE & FRAMEWORK
    # ------------------------------------------------------------------
    "Core Timer Engine": {
        "Pomodoro session loop": True,
        "Start / Pause / Resume / Reset": True,
        "Auto-switching (Work → Break)": True,
        "Tick logic via after()": True,
        "TimerEngine class (UI-agnostic logic)": True
    },

    # ------------------------------------------------------------------
    #  USER SETTINGS & SENSORY ENVIRONMENT
    # ------------------------------------------------------------------
    "Settings & Customization": {
        "User-defined durations": True,
        "Save/load user settings": True,
        "Theme manager (light/dark/minimalist)": False,
        "Audio alerts / ambient music support": False,              # ⇐ research §5
        "Background wallpapers / ambient mode": False               # ⇐ research §5
    },

    # ------------------------------------------------------------------
    #  SESSION & REFLECTION LOGGING  ––  *MUST feed insights*
    # ------------------------------------------------------------------
    "Session Logging": {
        "Log completed sessions to CSV": True,
        "Log duration (minutes)": True,
        "Track task/subject (e.g. 'Math')": False,                  # Task selector pending
        "Log session start + end timestamps": True,
        "Log incomplete / manually-ended sessions": False,
        "Log user productivity rating (1–5)": True,                 # ⇐ research says rating is vital
        "Log intent (pre-session)": True,                           # NEW
        "Log intent_fulfilled (Yes/Partial/No)": True               # NEW
    },

    # ------------------------------------------------------------------
    #  ANALYTICS & INSIGHT DASHBOARD
    # ------------------------------------------------------------------
    "Analytics Dashboard": {
        "Sessions per Day chart": True,
        "Time spent by session type": True,
        "Streak tracking": True,
        "7-day activity summary": True,
        "Task-specific breakdown": False,                           # needs task selector
        "Pie / bar / line chart visuals": True,
        "Load fallback mock data for dev mode": True,
        "Switch to real data after first session": False,
        "Show placeholder message when no data exists": False,
        "Productivity vs Time heatmap (hour-wise)": False,
        "Intent fulfilment ratio": False,                           # ⇐ research §3 (actionable insight)
        "Best focus window insight": False                          # ⇐ research §3
    },

    # ------------------------------------------------------------------
    #  UI SHELL & NAVIGATION
    # ------------------------------------------------------------------
    "UI & Navigation": {
        "Multi-screen layout": True,
        "Navigation via top buttons": True,
        "Modular screen loading via show_frame()": True,
        "Session history viewer": True,
        "Clean theme layout (grid-based)": True,
        "Minimalist focus-first timer screen": False                # ⇐ research §2
    },

    # ------------------------------------------------------------------
    #  PERSISTENCE
    # ------------------------------------------------------------------
    "Persistence & State": {
        "Save settings to JSON": True,
        "Restore settings on launch": True,
        "Save/resume timer state across app closes": False
    },

    # ------------------------------------------------------------------
    #  TASK / SUBTASK
    # ------------------------------------------------------------------
    "Task & Subtask Integration": {
        "Subtask-Driven Task Goal Enforcement": True,               # v1.4.2
        "Task Editing (name + goal)": True
    },

    # ------------------------------------------------------------------
    #  LOW-PRESSURE GAMIFICATION  (research: avoid gimmicks)
    # ------------------------------------------------------------------
    "Low-Pressure Gamification": {
        "Unlock activity timeline after 1 session": False,
        "Unlock sessions/day chart after 3 sessions": False,
        "Unlock pie chart after 5 sessions": False,
        "Unlock streak tracker after 7 sessions": False,
        "Locked views with motivational placeholders": False,
        "Unlock messages and gamified progress cues": False,
        "Productivity garden / collectible": False                  # placeholder idea (Forest-style)
    },

    # ------------------------------------------------------------------
    #  VISION & LONG-RANGE GOALS
    # ------------------------------------------------------------------
    "Vision & Product Goals": {
        "Year-end summary (like Spotify Wrapped)": False,
        "Custom themes (light/dark/modern)": False,
        "Multi-task tracking & productivity tags": False,
        "Encourage deep focus & flow state UX": False,
        "Built-in productivity music engine": False,                # ties to ambient sound
        "User profiles or workspace presets": False,                # multiple workloads
        "Mood-enhancing UI for comfort & focus": False
    },

    # ------------------------------------------------------------------
    #  MOTIVATIONAL HABIT DESIGN  (behavior-first features)
    # ------------------------------------------------------------------
    "Motivational Habit Design": {
        "One Honest Intent Prompt (before session)": True,          # v1.4.3
        "End Session Reflection (How was this session?)": True,     # v1.4.3
        "Intent fulfilment confirmation": True,                     # NEW (research §1)
        "Streaks by Behavior or Task Type": False,
        "Gentle 'You Showed Up' Daily Messages": False,
        "Flexible Planning Reminders (non-intrusive)": False,
        "Weekly Practice Summary & Export": True,                   # v1.4.3+
        "Session Forecasting with Reflection": False,
        "Session Context Mirror (Task/Subtask Display)": True       # v1.4.2
    },

    # ------------------------------------------------------------------
    #  BEHAVIORAL INSIGHTS & PERSONALIZATION
    # ------------------------------------------------------------------
    "Behavioral Insights & Personalization": {
        "Adaptive timer suggestions": False,                        # research §5 (AI coach)
        "Personal best / milestone highlights": False,              # event-driven insights
        "Just-in-time gentle nudges": False                         # JITAI concept
    }
}
