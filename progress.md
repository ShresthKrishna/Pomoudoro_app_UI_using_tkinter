# 🛠️ Project Progress Journal: Pomodoro Productivity and Analytics App

---

# 📅 2024-04-28
## Update 1
**Work Done:**
- Created project folder structure:
  - assets/, pomodoro/, data/
- Moved tomato.png into assets/images/
- Created professional documentation files:
  - README.md, CHANGELOG.md, ASK.md, WORKLOG.md
- Updated README.md content to match new vision (Analytics + Task Tracking)

**Decisions Made:**
- Follow Google Data Analytics phases (Ask → Prepare → Process → Analyze → Share → Act)
- Project will support future features like:
  - Background image customization
  - User-selected background music
  - Year-end Spotify Wrapped-style summaries

**Next Steps:**
- Create `run_app()` in app.py
- Build Tkinter window with Top, Middle, Bottom Frames
- Launch from main.py and test basic structure

**Notes:**
- Keeping documentation very clean for portfolio visibility
- Will maintain clean commit history: small commits, clear messages
## Update 2
# 🛠️ Project Progress Journal: Pomodoro Productivity and Analytics App


**Work Done:**
- Finalized project commitment: building a professional-grade Pomodoro + Analytics App
- Defined project goals clearly: modular, scalable, theme-ready, analytics dashboard
- Decided to type all code manually for deep understanding (no copy-paste)
- Discussed and planned dynamic screen switching (Home, Settings, Analytics views)
- Designed basic dynamic `run_app()` architecture:
  - Top Frame → Navigation buttons (Home, Settings, Analytics)
  - Middle Frame → Dynamic content area (switches screens)
  - Bottom Frame → Reserved for future Checkmarks and Music controls
- Setup centralized theme dictionary for future theming flexibility
- Finalized strict study approach: Read official documentation for every library used

**Decisions Made:**
- Will build everything modularly (dynamic screens, centralized styling, separated logic files)
- Will not rush — focus on deep understanding and professional development habits
- Will keep PROJECTS.md updated after every major working session (private journal)

**Next Steps:**
- Type the full updated `run_app()` manually into `app.py`
- Type clean `main.py` calling `run_app()`
- Run and test that window with navigation switching works
- Once verified working → clean Git commit + push

**Notes:**
- ChatGPT will continue serving both as project guide and strict mentor
- Documentation reading and mastery mindset is now officially part of workflow
## ✅ Update: UI Frame Navigation and Layout Fix

**🗓 Date:** April 30, 2025  
**🔧 Module:** `run_app()` – Layout and Navigation  
**🎯 Goal:** Fix frame stacking and ensure button-based navigation (Home, Settings, Analytics) with responsive layout

---

### 🐞 Issue
- Labels weren’t centered or scaling well  
- Frames not switching cleanly  
- Layout didn’t stretch/adapt properly on resize  

---

### 🛠 Fix Implemented
- Used `.grid()` with `rowconfigure` and `columnconfigure` for flexible resizing  
- Created a `middle_frame` to contain dynamic sub-screens  
- Used `tkraise()` to switch between `home`, `settings`, and `analytics` views  
- Top navigation buttons placed using `pack(side="left", expand=True)` for consistent layout  

---

### 📈 Result
- ✅ UI now switches views correctly  
- ✅ Layout adapts responsively to window resizing  
- ✅ Code is cleaner and modular for future feature expansion

---

### 🧭 Suggested Next Steps
1. **Code Functionality**: Implement actual logic for each screen  
2. **UI/UX Styling**: Polish themes, use consistent colors, consider icons or rounded corners  
3. **Analytics Planning**: Begin sketching out what usage data to collect and how to visualize it  
4. **Final Polishing**: Structure `main.py`, prepare `README.md`, and set up for GitHub

---
