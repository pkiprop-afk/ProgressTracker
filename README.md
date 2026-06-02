# ProgressTracker
# 📊 Activity Tracker

A GitHub-style contribution heatmap + daily task checker built with Streamlit and Python. Pre-loaded with 6 months of real Google Calendar history. Check off your daily tasks, watch the color intensity build up — just like GitHub contributions.

---

## Preview

```
📊 Activity Tracker
─────────────────────────────────────────────────────────
🔥 Streak: 184d   📅 Total: 1,027   ⭐ Best: 12 · Jun 1   📊 Week: 29

Dec  ░░▒▒▒▒░░░░▒▒▒▒░░▒▒▒▒▒▒▒▓▓▓▓▓▓
Jan  ▒▒▒▒░▒▒▒▒▒▒▒▒▓▒▒▒▒▒▒▒▒▒▓▒▒▒▒▒
Feb  ▒▒▒▒▒▒▒░▒▒▒▒▒▒░▒▒▒▒▒▒░▒▒▒▓▒▒░
Mar  ░▒▒▒▒▒░░▒▒▒▒▒░░▒▒▒▒▒░▒▒▒▒▒▒░
Apr  ░▒▒▒▒▒░░▒▒▒▒▒░░▒▒▒▒▓░▒▓▒▓▓▓░
May  ▓▒░▓▓▓▓▒░▓▓▓▓▓▒░▓▓▓▓▓▒░▓▓▓▓▓
Jun  ██░░░░░░░░░░░░
─────────────────────────────────────────────────────────
Tuesday, Jun 2 2026  🔴 Peak

☑ Bible Study      ☑ Pre-Market Prep
☑ Trading Session  ☑ Study Block
☑ Focus Time       ☑ Gym
☑ Lunch            ☑ Coding
☑ Evening Study    ☐ Church
                   [✅ Save progress]
```

---

## Features

- **GitHub-style heatmap** — 27 weeks of history rendered as a colored grid. Each square represents one day. Darker green = more tasks done.
- **Click any square** to jump directly to that day's task list.
- **10 daily checkboxes** matching your Google Calendar routine.
- **Auto-calculated intensity** — score 0–10 updates the heatmap color in real time after saving.
- **Persistent storage** — completions saved locally in SQLite (`tracker.db`). No cloud, no account needed.
- **Historical data baked in** — 184 days of real Google Calendar data (Dec 2025 – Jun 2026) pre-loaded as a baseline.

---

## Setup

### Requirements

- Python 3.10+
- pip

### Install

```bash
# Clone or unzip the project, then:
pip install -r requirements.txt
```

### Run

```bash
streamlit run app.py
```

Opens at **http://localhost:8501**

---

## Usage

### Checking off tasks

1. Open the app — it defaults to today's date.
2. Check each task as you complete it during the day.
3. Hit **✅ Save progress** — the heatmap square for today updates immediately.

### Navigating to other days

- **Click any heatmap square** to jump to that day.
- Or use the **date picker** below the heatmap.

### Historical days (before today)

Squares before today show Google Calendar event counts as a baseline. If you open a historical day and manually check tasks, your checked count replaces the calendar count going forward.

---

## Intensity Levels

| Score | Level    | Heatmap color   |
|-------|----------|-----------------|
| 0     | ⬜ Rest   | `#161b22` empty |
| 1–2   | 🟩 Light  | `#0e4429`       |
| 3–5   | 🟨 Active | `#006d32`       |
| 6–9   | 🟧 Grind  | `#26a641`       |
| 10    | 🔴 Peak   | `#39d353`       |

---

## Project Structure

```
activity_tracker/
├── app.py            # Everything — heatmap, UI, database, CSS
├── requirements.txt  # streamlit, plotly
├── README.md         # This file
├── CLAUDE.md         # AI assistant context for Claude Code
└── tracker.db        # Auto-created on first run (SQLite)
```

---

## Customising Tasks

Edit the `TASKS` list near the top of `app.py`:

```python
TASKS = [
    "Bible Study",
    "Pre-Market Prep",
    "Trading Session",
    "Study Block",
    "Focus Time",
    "Gym",
    "Lunch",
    "Coding",
    "Evening Study",
    "Church",
]
```

Add, remove, or rename tasks freely. The database stores completions by task name, so renamed tasks start fresh.

---

## Extending the App

Some ideas for next steps:

- **Google Calendar live sync** — pull today's events via the Google Calendar API and auto-populate the checklist instead of static tasks.
- **Weekly review page** — a second Streamlit page showing bar charts of tasks per day for the selected week.
- **Streak notifications** — a warning banner if today has no completions yet and it's past a certain hour.
- **Export to CSV** — download your full completion history.

---

## Dependencies

| Package    | Version  | Purpose                        |
|------------|----------|--------------------------------|
| streamlit  | ≥ 1.32   | Web UI framework               |
| plotly     | ≥ 5.20   | Interactive heatmap chart      |
| sqlite3    | built-in | Local persistence (no install) |
| json       | built-in | Task list serialisation        |
