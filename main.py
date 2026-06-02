import streamlit as st 
import plotly.graph_objects as go 
import sqlite3 
import json
from datetime import date, timedelta, datetime

# Page configuration
st.set_page_config(
    page_title = "Activity Tracker",
    page_icon = "📊",
    layout = "wide",
    initial_sidebar_state= "collapsed"
)

# CONSTANTS
TASKS = [
    "Bible Study",
    "Pre-Market Prep",
    "Trading Sessions",
    "Study Block",
    "Focus Time",
    "Gym",
    "Lunch",
    "Coding",
    "Evening Study",
    "Church",
]

GH = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]
LEVELS = ["⬜ Rest", "🟩 Light", "🟨 Active", "🟧 Grind", "🔴 Peak"]

# HISTORICAL GOOGLE CALENDAR DATA
HISTORY: dict[str, int] = {
    "2025-12-01": 6,  "2025-12-02": 8,  "2025-12-03": 5,  "2025-12-04": 5,
    "2025-12-05": 3,  "2025-12-06": 1,  "2025-12-07": 1,  "2025-12-08": 6,
    "2025-12-09": 6,  "2025-12-10": 3,  "2025-12-11": 4,  "2025-12-12": 3,
    "2025-12-13": 1,  "2025-12-14": 1,  "2025-12-15": 6,  "2025-12-16": 3,
    "2025-12-17": 2,  "2025-12-18": 2,  "2025-12-19": 2,  "2025-12-20": 4,
    "2025-12-21": 3,  "2025-12-22": 4,  "2025-12-23": 6,  "2025-12-24": 7,
    "2025-12-25": 7,  "2025-12-26": 8,  "2025-12-27": 3,  "2025-12-28": 3,
    "2025-12-29": 7,  "2025-12-30": 7,  "2025-12-31": 7,
    "2026-01-01": 8,  "2026-01-02": 7,  "2026-01-03": 4,  "2026-01-04": 3,
    "2026-01-05": 6,  "2026-01-06": 4,  "2026-01-07": 6,  "2026-01-08": 7,
    "2026-01-09": 7,  "2026-01-10": 3,  "2026-01-11": 2,  "2026-01-12": 6,
    "2026-01-13": 7,  "2026-01-14": 6,  "2026-01-15": 7,  "2026-01-16": 7,
    "2026-01-17": 4,  "2026-01-18": 3,  "2026-01-19": 5,  "2026-01-20": 7,
    "2026-01-21": 7,  "2026-01-22": 7,  "2026-01-23": 9,  "2026-01-24": 3,
    "2026-01-25": 5,  "2026-01-26": 7,  "2026-01-27": 9,  "2026-01-28": 7,
    "2026-01-29": 7,  "2026-01-30": 8,  "2026-01-31": 3,
    "2026-02-01": 7,  "2026-02-02": 5,  "2026-02-03": 6,  "2026-02-04": 7,
    "2026-02-05": 6,  "2026-02-06": 7,  "2026-02-07": 2,  "2026-02-08": 6,
    "2026-02-09": 5,  "2026-02-10": 6,  "2026-02-11": 6,  "2026-02-12": 6,
    "2026-02-13": 7,  "2026-02-14": 2,  "2026-02-15": 5,  "2026-02-16": 5,
    "2026-02-17": 7,  "2026-02-18": 6,  "2026-02-19": 6,  "2026-02-20": 7,
    "2026-02-21": 2,  "2026-02-22": 4,  "2026-02-23": 6,  "2026-02-24": 8,
    "2026-02-25": 6,  "2026-02-26": 6,  "2026-02-27": 7,  "2026-02-28": 2,
    "2026-03-01": 4,  "2026-03-02": 5,  "2026-03-03": 6,  "2026-03-04": 6,
    "2026-03-05": 6,  "2026-03-06": 7,  "2026-03-07": 2,  "2026-03-08": 4,
    "2026-03-09": 5,  "2026-03-10": 6,  "2026-03-11": 6,  "2026-03-12": 6,
    "2026-03-13": 7,  "2026-03-14": 2,  "2026-03-15": 4,  "2026-03-16": 6,
    "2026-03-17": 6,  "2026-03-18": 6,  "2026-03-19": 6,  "2026-03-20": 7,
    "2026-03-21": 2,  "2026-03-22": 3,  "2026-03-23": 5,  "2026-03-24": 6,
    "2026-03-25": 6,  "2026-03-26": 6,  "2026-03-27": 7,  "2026-03-28": 2,
    "2026-03-29": 3,  "2026-03-30": 5,  "2026-03-31": 7,
    "2026-04-01": 6,  "2026-04-02": 6,  "2026-04-03": 7,  "2026-04-04": 2,
    "2026-04-05": 3,  "2026-04-06": 5,  "2026-04-07": 6,  "2026-04-08": 6,
    "2026-04-09": 6,  "2026-04-10": 7,  "2026-04-11": 2,  "2026-04-12": 3,
    "2026-04-13": 5,  "2026-04-14": 7,  "2026-04-15": 6,  "2026-04-16": 6,
    "2026-04-17": 7,  "2026-04-18": 2,  "2026-04-19": 3,  "2026-04-20": 5,
    "2026-04-21": 6,  "2026-04-22": 8,  "2026-04-23": 6,  "2026-04-24": 7,
    "2026-04-25": 2,  "2026-04-26": 5,  "2026-04-27": 7,  "2026-04-28": 8,
    "2026-04-29": 8,  "2026-04-30": 8,
    "2026-05-01": 9,  "2026-05-02": 4,  "2026-05-03": 5,  "2026-05-04": 7,
    "2026-05-05": 8,  "2026-05-06": 8,  "2026-05-07": 8,  "2026-05-08": 9,
    "2026-05-09": 4,  "2026-05-10": 5,  "2026-05-11": 7,  "2026-05-12": 9,
    "2026-05-13": 8,  "2026-05-14": 9,  "2026-05-15": 9,  "2026-05-16": 4,
    "2026-05-17": 5,  "2026-05-18": 6,  "2026-05-19": 9,  "2026-05-20": 8,
    "2026-05-21": 8,  "2026-05-22": 9,  "2026-05-23": 4,  "2026-05-24": 5,
    "2026-05-25": 6,  "2026-05-26": 3,  "2026-05-27": 7,  "2026-05-28": 8,
    "2026-05-29": 9,  "2026-05-30": 4,  "2026-05-31": 5,
    "2026-06-01": 12, "2026-06-02": 12,
}

# DATABASE
DB_PATH = "tracker.db"

def _conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    with _conn() as c:
        c.execute(""" 
            CREATE TABLE IF NOT EXISTS completions (
                date TEXT PRIMARY KEY,
                tasks TEXT NOT NULL DEFAULT '[]'
            )
        """)

def load_day(ds: str) -> list[str]:
    with _conn() as c:
        row = c.execute(
            "INSERT OR REPLACE INTO completions(date, tasks) VALUES(?,?)",
            (ds, json.dumps(tasks)),
        )


def all_completions() -> dict[str, int]:
    with _conn() as c:
        rows = c.execute("SELECT date, tasks FROM completions").fetchall()
    return {ds: len(json.loads(t)) for ds, t in rows if json.loads(t)}

# HELPERS
def level(n: int) -> int:
    if n == 0: return 0
    if n <= 2: return 1
    if n <= 5: return 2
    if n <= 9: return 3
    return 4

def activity_map() -> dict[str, int]:
    am = dict(HISTORY)
    am.update(all_completions()) # checked tasks override calendar counts
    return am

def stats(am: dict[str, int]) -> dict:
    today = date.today()
    
    streak = 0
    d = today
    
    while am.get(d.strftime("%Y-%m-%d"), 0) > 0:
        streak += 1
        d -= timedelta(days=1)

    best_ds  = max(am, key=am.get, default="")
    best_cnt = am.get(best_ds, 0)
    best_lbl = (
        datetime.strptime(best_ds, "%Y-%m-%d").strftime("%b %d")
        if best_ds else "—"
    )

    week_start = today - timedelta(days=(today.weekday() + 1) % 7)
    week_total = sum(
        am.get((week_start + timedelta(i)).strftime("%Y-%m-%d"), 0)
        for i in range(7)
    )

    return {
        "streak":  streak,
        "total":   sum(am.values()),
        "best":    f"{best_cnt} · {best_lbl}",
        "week":    week_total,
    }


# ─── HEATMAP ──────────────────────────────────────────────────────────────────
WEEKS = 27
DAY_LABELS = {6: "Sun", 4: "Tue", 2: "Thu", 0: "Sat"}   # y-index → label


def build_heatmap(am: dict[str, int], selected: date) -> go.Figure:
    today = date.today()

    # align grid start to Sunday
    start = today - timedelta(weeks=WEEKS)
    start -= timedelta(days=(start.weekday() + 1) % 7)

    xs, ys, fills, borders, hovers, dates = [], [], [], [], [], []
    month_marks: dict[int, str] = {}

    for w in range(WEEKS):
        for d in range(7):                     # d=0 → Sunday
            cur = start + timedelta(w * 7 + d)
            ds  = cur.strftime("%Y-%m-%d")
            cnt = am.get(ds, 0) if cur <= today else 0
            lv  = level(cnt)     if cur <= today else 0
            fut = cur > today
            sel = cur == selected

            xs.append(w + 0.5)
            ys.append(6 - d + 0.5)            # flip: Sun at top (y=6.5→0.5)
            fills.append("rgba(0,0,0,0)" if fut else GH[lv])
            borders.append("#39d353" if sel else "rgba(0,0,0,0)")
            hovers.append(
                f"<b>{cur.strftime('%a %b %d, %Y')}</b><br>{cnt} tasks" if not fut else ""
            )
            dates.append(ds)

            if cur.day <= 7 and w not in month_marks:
                month_marks[w] = cur.strftime("%b")

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=xs, y=ys,
        mode="markers",
        marker=dict(
            symbol="square",
            size=16,
            color=fills,
            line=dict(width=2, color=borders),
        ),
        text=hovers,
        hoverinfo="text",
        hoverlabel=dict(bgcolor="#1c2128", bordercolor="#30363d", font_color="#e6edf3"),
        customdata=dates,
        showlegend=False,
    ))

    annotations = []

    # Month labels
    for wi, mname in month_marks.items():
        annotations.append(dict(
            x=wi + 0.5, y=7.6,
            text=mname, showarrow=False,
            font=dict(size=11, color="#7d8590"),
            xanchor="left",
        ))

    # Day labels
    for yi, lbl in DAY_LABELS.items():
        annotations.append(dict(
            x=-0.8, y=yi + 0.5,
            text=lbl, showarrow=False,
            font=dict(size=10, color="#7d8590"),
            xanchor="right",
        ))

    # Legend squares
    legend_x = WEEKS - 5.5
    legend_y  = -0.9
    annotations.append(dict(x=legend_x - 0.8, y=legend_y, text="Less", showarrow=False,
                             font=dict(size=10, color="#7d8590"), xanchor="right"))
    annotations.append(dict(x=legend_x + 5.2, y=legend_y, text="More", showarrow=False,
                             font=dict(size=10, color="#7d8590"), xanchor="left"))
    for i, col in enumerate(GH):
        fig.add_trace(go.Scatter(
            x=[legend_x + i], y=[legend_y],
            mode="markers",
            marker=dict(symbol="square", size=13, color=col),
            hoverinfo="skip",
            showlegend=False,
        ))

    fig.update_layout(
        plot_bgcolor="#0d1117",
        paper_bgcolor="#0d1117",
        height=200,
        margin=dict(l=40, r=10, t=28, b=30),
        xaxis=dict(range=[-1.5, WEEKS + 0.5], showgrid=False, zeroline=False,
                   showticklabels=False, fixedrange=True),
        yaxis=dict(range=[-1.5, 8.1], showgrid=False, zeroline=False,
                   showticklabels=False, fixedrange=True),
        annotations=annotations,
        dragmode=False,
    )
    return fig


# ─── CSS ──────────────────────────────────────────────────────────────────────
STYLE = """
<style>
/* dark background */
[data-testid="stAppViewContainer"] { background: #0d1117; }
[data-testid="stHeader"] { background: #0d1117; }
section[data-testid="stSidebar"] { background: #161b22; }

/* metric cards */
[data-testid="stMetric"] {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 14px 18px;
}
[data-testid="stMetricLabel"]  { color: #7d8590 !important; font-size: 12px !important; }
[data-testid="stMetricValue"]  { color: #f0f6fc !important; font-size: 22px !important; }
[data-testid="stMetricDelta"]  { display: none; }

/* checkboxes */
[data-testid="stCheckbox"] label { font-size: 14px; color: #e6edf3; }
[data-testid="stCheckbox"] { padding: 4px 0; }

/* buttons */
[data-testid="baseButton-primary"] {
    background: #238636 !important;
    border-color: #2ea043 !important;
    color: white !important;
    border-radius: 6px !important;
}
[data-testid="baseButton-primary"]:hover {
    background: #2ea043 !important;
}

/* progress bar */
[data-testid="stProgress"] > div > div {
    background: #39d353 !important;
}

/* divider */
hr { border-color: #21262d !important; }

/* headers */
h1, h2, h3 { color: #f0f6fc !important; }
p, label   { color: #e6edf3; }

/* caption / subtext */
.caption { color: #7d8590; font-size: 12px; }

/* intensity badge */
.badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 12px;
    font-size: 13px;
    font-weight: 600;
}
.badge-0 { background:#21262d; color:#7d8590; }
.badge-1 { background:#0e4429; color:#56d364; }
.badge-2 { background:#1a3a00; color:#ffa657; }
.badge-3 { background:#3d1a00; color:#ffa657; }
.badge-4 { background:#3d0000; color:#ff7b72; }

/* task section card */
.task-card {
    background: #161b22;
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 20px 24px;
    margin-top: 6px;
}
</style>
"""


# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    init_db()
    st.markdown(STYLE, unsafe_allow_html=True)

    # ── Header ────────────────────────────────────────────────────────────────
    st.markdown("## 📊 Activity Tracker")
    st.markdown(
        '<p class="caption">Synced from Google Calendar · pkiprop@caldwell.edu '
        '· Check off tasks as you complete them</p>',
        unsafe_allow_html=True,
    )

    am    = activity_map()
    s     = stats(am)
    today = date.today()

    # ── Stats row ─────────────────────────────────────────────────────────────
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔥 Streak",       f"{s['streak']} days")
    c2.metric("📅 Total Events", f"{s['total']:,}")
    c3.metric("⭐ Best Day",     s["best"])
    c4.metric("📊 This Week",    s["week"])

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Heatmap ───────────────────────────────────────────────────────────────
    if "selected_date" not in st.session_state:
        st.session_state.selected_date = today

    sel: date = st.session_state.selected_date

    fig = build_heatmap(am, sel)

    event = st.plotly_chart(
        fig,
        use_container_width=True,
        key="heatmap",
        on_select="rerun",
        selection_mode="points",
    )

    # Handle click → navigate to that day
    if event and event.selection and event.selection.get("points"):
        pt = event.selection["points"][0]
        idx = pt.get("point_index")
        if idx is not None:
            trace = fig.data[0]
            ds = trace.customdata[idx]
            try:
                clicked_date = datetime.strptime(ds, "%Y-%m-%d").date()
                if clicked_date <= today:
                    st.session_state.selected_date = clicked_date
                    st.rerun()
            except Exception:
                pass

    st.divider()

    # ── Task Checker ──────────────────────────────────────────────────────────
    left, right = st.columns([1, 2])

    with left:
        picked = st.date_input(
            "Select a day",
            value=st.session_state.selected_date,
            max_value=today + timedelta(days=30),
            key="date_picker",
        )
        if isinstance(picked, date):
            st.session_state.selected_date = picked
            sel = picked

    ds_str     = sel.strftime("%Y-%m-%d")
    day_label  = sel.strftime("%A, %b %d %Y")
    completed  = load_day(ds_str)
    cal_count  = HISTORY.get(ds_str, 0)
    is_today   = sel == today

    with right:
        badge_cls = f"badge-{level(len(completed))}"
        badge_txt = LEVELS[level(len(completed))]
        st.markdown(
            f"<h3 style='margin:0'>{day_label} &nbsp;"
            f'<span class="badge {badge_cls}">{badge_txt}</span></h3>',
            unsafe_allow_html=True,
        )
        if cal_count and not completed:
            st.markdown(
                f'<p class="caption">📅 {cal_count} calendar events on this day</p>',
                unsafe_allow_html=True,
            )

    st.markdown('<div class="task-card">', unsafe_allow_html=True)

    # Progress bar
    score = len(completed)
    if score > 0:
        st.progress(score / len(TASKS), text=f"{score}/{len(TASKS)} tasks done")
    else:
        st.progress(0.0, text=f"0/{len(TASKS)} tasks done")

    st.markdown("<br>", unsafe_allow_html=True)

    # Checkboxes in 2 columns
    with st.form(key=f"tasks_{ds_str}", clear_on_submit=False):
        col_a, col_b = st.columns(2)
        checked: list[str] = []

        for i, task in enumerate(TASKS):
            col = col_a if i % 2 == 0 else col_b
            ticked = col.checkbox(
                task,
                value=(task in completed),
                key=f"cb_{ds_str}_{task}",
            )
            if ticked:
                checked.append(task)

        st.markdown("<br>", unsafe_allow_html=True)
        submitted = st.form_submit_button(
            "✅  Save progress",
            type="primary",
            use_container_width=False,
        )

    st.markdown("</div>", unsafe_allow_html=True)

    if submitted:
        save_day(ds_str, checked)
        new_lv   = level(len(checked))
        new_txt  = LEVELS[new_lv]
        st.success(
            f"Saved! Score **{len(checked)}/10** — {new_txt}  "
            f"{'🎉 Full day unlocked!' if len(checked) == len(TASKS) else ''}"
        )
        st.rerun()

    # ── Tip ───────────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        '<p class="caption">💡 Click any square on the heatmap to jump to that day · '
        "Historical squares show Google Calendar event counts · "
        "Checked tasks override the count going forward</p>",
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
