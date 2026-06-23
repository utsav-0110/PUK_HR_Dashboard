import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64
import os

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Purple United Sales Limited — HR Analytics",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Logo ───────────────────────────────────────────────────────────────────────
def get_logo_b64():
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo.png")
    try:
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

LOGO_B64 = get_logo_b64()
LOGO_HTML = f'<img src="data:image/png;base64,{LOGO_B64}" style="width:42px;height:42px;object-fit:contain;border-radius:10px;">' if LOGO_B64 else '<span style="font-size:28px">🏢</span>'

# ── PREMIUM CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ─── RESET & BASE ─── */
*, *::before, *::after { box-sizing: border-box; }
html, body, [class*="css"], .main, .stApp {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    background-color: #F0F4F8 !important;
    color: #1A202C !important;
    scrollbar-width: thin;
    scrollbar-color: #7B2FF7 #E2E8F0;
}
.main .block-container {
    padding: 0 1.2rem 2rem 1.2rem !important;
    padding-top: 0 !important;
    max-width: 1600px !important;
    background: #F0F4F8 !important;
}
/* Remove Streamlit top padding/header white space */
header[data-testid="stHeader"] {
    background: #F0F4F8 !important;
    height: 0 !important;
    min-height: 0 !important;
}
#MainMenu, footer, header { visibility: hidden; height: 0; }
.stApp > header { display: none; }
div[data-testid="stDecoration"] { display: none; }
/* Fix cursor on charts - no crosshair/plus */
.js-plotly-plot .plotly .cursor-crosshair,
.js-plotly-plot .plotly .cursor-default,
.js-plotly-plot,
.js-plotly-plot * { cursor: default !important; }
.plotly-graph-div { cursor: default !important; }
.plotly .main-svg { cursor: default !important; }

/* ─── SCROLLBAR ─── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #E2E8F0; border-radius: 10px; }
::-webkit-scrollbar-thumb { background: linear-gradient(180deg, #7B2FF7, #A855F7); border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background: #6D28D9; }

/* ─── SIDEBAR ─── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #F8F5FF 0%, #EDE9FE 40%, #F8F5FF 100%) !important;
    border-right: 1px solid rgba(123,47,247,0.2);
    width: 240px !important;
}
[data-testid="stSidebar"] * { color: #4C1D95 !important; }
[data-testid="stSidebarNav"] { display: none; }
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #6D28D9 !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 500 !important;
    font-size: 13px !important;
    text-align: left !important;
    width: 100% !important;
    padding: 10px 14px !important;
    transition: all 0.25s ease !important;
    box-shadow: none !important;
    margin-bottom: 2px !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(123,47,247,0.12) !important;
    color: #5B21B6 !important;
    transform: translateX(5px) !important;
    box-shadow: 0 0 12px rgba(123,47,247,0.15) !important;
    border-left: 3px solid #7B2FF7 !important;
}

/* ─── SELECT / DROPDOWN ─── */
[data-baseweb="select"] > div {
    background: #fff !important;
    border: 1px solid rgba(123,47,247,0.35) !important;
    border-radius: 10px !important;
    color: #1A202C !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
[data-baseweb="select"] > div:hover {
    border-color: #7B2FF7 !important;
    box-shadow: 0 0 0 2px rgba(123,47,247,0.15) !important;
}
[data-baseweb="popover"] div {
    background: #fff !important;
    border: 1px solid rgba(123,47,247,0.3) !important;
}
[data-baseweb="menu"] { background: #fff !important; }
[data-baseweb="option"] { background: #fff !important; color: #1A202C !important; }
[data-baseweb="option"]:hover { background: rgba(123,47,247,0.08) !important; }
[aria-selected="true"] { background: rgba(123,47,247,0.12) !important; }
.stSelectbox label, .stMultiSelect label {
    color: #7B2FF7 !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.8px !important;
}

/* ─── MULTISELECT TAGS ─── */
[data-baseweb="tag"] {
    background: rgba(123,47,247,0.12) !important;
    border: 1px solid rgba(123,47,247,0.35) !important;
    border-radius: 6px !important;
    color: #5B21B6 !important;
}

/* ─── INPUTS ─── */
input, textarea {
    background: #fff !important;
    color: #1A202C !important;
    border: 1px solid rgba(123,47,247,0.3) !important;
    border-radius: 10px !important;
    caret-color: #7B2FF7 !important;
}
input:focus, textarea:focus {
    border-color: #7B2FF7 !important;
    box-shadow: 0 0 0 2px rgba(123,47,247,0.15) !important;
    outline: none !important;
}

/* ─── BUTTONS ─── */
.stButton > button {
    border-radius: 10px !important;
    background: rgba(123,47,247,0.15) !important;
    color: #C4B5FD !important;
    border: 1px solid rgba(123,47,247,0.35) !important;
    transition: all 0.2s ease !important;
    font-weight: 600 !important;
}
.stButton > button:hover {
    background: #7B2FF7 !important;
    color: #fff !important;
    border-color: #A855F7 !important;
    box-shadow: 0 0 18px rgba(123,47,247,0.4) !important;
    transform: translateY(-1px) !important;
}
.stDownloadButton > button {
    background: linear-gradient(135deg,#7B2FF7,#A855F7) !important;
    color: white !important; border: none !important;
    border-radius: 10px !important;
    box-shadow: 0 4px 15px rgba(123,47,247,0.4) !important;
}

/* ─── TABS ─── */
.stTabs [data-baseweb="tab-list"] {
    background: #E9E6F8;
    padding: 4px; border-radius: 12px; gap: 3px;
    border: 1px solid rgba(123,47,247,0.2);
}
.stTabs [data-baseweb="tab"] { color: #6D28D9 !important; border-radius: 9px !important; }
.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg,#7B2FF7,#A855F7) !important;
    color: white !important; border-radius: 9px !important;
    box-shadow: 0 3px 10px rgba(123,47,247,0.3) !important;
}

/* ─── DATAFRAME ─── */
div[data-testid="stDataFrame"] {
    border-radius: 12px; overflow: hidden;
    border: 1px solid rgba(123,47,247,0.2);
}

/* ─── EXPANDER ─── */
div[data-testid="stExpander"] {
    background: #fff !important;
    border: 1px solid rgba(123,47,247,0.2) !important;
    border-radius: 12px !important;
}
.streamlit-expanderHeader { color: #7B2FF7 !important; font-weight: 600 !important; }

/* ─── FILE UPLOADER ─── */
[data-testid="stFileUploader"] section,
[data-testid="stFileUploaderDropzone"] {
    background: #fff !important;
    border: 1.5px dashed rgba(123,47,247,0.4) !important;
    border-radius: 12px !important;
}
[data-testid="stFileUploader"] section:hover,
[data-testid="stFileUploaderDropzone"]:hover {
    border-color: rgba(123,47,247,0.7) !important;
    background: rgba(123,47,247,0.04) !important;
}
[data-testid="stFileUploader"] section *,
[data-testid="stFileUploaderDropzone"] * {
    color: #1A202C !important;
}
[data-testid="stFileUploader"] section small,
[data-testid="stFileUploaderDropzone"] small {
    color: #718096 !important;
}
[data-testid="stFileUploader"] button,
[data-testid="stFileUploaderDropzone"] button {
    background: rgba(123,47,247,0.08) !important;
    color: #6D28D9 !important;
    border: 1px solid rgba(123,47,247,0.4) !important;
}
[data-testid="stFileUploader"] button:hover,
[data-testid="stFileUploaderDropzone"] button:hover {
    background: rgba(123,47,247,0.15) !important;
    color: #5B21B6 !important;
}
[data-testid="stFileUploaderFileName"] { color: #1A202C !important; }

/* ─── ALERTS ─── */
.stSuccess { background: rgba(34,197,94,0.1) !important; border-color: rgba(34,197,94,0.3) !important; }
.stInfo    { background: rgba(123,47,247,0.1) !important; border-color: rgba(123,47,247,0.3) !important; }
.stWarning { background: rgba(245,158,11,0.1) !important; border-color: rgba(245,158,11,0.3) !important; }

/* ─── METRIC ─── */
.stMetric {
    background: #fff !important; border-radius: 12px !important;
    padding: 14px 18px !important;
    border: 1px solid rgba(123,47,247,0.15) !important;
}
.stMetric label { color: #718096 !important; font-size: 11px !important; }
.stMetric [data-testid="stMetricValue"] { color: #1A202C !important; font-weight: 800 !important; }

/* ─── TYPOGRAPHY ─── */
p, li, span, div { color: #2D3748; }
h1,h2,h3 { color: #1A202C !important; }
hr { border-color: rgba(123,47,247,0.15) !important; }

/* ─── KPI CARDS ─── */
.kpi-grid { display: grid; gap: 14px; margin-bottom: 20px; }
.kpi-card {
    background: #fff;
    border-radius: 14px;
    padding: 18px 20px;
    border: 1px solid #E2E8F0;
    border-left: 4px solid var(--accent, #0D9488);
    position: relative; overflow: hidden;
    transition: transform 0.25s cubic-bezier(.34,1.56,.64,1), box-shadow 0.25s ease;
    cursor: default;
    animation: fadeUp 0.5s ease both;
    min-height: 120px;
    display: flex; flex-direction: column; justify-content: center;
    box-sizing: border-box;
}
.kpi-card::before {
    content: '';
    position: absolute; top: 0; left: 0; right: 0; bottom: 0;
    background: linear-gradient(135deg, rgba(13,148,136,0.04), transparent);
    opacity: 0; transition: opacity 0.3s;
}
.kpi-card:hover {
    transform: translateY(-4px) scale(1.01);
    box-shadow: 0 12px 32px rgba(13,148,136,0.15), 0 0 0 1px rgba(13,148,136,0.2);
}
.kpi-card:hover::before { opacity: 1; }
.kpi-icon { font-size: 18px; margin-bottom: 6px; display: block; }
.kpi-val {
    font-size: 26px; font-weight: 900; color: #1A202C;
    line-height: 1; white-space: nowrap; overflow: hidden;
    text-overflow: ellipsis; letter-spacing: -0.5px;
}
.kpi-label {
    font-size: 10px; color: #718096; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px; margin-top: 6px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.kpi-delta {
    font-size: 11px; margin-top: 6px; font-weight: 600;
    display: flex; align-items: center; gap: 4px;
}
.kpi-glow {
    position: absolute; bottom: -20px; right: -20px;
    width: 80px; height: 80px; border-radius: 50%;
    background: var(--accent, #0D9488);
    opacity: 0.06; filter: blur(20px);
}

/* ─── CHART CARD ─── */
.chart-card {
    background: #fff;
    border-radius: 14px;
    padding: 18px 18px 8px;
    border: 1px solid #E2E8F0;
    margin-bottom: 16px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    transition: box-shadow 0.25s;
    animation: fadeUp 0.5s ease both;
}
.chart-card:hover {
    box-shadow: 0 8px 24px rgba(13,148,136,0.1);
}

/* ─── FILTER PANEL ─── */
.filter-panel {
    background: #fff;
    border: 1px solid rgba(123,47,247,0.2);
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 18px;
    animation: fadeUp 0.3s ease both;
}
.filter-header {
    display: flex; align-items: center; gap: 10px;
    margin-bottom: 14px;
    padding-bottom: 10px;
    border-bottom: 1px solid rgba(123,47,247,0.12);
}
.filter-dot {
    width: 8px; height: 8px; border-radius: 50%;
    background: linear-gradient(135deg, #7B2FF7, #A855F7);
}
.filter-title-text {
    font-size: 12px; font-weight: 700; color: #7B2FF7;
    text-transform: uppercase; letter-spacing: 1.2px;
}

/* ─── SECTION HEADER ─── */
.sec-hdr {
    display: flex; align-items: center; gap: 10px;
    border-bottom: 1px solid rgba(123,47,247,0.15);
    padding-bottom: 10px; margin: 20px 0 14px;
}
.sec-icon {
    width: 30px; height: 30px;
    background: linear-gradient(135deg,#7B2FF7,#A855F7);
    border-radius: 8px;
    display: flex; align-items: center; justify-content: center;
    font-size: 14px;
    box-shadow: 0 3px 10px rgba(123,47,247,0.25);
}
.sec-title { font-size: 14px; font-weight: 700; color: #1A202C; }

/* ─── SIDEBAR LOGO ─── */
.sb-logo {
    display: flex; align-items: center; gap: 12px;
    padding: 18px 14px 20px;
    border-bottom: 1px solid rgba(123,47,247,0.2);
    margin-bottom: 8px;
}
.sb-logo-text { font-size: 13px; font-weight: 800; color: #4C1D95 !important; line-height: 1.2; }
.sb-logo-sub  { font-size: 10px; color: #7B2FF7 !important; letter-spacing: 0.5px; }
.sb-section {
    font-size: 9px; font-weight: 800; letter-spacing: 1.8px; color: #7B2FF7 !important;
    text-transform: uppercase; padding: 14px 14px 5px;
}

/* ─── HEADER ─── */
.dash-header {
    background: linear-gradient(135deg, #F8F5FF 0%, #EDE9FE 40%, #DDD6FE 70%, #F8F5FF 100%);
    border-radius: 16px;
    padding: 20px 28px;
    display: flex; align-items: center; justify-content: space-between;
    margin-bottom: 18px;
    border: 1px solid rgba(123,47,247,0.25);
    box-shadow: 0 4px 20px rgba(123,47,247,0.1);
    position: relative; overflow: hidden;
}
.dash-header::before {
    content: '';
    position: absolute; top: -50%; right: -10%;
    width: 300px; height: 300px; border-radius: 50%;
    background: radial-gradient(circle, rgba(123,47,247,0.08), transparent 70%);
    pointer-events: none;
}
.header-title { color: #4C1D95; font-size: 18px; font-weight: 800; line-height: 1.2; }
.header-sub   { color: #7B2FF7; font-size: 11px; margin-top: 3px; letter-spacing: 0.3px; }
.header-badge {
    background: rgba(123,47,247,0.12); border: 1px solid rgba(123,47,247,0.3);
    border-radius: 20px; padding: 3px 10px;
    font-size: 10px; color: #6D28D9; font-weight: 700;
    text-transform: uppercase; letter-spacing: 1px;
    display: inline-block; margin-top: 6px;
}
.header-time  { color: #4C1D95; font-size: 22px; font-weight: 800; text-align: right; font-variant-numeric: tabular-nums; }
.header-day   { color: #7B2FF7; font-size: 11px; text-align: right; }
.header-date  { color: #718096; font-size: 11px; text-align: right; }
.header-avatar {
    width: 38px; height: 38px;
    background: linear-gradient(135deg,#7B2FF7,#C084FC);
    border-radius: 50%; display: flex; align-items: center; justify-content: center;
    font-size: 16px; box-shadow: 0 0 15px rgba(123,47,247,0.3);
}

/* ─── PAGE TITLE ─── */
.page-title { font-size: 22px; font-weight: 900; color: #1A202C !important; margin-bottom: 0px; margin-top: -18px; }
.page-sub   { font-size: 12px; color: #718096; margin-bottom: 8px; letter-spacing: 0.3px; }

/* ─── PROGRESS BAR ─── */
.prog-wrap { background: rgba(123,47,247,0.1); border-radius: 999px; height: 6px; overflow: hidden; margin: 4px 0 9px; }
.prog-fill  { height: 100%; border-radius: 999px; background: linear-gradient(90deg,#7B2FF7,#A855F7); transition: width 0.8s ease; }

/* ─── UPLOAD AREA ─── */
.upload-box {
    border: 2px dashed rgba(123,47,247,0.35); border-radius: 10px;
    padding: 6px 18px; text-align: center;
    background: rgba(123,47,247,0.03); margin-bottom: 6px;
    transition: border-color 0.2s, background 0.2s;
}
.upload-box:hover { border-color: rgba(123,47,247,0.6); background: rgba(123,47,247,0.06); }

/* ─── FILTER BADGE ─── */
.filter-badge {
    background: linear-gradient(90deg, rgba(123,47,247,0.08), rgba(168,85,247,0.05));
    border: 1px solid rgba(123,47,247,0.2);
    border-radius: 10px; padding: 8px 16px;
    margin-bottom: 12px; font-size: 12px; color: #6D28D9; font-weight: 600;
}

/* ─── ANIMATIONS ─── */
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(16px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes countUp {
    from { opacity: 0; }
    to   { opacity: 1; }
}
@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(123,47,247,0.3); }
    50%       { box-shadow: 0 0 0 6px rgba(123,47,247,0); }
}

/* ─── SHIMMER LOADING ─── */
.shimmer {
    background: linear-gradient(90deg, #E2E8F0 0%, #F0F4F8 50%, #E2E8F0 100%);
    background-size: 200% 100%;
    animation: shimmer 1.5s infinite;
    border-radius: 10px; height: 100px;
}
@keyframes shimmer {
    0%   { background-position: -200% 0; }
    100% { background-position:  200% 0; }
}
</style>

<script>
// Live clock injection into Streamlit
function updateClock() {
    const el = document.getElementById('live-clock');
    if (el) {
        const now = new Date();
        const h = String(now.getHours()).padStart(2,'0');
        const m = String(now.getMinutes()).padStart(2,'0');
        const s = String(now.getSeconds()).padStart(2,'0');
        el.textContent = h + ':' + m + ':' + s;
    }
    setTimeout(updateClock, 1000);
}
updateClock();
</script>
""", unsafe_allow_html=True)


# ── Constants ──────────────────────────────────────────────────────────────────
PAYROLL_COLS    = ["New Joining", "Resign", "F&F"]
COMPLIANCE_COLS = ["PF", "ESIC", "PT", "LWF"]
LABOUR_COLS     = ["S&E", "Trade Licence", "Form A under POG Act"]
DOC_COLS        = ["Appointment Letter", "KYC (PAN+Aadhar+Bank)", "PF Form", "ESIC Form", "BGV"]
RECRUIT_COLS    = ["Location", "Profile Position", "Recruiter Name", "Profile Source"]
STATUS_COL      = "Employment Status"

# Frosted Slate + Purple palette
P = dict(
    primary   = "#0D9488",
    secondary = "#7B2FF7",
    accent    = "#A855F7",
    bg        = "#F0F4F8",
    card      = "#FFFFFF",
    hover     = "#F8F5FF",
    text      = "#1A202C",
    muted     = "#718096",
    green     = "#059669",
    red       = "#DC2626",
    amber     = "#D97706",
    blue      = "#2563EB",
    teal      = "#0D9488",
)

PALETTE = ["#0D9488","#7B2FF7","#A855F7","#2563EB","#059669","#D97706","#DC2626","#0891B2","#EC4899","#F97316"]
CHART_BG   = "#FFFFFF"
CHART_GRID = "rgba(0,0,0,0.04)"
CHART_TEXT = "#718096"


# ── Chart Layout ───────────────────────────────────────────────────────────────
def chart_layout(fig, height=300, title=""):
    fig.update_layout(
        paper_bgcolor=CHART_BG,
        plot_bgcolor=CHART_BG,
        margin=dict(l=12, r=12, t=44, b=12),
        height=height,
        font=dict(family="Inter, sans-serif", color=CHART_TEXT, size=11),
        title=dict(text=title, font=dict(color="#1A202C", size=13, family="Inter"), x=0.01, xanchor="left"),
        legend=dict(
            bgcolor="rgba(255,255,255,0.95)",
            bordercolor="rgba(123,47,247,0.2)",
            borderwidth=1,
            font=dict(color="#2D3748"),
        ),
        xaxis=dict(
            gridcolor=CHART_GRID, linecolor="rgba(0,0,0,0.06)",
            tickfont=dict(color=CHART_TEXT), title_font=dict(color=CHART_TEXT),
            zeroline=False,
        ),
        yaxis=dict(
            gridcolor=CHART_GRID, linecolor="rgba(0,0,0,0.06)",
            tickfont=dict(color=CHART_TEXT), title_font=dict(color=CHART_TEXT),
            zeroline=False,
        ),
        hoverlabel=dict(
            bgcolor="#F8F5FF",
            bordercolor=P["secondary"],
            font=dict(color="#1A202C", family="Inter", size=12),
        ),
    )
    return fig


# ── Helpers ────────────────────────────────────────────────────────────────────
def compliance_pct(series):
    s     = series.astype(str).str.strip()
    done  = (s.str.upper() == "DONE").sum()
    # count both blanks AND explicit "Not Done" as pending
    blank = (s == "").sum()
    notdone = (s.str.upper() == "NOT DONE").sum()
    total = done + blank + notdone
    return round(done / total * 100, 1) if total > 0 else 0.0

def compliance_counts(series):
    s = series.astype(str).str.strip()
    done    = (s.str.upper() == "DONE").sum()
    blank   = (s == "").sum()
    notdone = (s.str.upper() == "NOT DONE").sum()
    na      = (s.str.upper() == "N/A").sum()
    return int(done), int(blank + notdone), int(na)

def progress_bar(pct, color=None):
    c = color or P["primary"]
    return f"<div class='prog-wrap'><div class='prog-fill' style='width:{pct}%;background:{c};'></div></div>"

def kpi(icon, value, label, accent=None, delta=""):
    ac = accent or P["primary"]
    green = P["green"]
    delta_html = f"<div class='kpi-delta' style='color:{green}'>{delta}</div>" if delta else ""
    return f"""
    <div class='kpi-card' style='--accent:{ac}'>
        <div class='kpi-glow' style='background:{ac}'></div>
        <span class='kpi-icon'>{icon}</span>
        <div class='kpi-val'>{value}</div>
        <div class='kpi-label'>{label}</div>
        {delta_html}
    </div>"""

def sec(icon, title):
    st.markdown(f"""
    <div class='sec-hdr'>
        <div class='sec-icon'>{icon}</div>
        <span class='sec-title'>{title}</span>
    </div>""", unsafe_allow_html=True)

def to_excel(df):
    import io
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as w:
        df.to_excel(w, index=False)
    return buf.getvalue()


# ── Data Loading ───────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_data(file_bytes, file_name):
    if file_name.endswith(".csv"):
        df = pd.read_csv(file_bytes)
    else:
        df = pd.read_excel(file_bytes)

    for col in ["DOJ", "Resignation Date", "Exit Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    for col in df.columns:
        if df[col].dtype == object:
            df[col] = df[col].fillna("").astype(str).str.strip()

    # Normalize labour compliance column names
    col_remap = {}
    for alt in ["Trade License", "Trade", "Trade Lic", "Trade licence", "trade", "trade license"]:
        if alt in df.columns and "Trade Licence" not in df.columns:
            col_remap[alt] = "Trade Licence"; break
    for alt in ["Form A Under POG Act", "Form A under Pog Act", "Form A under POG act",
                "Form A Under Pog Act", "Form A under pog act", "Form A", "POG Act"]:
        if alt in df.columns and "Form A under POG Act" not in df.columns:
            col_remap[alt] = "Form A under POG Act"; break
    # Also try case-insensitive match for Form A under POG Act
    if "Form A under POG Act" not in df.columns:
        for c in df.columns:
            if c.strip().lower() == "form a under pog act":
                col_remap[c] = "Form A under POG Act"; break
    if col_remap:
        df = df.rename(columns=col_remap)

    if "ESIC Form" in df.columns:
        idx = list(df.columns).index("ESIC Form")
        extra = [c for c in df.columns[idx+1:]
                 if c not in RECRUIT_COLS + ["Remarks", "BGV", "Location",
                    "Profile Position", "Recruiter Name", "Profile Source"]]
        global DOC_COLS
        DOC_COLS = ["Appointment Letter","KYC (PAN+Aadhar+Bank)","PF Form","ESIC Form","BGV"] + extra

    return df

def get_df():
    if st.session_state.get("uploaded_file") is not None:
        uf = st.session_state.uploaded_file
        return load_data(uf, uf.name)
    try:
        return load_data(open("sample_hr_data.xlsx","rb"), "sample_hr_data.xlsx")
    except:
        try:
            return load_data(open("sample_hr_data.csv","rb"), "sample_hr_data.csv")
        except:
            return pd.DataFrame()


# ── Session State ──────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"
if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None

# Persistent filter storage (survives nav switches)
if "_filter_store" not in st.session_state:
    st.session_state._filter_store = {}

# Restore saved filter values into session state before widgets render
for _k, _v in st.session_state._filter_store.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v

def persistent_selectbox(label, options, key):
    """Selectbox that remembers its value across page navigation."""
    store = st.session_state._filter_store
    saved = store.get(key, "All")
    idx = 0
    if saved in options:
        idx = options.index(saved)
    val = st.selectbox(label, options, index=idx, key=key)
    store[key] = val
    return val


# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div class='sb-logo'>
        <div>{LOGO_HTML}</div>
        <div>
            <div class='sb-logo-text'>Purple United Sales Limited</div>
            <div class='sb-logo-sub'>Analytics Overview</div>
        </div>
    </div>""", unsafe_allow_html=True)

    with st.expander("📂 Upload Excel / CSV", expanded=False):
        uf = st.file_uploader("HR Master File", type=["xlsx","xls","csv"], label_visibility="collapsed")
        if uf:
            st.session_state.uploaded_file = uf
            st.success(f"✅ {uf.name}")

    st.markdown('<div class="sb-section">Navigation</div>', unsafe_allow_html=True)

    NAV = [
        ("🏠", "Dashboard"),
        ("📢", "Recruitment"),
        ("📑", "HRIS"),
        ("💰", "Payroll"),
        ("⚖️", "Payroll Compliance"),
        ("🏭", "Labour Compliance"),
        ("📊", "Reports"),
        ("⚙️", "Settings"),
    ]
    for icon, label in NAV:
        active = "🟣 " if st.session_state.page == label else ""
        if st.button(f"{active}{icon}  {label}", key=f"nav_{label}", use_container_width=True):
            # Preserve all filter keys before switching page
            for k, v in list(st.session_state.items()):
                if k.startswith(("rec_","dash_","pay_","hris_","comp_","pc_","doc_","lab_")):
                    st.session_state._filter_store[k] = v
            st.session_state.page = label
            st.rerun()

    st.markdown("---")


# ── LOAD RAW DATA ──────────────────────────────────────────────────────────────
raw_df = get_df()


# ── GLOBAL FILTERS (only 4) ────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sb-section">Global Filters</div>', unsafe_allow_html=True)

    # Year filter
    if "DOJ" in raw_df.columns and raw_df["DOJ"].notna().any():
        year_opts_g = ["All"] + sorted(raw_df["DOJ"].dropna().dt.year.astype(int).unique().tolist(), reverse=True)
    else:
        year_opts_g = ["All"]
    f_year_g = st.selectbox("📅 Year", year_opts_g, key="g_year")

    # Month filter
    month_names = ["All","January","February","March","April","May","June",
                   "July","August","September","October","November","December"]
    f_month_g = st.selectbox("🗓️ Month", month_names, key="g_month")

    # Recruiter filter
    if "Recruiter Name" in raw_df.columns:
        rec_opts = ["All"] + sorted(r for r in raw_df["Recruiter Name"].unique() if r)
    else:
        rec_opts = ["All"]
    f_rec_g = st.selectbox("🧑‍💼 Recruiter Name", rec_opts, key="g_recruiter")

    # Location filter
    if "Location" in raw_df.columns:
        loc_opts = ["All"] + sorted(l for l in raw_df["Location"].unique() if l)
    else:
        loc_opts = ["All"]
    f_loc_g = st.selectbox("📍 Location", loc_opts, key="g_location")

    if st.button("🔄 Reset All Filters", use_container_width=True):
        for k in ["g_year","g_month","g_recruiter","g_location"]:
            st.session_state.pop(k, None)
        st.rerun()

# ── APPLY GLOBAL FILTERS ───────────────────────────────────────────────────────
def apply_global_filters(data):
    """Apply the sidebar's existing Year / Month / Recruiter / Location filters
    to any dataframe. Kept identical to the original inline logic below so the
    already-working global filters behave exactly as before."""
    out = data.copy()

    if f_year_g != "All" and "DOJ" in out.columns:
        out = out[out["DOJ"].dt.year == int(f_year_g)]

    if f_month_g != "All" and "DOJ" in out.columns:
        month_num = month_names.index(f_month_g)
        out = out[out["DOJ"].dt.month == month_num]

    if f_rec_g != "All" and "Recruiter Name" in out.columns:
        out = out[out["Recruiter Name"] == f_rec_g]

    if f_loc_g != "All" and "Location" in out.columns:
        out = out[out["Location"] == f_loc_g]

    return out

df = apply_global_filters(raw_df)

# Keep an untouched reference to the master (sidebar-uploaded / sample) data so
# each page can fall back to exactly today's behaviour when no section-specific
# file has been uploaded for it.
BASE_RAW_DF = raw_df
BASE_DF     = df


# ── SECTION-SPECIFIC EXCEL UPLOAD (per nav page) ───────────────────────────────
def section_file_uploader(section_key, section_label, fallback_df, apply_filters=True):
    """Renders a small 'Upload Excel for <Section>' box at the top of a page.
    - If the user uploads a file here, that file's data is used for this page only
      (existing global sidebar filters still apply on top of it, unless apply_filters=False).
    - If nothing is uploaded, the page silently falls back to fallback_df, i.e. the
      exact same data/filters that already work today. Nothing else is affected."""
    state_key = f"section_file_{section_key}"

    st.markdown(
        f'<div class="upload-box"><p style="color:#A855F7;font-weight:700;font-size:14px">'
        f'📂 Upload Excel for {section_label} (.xlsx / .xls / .csv)</p>'
        f'<p style="font-size:12px;color:#7B2FF7">Optional — leave empty to keep using the master dataset & current filters</p></div>',
        unsafe_allow_html=True,
    )
    new_file = st.file_uploader(
        f"Upload {section_label} Excel",
        type=["xlsx", "xls", "csv"],
        key=f"uploader_{section_key}",
        label_visibility="collapsed",
    )
    if new_file is not None:
        st.session_state[state_key] = new_file

    section_file = st.session_state.get(state_key)
    if section_file is not None:
        try:
            section_raw = load_data(section_file, section_file.name)
            st.success(f"✅ Using '{section_file.name}' for {section_label}")
            return apply_global_filters(section_raw) if apply_filters else section_raw
        except Exception as e:
            st.warning(f"⚠️ Could not read '{section_file.name}' ({e}). Showing master dataset instead.")
            return fallback_df

    return fallback_df


# ── HEADER ─────────────────────────────────────────────────────────────────────
now = datetime.now()
greeting = "Good Morning" if now.hour < 12 else ("Good Afternoon" if now.hour < 17 else "Good Evening")
day_name = now.strftime("%A")
date_str = now.strftime("%B %d, %Y")
time_str = now.strftime("%H:%M:%S")

active_filters = []
if f_year_g != "All":  active_filters.append(f"Year: {f_year_g}")
if f_month_g != "All": active_filters.append(f"Month: {f_month_g}")
if f_rec_g != "All":   active_filters.append(f"Recruiter: {f_rec_g}")
if f_loc_g != "All":   active_filters.append(f"Location: {f_loc_g}")

filter_status = f"Showing {len(df)} of {len(raw_df)} employees" + (f" · {' · '.join(active_filters)}" if active_filters else " · No filters active")

st.markdown(f"""
<div class='dash-header'>
    <div style='display:flex;align-items:center;gap:16px'>
        <div style='width:52px;height:52px;background:rgba(255,255,255,0.1);backdrop-filter:blur(12px);
                    border:1px solid rgba(255,255,255,0.2);border-radius:14px;
                    display:flex;align-items:center;justify-content:center;
                    box-shadow:0 0 20px rgba(123,47,247,0.3)'>
            {LOGO_HTML}
        </div>
        <div>
            <div class='header-title'>Purple United Sales Limited</div>
            <div class='header-sub'>Human Resource Dashboard  ·  Executive Overview</div>
            <div class='header-badge'>✦ {filter_status}</div>
        </div>
    </div>
    <div style='display:flex;align-items:center;gap:20px'>
        <div>
            <div class='header-time' id='live-clock'>{time_str}</div>
            <div class='header-day'>{day_name}</div>
            <div class='header-date'>{date_str}</div>
        </div>
        <div style='text-align:right;'>
            <div style='font-size:11px;color:#A855F7;font-weight:600'>{greeting}</div>
            <div class='header-avatar' style='margin:6px auto 0'>👤</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE FUNCTIONS
# ══════════════════════════════════════════════════════════════════════════════

def page_dashboard():
    st.markdown('<p class="page-title">🏠 Executive Analysis</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">HR metrics · Purple United Sales Limited</p>', unsafe_allow_html=True)

    raw_df = section_file_uploader("dashboard", "Dashboard", BASE_RAW_DF, apply_filters=False)

    # ── INLINE FILTERS ON DASHBOARD ─────────────────────────────────────────
    st.markdown('<div class="filter-panel"><div class="filter-header"><div class="filter-dot"></div><span class="filter-title-text">🔍 Dashboard Filters</span></div></div>', unsafe_allow_html=True)
    fi1, fi2, fi3, fi4, fi5 = st.columns([1, 1, 1, 1, 1])

    with fi1:
        _year_opts = ["All"] + sorted(raw_df["DOJ"].dropna().dt.year.astype(int).unique().tolist(), reverse=True) if "DOJ" in raw_df.columns and raw_df["DOJ"].notna().any() else ["All"]
        _f_year = st.selectbox("📅 Year", _year_opts, key="dash_year")
    with fi2:
        _month_names = ["All","January","February","March","April","May","June","July","August","September","October","November","December"]
        _f_month = st.selectbox("🗓️ Month", _month_names, key="dash_month")
    with fi3:
        _rec_opts = ["All"] + sorted(str(r) for r in raw_df["Recruiter Name"].unique() if str(r).strip() and str(r) != "nan") if "Recruiter Name" in raw_df.columns else ["All"]
        _f_rec = st.selectbox("🧑‍💼 Recruiter", _rec_opts, key="dash_rec")
    with fi4:
        _loc_opts = ["All"] + sorted(str(l) for l in raw_df["Location"].unique() if str(l).strip() and str(l) != "nan") if "Location" in raw_df.columns else ["All"]
        _f_loc = st.selectbox("📍 Location", _loc_opts, key="dash_loc")
    with fi5:
        _dept_opts = ["All"] + sorted(str(d) for d in raw_df["Department"].unique() if str(d).strip() and str(d) != "nan") if "Department" in raw_df.columns else ["All"]
        _f_dept = st.selectbox("🏢 Department", _dept_opts, key="dash_dept")

    # Build a fresh filtered dataframe from raw_df using dashboard filter values
    dash_df = raw_df.copy()
    if _f_year != "All" and "DOJ" in dash_df.columns:
        dash_df = dash_df[dash_df["DOJ"].dt.year == int(_f_year)]
    if _f_month != "All" and "DOJ" in dash_df.columns:
        dash_df = dash_df[dash_df["DOJ"].dt.month == _month_names.index(_f_month)]
    if _f_rec != "All" and "Recruiter Name" in dash_df.columns:
        dash_df = dash_df[dash_df["Recruiter Name"].astype(str) == _f_rec]
    if _f_loc != "All" and "Location" in dash_df.columns:
        dash_df = dash_df[dash_df["Location"].astype(str) == _f_loc]
    if _f_dept != "All" and "Department" in dash_df.columns:
        dash_df = dash_df[dash_df["Department"].astype(str) == _f_dept]

    if dash_df.empty:
        st.warning("⚠️ No data matches the current filters. Try adjusting the filters.")
        return

    today = pd.Timestamp.today()

    # ── KPI CALCULATIONS — all 6 are fully filter-aware via dash_df ────────
    # Total Active
    active = int((raw_df[STATUS_COL] == "Active").sum()) if STATUS_COL in raw_df.columns else 0

    # Exited
    _exit_df = raw_df.copy()
    if "Exit Date" in _exit_df.columns:
        if _f_year != "All":
            _exit_df = _exit_df[_exit_df["Exit Date"].dt.year == int(_f_year)]
        if _f_month != "All":
            _exit_df = _exit_df[_exit_df["Exit Date"].dt.month == _month_names.index(_f_month)]
    if _f_rec != "All" and "Recruiter Name" in _exit_df.columns:
        _exit_df = _exit_df[_exit_df["Recruiter Name"].astype(str) == _f_rec]
    if _f_loc != "All" and "Location" in _exit_df.columns:
        _exit_df = _exit_df[_exit_df["Location"].astype(str) == _f_loc]
    if _f_dept != "All" and "Department" in _exit_df.columns:
        _exit_df = _exit_df[_exit_df["Department"].astype(str) == _f_dept]
    exited = int((_exit_df[STATUS_COL] == "Exited").sum()) if STATUS_COL in _exit_df.columns else 0

    # New Hires = employees whose DOJ falls in the selected month/year
    if "DOJ" in dash_df.columns:
        if _f_month != "All" and _f_year != "All":
            # Both month and year — exact match
            nh_month = _month_names.index(_f_month)
            nh_year  = int(_f_year)
            new_hires_current_month = int(
                ((dash_df["DOJ"].dt.month == nh_month) & (dash_df["DOJ"].dt.year == nh_year)).sum()
            )
        elif _f_month != "All":
            # Only month selected — count across ALL years for that month
            nh_month = _month_names.index(_f_month)
            new_hires_current_month = int(
                (dash_df["DOJ"].dt.month == nh_month).sum()
            )
        elif _f_year != "All":
            # Only year selected — all hires that year
            new_hires_current_month = int(
                (dash_df["DOJ"].dt.year == int(_f_year)).sum()
            )
        else:
            # No filter — show current month hires
            new_hires_current_month = int(
                ((dash_df["DOJ"].dt.month == today.month) & (dash_df["DOJ"].dt.year == today.year)).sum()
            )
    else:
        new_hires_current_month = 0

    # Avg service age — always from raw_df (filter-independent), DOJ to today
    if "DOJ" in raw_df.columns and STATUS_COL in raw_df.columns:
        act_only = raw_df[raw_df[STATUS_COL] == "Active"].copy()
        act_only = act_only[act_only["DOJ"].notna()]
        act_only["Tenure"] = (today - act_only["DOJ"]).dt.days / 365.25
        avg_tenure = round(act_only["Tenure"].mean(), 1) if len(act_only) > 0 else 0
        avg_months = int(round(avg_tenure * 12))
        yrs = avg_months // 12
        mos = avg_months % 12
        if yrs > 0 and mos > 0:
            tenure_label = f"{yrs}y {mos}m"
        elif yrs > 0:
            tenure_label = f"{yrs} yrs"
        else:
            tenure_label = f"{mos} mos"
    else:
        tenure_label = "N/A"

    # Gender diversity — from dash_df (filter-aware)
    if "Gender" in dash_df.columns:
        gc = dash_df["Gender"].str.strip().str.title().value_counts()
        total_g = gc.sum()
        m_pct = round(int(gc.get("Male",   0)) / total_g * 100, 1) if total_g > 0 else 0
        f_pct = round(int(gc.get("Female", 0)) / total_g * 100, 1) if total_g > 0 else 0
        gender_html = f"<span style='color:#F472B6'>F {f_pct}%</span>"
    else:
        gender_html = "N/A"

    # Attrition ratio — filter-aware
    attrition_base = active + exited
    attrition_pct  = round(exited / attrition_base * 100, 1) if attrition_base > 0 else 0
    attrition_color = P["red"] if attrition_pct > 15 else (P["amber"] if attrition_pct > 8 else P["green"])

    # ── 6 KPI CARDS ─────────────────────────────────────────────────────────
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    # Gender card uses raw HTML so we call st.markdown directly
    for col, icon, val, label, accent in [
        (c1, "✅", active,                  "Total Active Employees", P["green"]),
        (c2, "🆕", new_hires_current_month, "New Hires",              P["blue"]),
        (c3, "🚪", exited,                  "Exited",                 P["red"]),
        (c4, "📅", tenure_label,            "Avg Service Age",        P["amber"]),
        (c6, "📉", f"{attrition_pct}%",     "Attrition Ratio",        attrition_color),
    ]:
        with col:
            st.markdown(kpi(icon, val, label, accent), unsafe_allow_html=True)

    # Gender card with two-line value
    with c5:
        st.markdown(f"""
        <div class='kpi-card' style='--accent:{P["secondary"]}'>
            <div class='kpi-glow' style='background:{P["secondary"]}'></div>
            <span class='kpi-icon'>⚧</span>
            <div class='kpi-val'>{gender_html}</div>
            <div class='kpi-label'>Gender Diversity</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # ── ROW 3: Monthly Hiring + Status Donut ─────────────────────────────────
    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if "DOJ" in dash_df.columns and dash_df["DOJ"].notna().any():
            d2 = dash_df.copy()
            d2["YearMonth"] = d2["DOJ"].dt.strftime("%b")
            month_order=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
            trend=d2.groupby("YearMonth").size().reindex(month_order,fill_value=0).reset_index(name="New Hires")
            colors = [P["primary"] if i < len(trend)-3 else P["accent"] for i in range(len(trend))]
            fig1 = go.Figure()
    # ── ROW 3: Monthly Hiring + Status Donut ─────────────────────────────────
    col_a, col_b = st.columns([3, 2])

    with col_a:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if "DOJ" in dash_df.columns and dash_df["DOJ"].notna().any():
            d2 = dash_df.copy()
            d2["YearMonth"] = d2["DOJ"].dt.strftime("%b")
            month_order=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
            trend=d2.groupby("YearMonth").size().reindex(month_order,fill_value=0).reset_index(name="New Hires")
            colors = [P["primary"] if i < len(trend)-3 else P["accent"] for i in range(len(trend))]
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(
                x=trend["YearMonth"], y=trend["New Hires"],
                marker=dict(
                    color=colors,
                    line=dict(color="rgba(0,0,0,0)", width=0),
                ),
                text=trend["New Hires"], textposition="outside",
                textfont=dict(color="#CBD5E1", size=10),
                hovertemplate="<b>%{x}</b><br>New Hires: <b>%{y}</b><extra></extra>",
                name="Monthly Hires"
            ))
            fig1.add_trace(go.Scatter(
                x=trend["YearMonth"], y=trend["New Hires"].rolling(3, min_periods=1).mean(),
                mode="lines", line=dict(color=P["accent"], width=2, dash="dot"),
                name="3M Avg", opacity=0.7,
                hovertemplate="<b>3M Avg: %{y:.1f}</b><extra></extra>",
            ))
            fig1.update_layout(xaxis=dict(tickangle=-35), showlegend=True,
                               legend=dict(orientation="h", y=1.1, x=1, xanchor="right"))
            st.plotly_chart(chart_layout(fig1, 320, "📈 Monthly Hiring Trend"),
                            use_container_width=True, config={"displayModeBar":False}, key="d_hiring_trend")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if STATUS_COL in dash_df.columns:
            sc = dash_df[STATUS_COL].value_counts().reset_index()
            sc.columns = ["Status","Count"]
            status_colors = {"Active": P["green"], "Exited": P["red"],
                             "Notice Period": P["amber"], "Hold": P["blue"]}
            fig2 = go.Figure(go.Pie(
                labels=sc["Status"], values=sc["Count"],
                hole=0.6,
                marker=dict(colors=[status_colors.get(s, P["primary"]) for s in sc["Status"]],
                            line=dict(color="#252938", width=2)),
                textinfo="label+percent",
                textfont=dict(color="#E2E8F0", size=11),
                hovertemplate="<b>%{label}</b><br>Count: <b>%{value}</b><br>Share: <b>%{percent}</b><extra></extra>",
            ))
            fig2.update_layout(
                annotations=[dict(text=f"<b>{len(dash_df)}</b><br><span style='font-size:9px'>TOTAL</span>",
                                  x=0.5, y=0.5, font=dict(size=18, color="#F1F5F9"), showarrow=False)],
                showlegend=True,
                legend=dict(orientation="v", x=1.05),
            )
            st.plotly_chart(chart_layout(fig2, 320, "👥 Status of Employees"),
                            use_container_width=True, config={"displayModeBar":False}, key="d_status_pie")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── ROW 4: Attrition by Dept + Location Hires ────────────────────────────
    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if "Department" in dash_df.columns and STATUS_COL in dash_df.columns:
            dept_data = []
            for dept in sorted(dash_df["Department"].unique()):
                sub = dash_df[dash_df["Department"] == dept]
                sa = (sub[STATUS_COL] == "Active").sum()
                se = (sub[STATUS_COL] == "Exited").sum()
                base = sa + se
                dept_data.append({"Dept": dept, "Active": sa, "Exited": se,
                                  "Attrition %": round(se/base*100,1) if base > 0 else 0})
            adf = pd.DataFrame(dept_data).sort_values("Attrition %", ascending=True)
            fig3 = go.Figure()
            fig3.add_trace(go.Bar(
                x=adf["Active"], y=adf["Dept"], orientation="h",
                name="Active", marker_color=P["green"], opacity=0.85,
                hovertemplate="<b>%{y}</b><br>Active: <b>%{x}</b><extra></extra>",
            ))
            fig3.add_trace(go.Bar(
                x=adf["Exited"], y=adf["Dept"], orientation="h",
                name="Exited", marker_color=P["red"], opacity=0.85,
                hovertemplate="<b>%{y}</b><br>Exited: <b>%{x}</b><extra></extra>",
            ))
            fig3.update_layout(barmode="stack", xaxis_title="Employees",
                               legend=dict(orientation="h", y=1.1, x=0))
            st.plotly_chart(chart_layout(fig3, 320, "📊 Department Headcount (Active vs Exited)"),
                            use_container_width=True, config={"displayModeBar":False}, key="d_dept_stack")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_d:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if "Gender" in dash_df.columns:
            gc = dash_df["Gender"].str.strip().str.title().value_counts().reset_index()
            gc.columns = ["Gender", "Count"]
            gc = gc[gc["Gender"].astype(str).str.strip() != ""]
            if gc.empty:
                gc = raw_df["Gender"].str.strip().str.title().value_counts().reset_index()
                gc.columns = ["Gender", "Count"]
                gc = gc[gc["Gender"].astype(str).str.strip() != ""]
            gender_colors = {"Male": "#6366F1", "Female": "#EC4899", "Other": "#F59E0B"}
            fig4 = go.Figure(go.Bar(
                x=gc["Gender"], y=gc["Count"],
                width=0.35,
                marker=dict(
                    color=[gender_colors.get(g, "#8B5CF6") for g in gc["Gender"]],
                    line=dict(color="rgba(0,0,0,0)", width=0),
                ),
                text=gc["Count"], textposition="outside",
                textfont=dict(color="#4A5568", size=12, family="Inter"),
                hovertemplate="<b>%{x}</b><br>Count: <b>%{y}</b><extra></extra>",
            ))
            fig4.update_layout(xaxis=dict(title=""), yaxis=dict(title=""))
            st.plotly_chart(chart_layout(fig4, 320, "⚖️ Gender Diversity"),
                            use_container_width=True, config={"displayModeBar":False}, key="d_location")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── ROW 5: Exit Trend + Recruiter Performance ────────────────────────────
    col_e, col_f = st.columns(2)

    with col_e:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if "Exit Date" in raw_df.columns and raw_df["Exit Date"].notna().any():
            _ex_raw = raw_df[raw_df["Exit Date"].notna()].copy()
            if _f_year != "All":
                _ex_raw = _ex_raw[_ex_raw["Exit Date"].dt.year == int(_f_year)]
            if _f_month != "All":
                _ex_raw = _ex_raw[_ex_raw["Exit Date"].dt.month == _month_names.index(_f_month)]
            if _f_rec != "All" and "Recruiter Name" in _ex_raw.columns:
                _ex_raw = _ex_raw[_ex_raw["Recruiter Name"].astype(str) == _f_rec]
            if _f_loc != "All" and "Location" in _ex_raw.columns:
                _ex_raw = _ex_raw[_ex_raw["Location"].astype(str) == _f_loc]
            if _f_dept != "All" and "Department" in _ex_raw.columns:
                _ex_raw = _ex_raw[_ex_raw["Department"].astype(str) == _f_dept]
            if not _ex_raw.empty:
                ex = _ex_raw.copy()
                ex["Day"] = ex["Exit Date"].dt.day
                try:
                    ex["DayLabel"] = ex["Exit Date"].dt.strftime("%#d %B")
                except:
                    ex["DayLabel"] = ex["Exit Date"].dt.strftime("%-d %B")
                et = ex.groupby(["Day","DayLabel"]).size().reset_index(name="Exits").sort_values("Day")
                fig5 = go.Figure()
                fig5.add_trace(go.Scatter(
                    x=et["DayLabel"], y=et["Exits"],
                    mode="lines+markers",
                    line=dict(color=P["red"], width=2.5),
                    marker=dict(size=6, color=P["red"], line=dict(color="#252938", width=2)),
                    fill="tozeroy", fillcolor="rgba(239,68,68,0.08)",
                    hovertemplate="<b>%{x}</b><br>Exits: <b>%{y}</b><extra></extra>",
                    name="Monthly Exits"
                ))
                fig5.update_layout(xaxis=dict(tickangle=-35))
                st.plotly_chart(chart_layout(fig5, 300, "🚪 Within-Month Attrition"),
                                use_container_width=True, config={"displayModeBar":False}, key="d_exits")
            else:
                st.info("No exit date data for current filters.")
        else:
            st.info("No exit date data for current filters.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_f:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if "Recruiter Name" in dash_df.columns:
            rc = dash_df["Recruiter Name"].value_counts().reset_index()
            rc.columns = ["Recruiter","Hired"]
            rc_active = []
            for _, row in rc.iterrows():
                sub = dash_df[dash_df["Recruiter Name"] == row["Recruiter"]]
                act = (sub[STATUS_COL] == "Active").sum() if STATUS_COL in dash_df.columns else 0
                rc_active.append(act)
            rc["Active"] = rc_active
            fig6 = go.Figure()
            fig6.add_trace(go.Bar(
                x=rc["Hired"], y=rc["Recruiter"], orientation="h",
                name="Total Hired", marker_color=P["primary"], opacity=0.7,
                hovertemplate="<b>%{y}</b><br>Total Hired: <b>%{x}</b><extra></extra>",
            ))
            fig6.add_trace(go.Bar(
                x=rc["Active"], y=rc["Recruiter"], orientation="h",
                name="Active Now", marker_color=P["accent"], opacity=0.9,
                hovertemplate="<b>%{y}</b><br>Still Active: <b>%{x}</b><extra></extra>",
            ))
            fig6.update_layout(barmode="overlay", legend=dict(orientation="h", y=1.1, x=0))
            st.plotly_chart(chart_layout(fig6, 300, "🧑‍💼 Recruiter Performance"),
                            use_container_width=True, config={"displayModeBar":False}, key="d_recruiter_perf")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── ROW 6: Service Age + Source Distribution ──────────────────────────────
    col_g, col_h = st.columns([3, 2])

    with col_g:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if "DOJ" in dash_df.columns:
            act_only = dash_df[dash_df[STATUS_COL]=="Active"].copy() if STATUS_COL in dash_df.columns else dash_df.copy()
            act_only["Tenure_Y"] = ((today - act_only["DOJ"]).dt.days / 365.25).round(1)
            bins   = [0, 0.5, 1, 2, 3, 5, 10, 100]
            labels = ["<6 Months","6M–1 Year","1–2 Years","2–3 Years","3–5 Years","5–10 Years","10+ Years"]
            act_only["Band"] = pd.cut(act_only["Tenure_Y"], bins=bins, labels=labels)
            bc = act_only["Band"].value_counts().reindex(labels, fill_value=0).reset_index()
            bc.columns = ["Band","Count"]
            band_colors = ["#7B2FF7","#8B3FF8","#9B4FF9","#A855F7","#B865F8","#C075F9","#C084FC"]
            fig7 = go.Figure(go.Bar(
                x=bc["Band"], y=bc["Count"],
                marker=dict(color=band_colors, line=dict(color="rgba(0,0,0,0)", width=0)),
                text=bc["Count"], textposition="outside",
                textfont=dict(color="#CBD5E1"),
                hovertemplate="<b>%{x}</b><br>Employees: <b>%{y}</b><extra></extra>",
            ))
            st.plotly_chart(chart_layout(fig7, 280, "📅 Service Age Distribution (Active Employees)"),
                            use_container_width=True, config={"displayModeBar":False}, key="d_tenure")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_h:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if "Profile Source" in dash_df.columns:
            ps = dash_df["Profile Source"].value_counts().reset_index()
            ps.columns = ["Source","Count"]
            fig8 = go.Figure(go.Pie(
                labels=ps["Source"], values=ps["Count"],
                hole=0.55,
                marker=dict(colors=PALETTE[:len(ps)],
                            line=dict(color="#252938", width=2)),
                textinfo="label+percent",
                textfont=dict(color="#E2E8F0", size=11),
                hovertemplate="<b>%{label}</b><br>Count: <b>%{value}</b><br>Share: <b>%{percent}</b><extra></extra>",
            ))
            st.plotly_chart(chart_layout(fig8, 280, "🌐 Hiring Source Distribution"),
                            use_container_width=True, config={"displayModeBar":False}, key="d_source")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── ROW 7: Department Attrition Heatmap ───────────────────────────────────
    if "Department" in dash_df.columns and "DOJ" in dash_df.columns:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        pivot_data = []
        if dash_df["DOJ"].notna().any():
            df2 = dash_df.copy()
            df2["Year"] = df2["DOJ"].dt.year
            years_avail = sorted(df2["Year"].dropna().astype(int).unique())
            depts_avail = sorted(df2["Department"].unique())
            matrix = pd.DataFrame(index=depts_avail, columns=[str(y) for y in years_avail], data=0)
            for (dept, yr), grp in df2.groupby(["Department","Year"]):
                matrix.loc[dept, str(int(yr))] = len(grp)
            matrix = matrix.astype(int)
            fig9 = px.imshow(
                matrix,
                color_continuous_scale=[[0,"#14162B"],[0.3,"#3B1F7F"],[0.7,P["primary"]],[1,P["accent"]]],
                text_auto=True, aspect="auto",
                title="🗺️ Yearly Hiring Heatmap (Department × Year)"
            )
            fig9.update_traces(
                textfont=dict(color="#E2E8F0", size=11),
                hovertemplate="<b>%{y}</b><br>Year: <b>%{x}</b><br>Hired: <b>%{z}</b><extra></extra>",
            )
            st.plotly_chart(chart_layout(fig9, 280), use_container_width=True,
                            config={"displayModeBar":False}, key="d_heatmap")
        st.markdown('</div>', unsafe_allow_html=True)


# ── Recruitment Page ───────────────────────────────────────────────────────────
def page_recruitment():
    st.markdown('<p class="page-title">📢 Recruitment Analytics</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Hiring pipeline · Recruiter performance · Source analytics</p>', unsafe_allow_html=True)

    raw = section_file_uploader("recruitment", "Recruitment", BASE_RAW_DF, apply_filters=False)

    # ── Recruitment Filters
    st.markdown('<div class="filter-panel"><div class="filter-header"><div class="filter-dot"></div><span class="filter-title-text">🔍 Recruitment Filters</span></div></div>', unsafe_allow_html=True)
    rf1, rf2, rf3, rf4 = st.columns(4)
    with rf1:
        _yr_opts = ["All"] + sorted(raw["DOJ"].dropna().dt.year.astype(int).unique().tolist(), reverse=True) if "DOJ" in raw.columns and raw["DOJ"].notna().any() else ["All"]
        _rec_yr = st.selectbox("📅 Year", _yr_opts, key="rec_year")
    with rf2:
        _mn = ["All","January","February","March","April","May","June","July","August","September","October","November","December"]
        _rec_mo = st.selectbox("🗓️ Month", _mn, key="rec_month")
    with rf3:
        _loc_opts = ["All"] + sorted(str(l) for l in raw["Location"].unique() if str(l).strip() and str(l) != "nan") if "Location" in raw.columns else ["All"]
        _rec_loc = st.selectbox("📍 Location", _loc_opts, key="rec_loc")
    with rf4:
        _recr_opts = ["All"] + sorted(str(r) for r in raw["Recruiter Name"].unique() if str(r).strip() and str(r) != "nan") if "Recruiter Name" in raw.columns else ["All"]
        _rec_recr = st.selectbox("🧑💼 Recruiter", _recr_opts, key="rec_recruiter")

    df = raw.copy()
    if _rec_yr != "All" and "DOJ" in df.columns:
        df = df[df["DOJ"].dt.year == int(_rec_yr)]
    if _rec_mo != "All" and "DOJ" in df.columns:
        df = df[df["DOJ"].dt.month == _mn.index(_rec_mo)]
    if _rec_loc != "All" and "Location" in df.columns:
        df = df[df["Location"].astype(str) == _rec_loc]
    if _rec_recr != "All" and "Recruiter Name" in df.columns:
        df = df[df["Recruiter Name"].astype(str) == _rec_recr]

    if df.empty:
        st.warning("No data matches current filters."); return

    # KPI 1: Total Hired — new hires of the filtered month only
    if "New Joining" in df.columns:
        total_hired = int((df["New Joining"].str.upper() == "DONE").sum())
    elif "DOJ" in df.columns:
        total_hired = int(df["DOJ"].notna().sum())
    else:
        total_hired = len(df)

    # KPI 2: Locations Covered
    locs_count = df["Location"].nunique() if "Location" in df.columns else 0

    # KPI 3: Unique Positions
    pos_count = df["Profile Position"].nunique() if "Profile Position" in df.columns else 0

    # KPI 4: Source Mix
    source_count = df["Profile Source"].nunique() if "Profile Source" in df.columns else 0

    # KPI 5: BGV %
    if "BGV" in df.columns:
        bgv_s = df["BGV"].astype(str).str.strip().str.upper()
        bgv_done = (bgv_s == "DONE").sum()
        bgv_total = len(df)
        bgv_pct = round(bgv_done / bgv_total * 100, 1) if bgv_total > 0 else 0
    else:
        bgv_pct = 0

    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.markdown(kpi("👥", total_hired, "Total Hired", P["primary"]), unsafe_allow_html=True)
    with c2: st.markdown(kpi("📍", locs_count, "Locations Covered", P["teal"]), unsafe_allow_html=True)
    with c3: st.markdown(kpi("💼", pos_count, "Unique Positions", P["accent"]), unsafe_allow_html=True)
    with c4: st.markdown(kpi("🌐", source_count, "Source Mix", P["secondary"]), unsafe_allow_html=True)
    with c5: st.markdown(kpi("🔍", f"{bgv_pct}%", "BGV Done", P["green"] if bgv_pct >= 80 else P["amber"]), unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    col_a,col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if "Location" in df.columns:
            lc = df["Location"].value_counts().reset_index(); lc.columns=["Location","Count"]
            fig = go.Figure(go.Bar(
                x=lc["Location"], y=lc["Count"],
                marker=dict(color=PALETTE[:len(lc)]),
                text=lc["Count"], textposition="outside",
                textfont=dict(color="#CBD5E1"),
                hovertemplate="<b>%{x}</b><br>Hired: <b>%{y}</b><extra></extra>",
            ))
            st.plotly_chart(chart_layout(fig, 300, "📍 Location-wise Hiring"),
                            use_container_width=True, config={"displayModeBar":False}, key="r_loc")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if "Profile Source" in df.columns:
            sc = df["Profile Source"].value_counts().reset_index(); sc.columns=["Source","Count"]
            fig2 = go.Figure(go.Pie(
                labels=sc["Source"], values=sc["Count"], hole=0.55,
                marker=dict(colors=PALETTE[:len(sc)], line=dict(color="#252938", width=2)),
                textinfo="label+percent",
                hovertemplate="<b>%{label}</b><br>Count: <b>%{value}</b><br>%{percent}<extra></extra>",
            ))
            st.plotly_chart(chart_layout(fig2, 300, "🌐 Recruitment Source Mix"),
                            use_container_width=True, config={"displayModeBar":False}, key="r_src")
        st.markdown('</div>', unsafe_allow_html=True)

    col_c,col_d = st.columns(2)
    with col_c:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if "Recruiter Name" in df.columns:
            rc = df.groupby("Recruiter Name").agg(
                Total=("Emp Code","count"),
                Active=(STATUS_COL, lambda x: (x=="Active").sum()) if STATUS_COL in df.columns else ("Emp Code","count")
            ).reset_index().sort_values("Total", ascending=True)
            fig3 = go.Figure()
            fig3.add_trace(go.Bar(x=rc["Total"], y=rc["Recruiter Name"], orientation="h",
                                  name="Total Recruited", marker_color=P["primary"], opacity=0.7,
                                  hovertemplate="<b>%{y}</b><br>Total: <b>%{x}</b><extra></extra>"))
            fig3.add_trace(go.Bar(x=rc["Active"], y=rc["Recruiter Name"], orientation="h",
                                  name="Still Active", marker_color=P["accent"],
                                  hovertemplate="<b>%{y}</b><br>Active: <b>%{x}</b><extra></extra>"))
            fig3.update_layout(barmode="overlay", legend=dict(orientation="h", y=1.12, x=0))
            st.plotly_chart(chart_layout(fig3, 300, "🧑‍💼 Recruiter Performance"),
                            use_container_width=True, config={"displayModeBar":False}, key="r_rec")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_d:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if "Profile Position" in df.columns:
            pc = df["Profile Position"].value_counts().head(10).reset_index(); pc.columns=["Position","Count"]
            fig4 = go.Figure(go.Bar(
                x=pc["Count"], y=pc["Position"], orientation="h",
                marker=dict(
                    color=pc["Count"],
                    colorscale=[[0,"#3B1F7F"],[1,P["accent"]]],
                    showscale=False,
                ),
                text=pc["Count"], textposition="outside",
                textfont=dict(color="#CBD5E1"),
                hovertemplate="<b>%{y}</b><br>Hired: <b>%{x}</b><extra></extra>",
            ))
            st.plotly_chart(chart_layout(fig4, 300, "💼 Top Positions Hired"),
                            use_container_width=True, config={"displayModeBar":False}, key="r_pos")
        st.markdown('</div>', unsafe_allow_html=True)

    if "DOJ" in df.columns and df["DOJ"].notna().any():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        d2 = df.copy()
        d2["Month"] = d2["DOJ"].dt.to_period("M").astype(str)
        mt = d2.groupby("Month").size().reset_index(name="Hires").tail(24)
        fig5 = go.Figure()
        fig5.add_trace(go.Bar(x=mt["Month"], y=mt["Hires"],
                               marker_color=P["primary"], opacity=0.8,
                               text=mt["Hires"], textposition="outside",
                               textfont=dict(color="#CBD5E1"),
                               hovertemplate="<b>%{x}</b><br>Hires: <b>%{y}</b><extra></extra>"))
        fig5.add_trace(go.Scatter(x=mt["Month"], y=mt["Hires"].rolling(3,min_periods=1).mean(),
                                   mode="lines", line=dict(color=P["accent"], width=2, dash="dot"),
                                   name="3M Avg", hovertemplate="3M Avg: <b>%{y:.1f}</b><extra></extra>"))
        fig5.update_layout(showlegend=True, xaxis=dict(tickangle=-35))
        st.plotly_chart(chart_layout(fig5, 280, "📈 Monthly Hiring Trend (Full History)"),
                        use_container_width=True, config={"displayModeBar":False}, key="r_trend")
        st.markdown('</div>', unsafe_allow_html=True)


# ── HR Documentation ───────────────────────────────────────────────────────────
def page_documentation():
    st.markdown('<p class="page-title">📑 HR Documentation</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Document completion tracking across all employee records</p>', unsafe_allow_html=True)

    raw = section_file_uploader("hr_documentation", "HR Documentation", BASE_RAW_DF, apply_filters=False)

    # ── Documentation Filters
    st.markdown('<div class="filter-panel"><div class="filter-header"><div class="filter-dot"></div><span class="filter-title-text">🔍 Documentation Filters</span></div></div>', unsafe_allow_html=True)
    df1, df2, df3 = st.columns(3)
    with df1:
        _yr_opts = ["All"] + sorted(raw["DOJ"].dropna().dt.year.astype(int).unique().tolist(), reverse=True) if "DOJ" in raw.columns and raw["DOJ"].notna().any() else ["All"]
        _doc_yr = st.selectbox("📅 Year", _yr_opts, key="doc_year")
    with df2:
        _mn = ["All","January","February","March","April","May","June","July","August","September","October","November","December"]
        _doc_mo = st.selectbox("🗓️ Month", _mn, key="doc_month")
    with df3:
        _dept_opts = ["All"] + sorted(str(d) for d in raw["Department"].unique() if str(d).strip() and str(d) != "nan") if "Department" in raw.columns else ["All"]
        _doc_dept = st.selectbox("🏢 Department", _dept_opts, key="doc_dept")

    df = raw.copy()
    if _doc_yr != "All" and "DOJ" in df.columns:
        df = df[df["DOJ"].dt.year == int(_doc_yr)]
    if _doc_mo != "All" and "DOJ" in df.columns:
        df = df[df["DOJ"].dt.month == _mn.index(_doc_mo)]
    if _doc_dept != "All" and "Department" in df.columns:
        df = df[df["Department"].astype(str) == _doc_dept]

    if df.empty:
        st.warning("No data matches current filters."); return

    doc_avail = [c for c in DOC_COLS if c in df.columns]
    if not doc_avail:
        st.warning("No documentation columns found."); return

    cols = st.columns(len(doc_avail))
    for i, col in enumerate(doc_avail):
        d, p, na = compliance_counts(df[col])
        total_dp = d + p
        pct = round(d/total_dp*100,1) if total_dp > 0 else 0
        with cols[i]:
            ac = P["green"] if pct >= 80 else (P["amber"] if pct >= 60 else P["red"])
            st.markdown(kpi("📄", f"{pct}%", col[:18], ac), unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        data = []
        for c in doc_avail:
            dn, pe, na = compliance_counts(df[c])
            data.append({"Document": c, "Done": dn, "Pending": pe, "N/A": na})
        ddf2 = pd.DataFrame(data)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=ddf2["Document"], y=ddf2["Done"], name="Done",
                             marker_color=P["green"],
                             hovertemplate="<b>%{x}</b><br>Done: <b>%{y}</b><extra></extra>"))
        fig.add_trace(go.Bar(x=ddf2["Document"], y=ddf2["Pending"], name="Pending",
                             marker_color=P["red"],
                             hovertemplate="<b>%{x}</b><br>Pending: <b>%{y}</b><extra></extra>"))
        fig.update_layout(barmode="stack", xaxis=dict(tickangle=-20),
                          legend=dict(orientation="h", y=1.1, x=0))
        st.plotly_chart(chart_layout(fig, 320, "📊 Documentation Status by Type"),
                        use_container_width=True, config={"displayModeBar":False}, key="doc_stack")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        pcts = []
        for c in doc_avail:
            dn, pe, _ = compliance_counts(df[c])
            tot = dn + pe
            pcts.append(round(dn/tot*100,1) if tot > 0 else 0)
        fig2 = go.Figure(go.Bar(
            x=doc_avail, y=pcts,
            marker=dict(
                color=pcts,
                colorscale=[[0,P["red"]],[0.6,P["amber"]],[1,P["green"]]],
                cmin=0, cmax=100,
            ),
            text=[f"{p}%" for p in pcts], textposition="outside",
            textfont=dict(color="#CBD5E1"),
            hovertemplate="<b>%{x}</b><br>Completion: <b>%{y}%</b><extra></extra>",
        ))
        fig2.update_layout(xaxis=dict(tickangle=-20), yaxis=dict(range=[0,115]))
        st.plotly_chart(chart_layout(fig2, 320, "✅ Completion % per Document"),
                        use_container_width=True, config={"displayModeBar":False}, key="doc_pct")
        st.markdown('</div>', unsafe_allow_html=True)

    if "Department" in df.columns:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        dept_rows = []
        for d in sorted(df["Department"].unique()):
            sub = df[df["Department"] == d]
            row = {"Department": d}
            for c in doc_avail:
                dn, pe, _ = compliance_counts(sub[c])
                tot = dn + pe
                row[c] = round(dn/tot*100,1) if tot > 0 else 0
            dept_rows.append(row)
        dept_df2 = pd.DataFrame(dept_rows)
        fig3 = px.imshow(
            dept_df2.set_index("Department")[doc_avail].T,
            color_continuous_scale=[[0,"#14162B"],[0.4,P["red"]],[0.7,P["amber"]],[1,P["green"]]],
            zmin=0, zmax=100, text_auto=True,
        )
        fig3.update_traces(
            textfont=dict(color="#E2E8F0"),
            hovertemplate="<b>%{x}</b><br>%{y}: <b>%{z}%</b><extra></extra>",
        )
        st.plotly_chart(chart_layout(fig3, 340, "🗺️ Documentation Heatmap by Department (%)"),
                        use_container_width=True, config={"displayModeBar":False}, key="doc_heat")
        st.markdown('</div>', unsafe_allow_html=True)


# ── Payroll ────────────────────────────────────────────────────────────────────
def page_payroll():
    st.markdown('<p class="page-title">💰 Payroll</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Joining, resignation and full & final settlement tracking</p>', unsafe_allow_html=True)

    df = section_file_uploader("payroll", "Payroll", BASE_DF)

    # Column mapping: detect actual column names from uploaded file
    _doj_col = "Date of Joining" if "Date of Joining" in df.columns else ("DOJ" if "DOJ" in df.columns else None)
    _exit_col = "Date of Exit" if "Date of Exit" in df.columns else ("Exit Date" if "Exit Date" in df.columns else None)
    _ff_col = "F&F Status" if "F&F Status" in df.columns else ("F&F" if "F&F" in df.columns else None)

    if _doj_col and _doj_col != "Date of Joining":
        df["Date of Joining"] = pd.to_datetime(df[_doj_col], errors="coerce")
    elif _doj_col:
        df["Date of Joining"] = pd.to_datetime(df["Date of Joining"], errors="coerce")
    else:
        df["Date of Joining"] = pd.NaT

    if _exit_col and _exit_col != "Date of Exit":
        df["Date of Exit"] = pd.to_datetime(df[_exit_col], errors="coerce")
    elif _exit_col:
        df["Date of Exit"] = pd.to_datetime(df["Date of Exit"], errors="coerce")
    else:
        df["Date of Exit"] = pd.NaT

    if _ff_col and _ff_col != "F&F Status":
        df["F&F Status"] = df[_ff_col].astype(str).str.strip()
    elif _ff_col:
        df["F&F Status"] = df["F&F Status"].astype(str).str.strip()
    else:
        df["F&F Status"] = ""

    # ── Payroll Filters
    st.markdown('<div class="filter-panel"><div class="filter-header"><div class="filter-dot"></div><span class="filter-title-text">🔍 Payroll Filters</span></div></div>', unsafe_allow_html=True)
    pf1, pf2, pf3, pf4 = st.columns(4)
    with pf1:
        _yr_opts = ["All"] + sorted(df["Date of Joining"].dropna().dt.year.astype(int).unique().tolist(), reverse=True) if df["Date of Joining"].notna().any() else ["All"]
        _pay_yr = st.selectbox("📅 Year", _yr_opts, key="pay_year")
    with pf2:
        _mn = ["All","January","February","March","April","May","June","July","August","September","October","November","December"]
        _pay_mo = st.selectbox("🗓️ Month", _mn, key="pay_month")
    with pf3:
        _emp_opts = ["All"] + sorted(str(e) for e in df["Employee Name"].unique() if str(e).strip() and str(e) != "nan") if "Employee Name" in df.columns else ["All"]
        _pay_emp = st.selectbox("👤 Employee Name", _emp_opts, key="pay_emp")
    with pf4:
        _ff_opts = ["All"] + sorted(str(f) for f in df["F&F Status"].unique() if str(f).strip() and str(f) != "nan") if "F&F Status" in df.columns else ["All"]
        _pay_ff = st.selectbox("💼 F&F Status", _ff_opts, key="pay_ff")

    # Apply employee name filter to base df
    if _pay_emp != "All" and "Employee Name" in df.columns:
        df = df[df["Employee Name"].astype(str) == _pay_emp]

    # Build joining_df (filtered by Date of Joining month/year)
    joining_df = df.copy()
    if _pay_yr != "All":
        joining_df = joining_df[joining_df["Date of Joining"].dt.year == int(_pay_yr)]
    if _pay_mo != "All":
        joining_df = joining_df[joining_df["Date of Joining"].dt.month == _mn.index(_pay_mo)]
    joining_df = joining_df[joining_df["Date of Joining"].notna()]

    # Build exited_df (filtered by Date of Exit month/year)
    exited_df = df[df["Date of Exit"].notna()].copy()
    if _pay_yr != "All":
        exited_df = exited_df[exited_df["Date of Exit"].dt.year == int(_pay_yr)]
    if _pay_mo != "All":
        exited_df = exited_df[exited_df["Date of Exit"].dt.month == _mn.index(_pay_mo)]
    if _pay_ff != "All" and "F&F Status" in exited_df.columns:
        exited_df = exited_df[exited_df["F&F Status"].astype(str).str.strip().str.upper() == _pay_ff.strip().upper()]

    # KPI values
    nj      = len(joining_df)
    # Total Resignations = all employees with valid Date of Exit (before F&F filter)
    res_df  = df[df["Date of Exit"].notna()].copy()
    if _pay_yr != "All":
        res_df = res_df[res_df["Date of Exit"].dt.year == int(_pay_yr)]
    if _pay_mo != "All":
        res_df = res_df[res_df["Date of Exit"].dt.month == _mn.index(_pay_mo)]
    # Fallback: if no Exit Date rows but Resign column has DONE entries, use Resign column
    if len(res_df) == 0 and "Resign" in df.columns:
        res_df = df[df["Resign"].astype(str).str.strip().str.upper() == "DONE"].copy()
    res     = len(res_df)
    ff_done = int((res_df["F&F Status"].astype(str).str.strip().str.lower().isin(["completed", "done"])).sum()) if "F&F Status" in res_df.columns else 0
    ff_pend = res - ff_done

    c1,c2,c3,c4 = st.columns(4)
    with c1: st.markdown(kpi("🆕", nj,      "New Joinings Processed", P["green"]),    unsafe_allow_html=True)
    with c2: st.markdown(kpi("🚪", res,     "Resignations",           P["red"]),      unsafe_allow_html=True)
    with c3: st.markdown(kpi("✅", ff_done, "F&F Completed",          P["primary"]),  unsafe_allow_html=True)
    with c4: st.markdown(kpi("⏳", ff_pend, "F&F Pending",            P["amber"]),    unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Charts ──────────────────────────────────────────────────────────────
    col_ch1, col_ch2 = st.columns(2)
    with col_ch1:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if joining_df["Date of Joining"].notna().any():
            jt = joining_df.copy()
            jt["Month"] = jt["Date of Joining"].dt.strftime("%b")
            month_order=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
            jt_grp = jt.groupby("Month").size().reindex(month_order, fill_value=0).reset_index(name="Joinings")
            fig_j = go.Figure(go.Bar(
                x=jt_grp["Month"], y=jt_grp["Joinings"],
                marker_color=P["green"], opacity=0.85,
                text=jt_grp["Joinings"], textposition="outside",
                textfont=dict(color="#CBD5E1"),
                hovertemplate="<b>%{x}</b><br>Joinings: <b>%{y}</b><extra></extra>",
            ))
            st.plotly_chart(chart_layout(fig_j, 280, "📅 Monthly Joining Trend"),
                            use_container_width=True, config={"displayModeBar":False}, key="p_join_trend")
        else:
            st.info("No joining data available.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_ch2:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if exited_df["Date of Exit"].notna().any():
            et = exited_df.copy()
            et["Month"] = et["Date of Exit"].dt.strftime("%b")
            month_order=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
            et_grp = et.groupby("Month").size().reindex(month_order, fill_value=0).reset_index(name="Exits")
            fig_e = go.Figure(go.Scatter(
                x=et_grp["Month"], y=et_grp["Exits"],
                mode="lines+markers",
                line=dict(color=P["red"], width=2.5),
                marker=dict(size=6, color=P["red"]),
                fill="tozeroy", fillcolor="rgba(239,68,68,0.08)",
                hovertemplate="<b>%{x}</b><br>Exits: <b>%{y}</b><extra></extra>",
            ))
            st.plotly_chart(chart_layout(fig_e, 280, "📉 Monthly Exit Trend"),
                            use_container_width=True, config={"displayModeBar":False}, key="p_exit_trend")
        else:
            st.info("No exit data available.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    if "F&F Status" in exited_df.columns and len(exited_df) > 0:
        ff_counts = exited_df["F&F Status"].astype(str).str.strip().str.upper().value_counts().reset_index()
        ff_counts.columns = ["Status", "Count"]
        ff_colors = {"DONE": P["green"], "PENDING": P["amber"]}
        fig_ff = go.Figure(go.Pie(
            labels=ff_counts["Status"], values=ff_counts["Count"],
            hole=0.6,
            marker=dict(colors=[ff_colors.get(s, P["primary"]) for s in ff_counts["Status"]],
                        line=dict(color="#252938", width=2)),
            textinfo="label+percent",
            hovertemplate="<b>%{label}</b><br>Count: <b>%{value}</b><br>%{percent}<extra></extra>",
        ))
        fig_ff.update_layout(
            annotations=[dict(text=f"<b>{len(exited_df)}</b><br><span style='font-size:9px'>TOTAL</span>",
                              x=0.5, y=0.5, font=dict(size=18, color="#1A202C"), showarrow=False)],
        )
        st.plotly_chart(chart_layout(fig_ff, 280, "💼 F&F Status Distribution"),
                        use_container_width=True, config={"displayModeBar":False}, key="p_ff_donut")
    else:
        st.info("No F&F data available.")
    st.markdown('</div>', unsafe_allow_html=True)

    tab1,tab2,tab3 = st.tabs(["🆕 New Joining", "🚪 Resignation", "💼 F&F Settlement"])

    with tab1:
        sec("📋", f"New Joinings — {len(joining_df)} records")
        st.dataframe(joining_df, use_container_width=True, height=280)
        if len(joining_df) > 0:
            st.download_button("⬇️ Download New Joinings", to_excel(joining_df), "new_joinings.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    with tab2:
        sec("📋", f"Resignation Records — {len(exited_df)} employees")
        st.dataframe(exited_df, use_container_width=True, height=280)
        if len(exited_df) > 0:
            st.download_button("⬇️ Download Resignations", to_excel(exited_df), "resignations.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    with tab3:
        col_a,col_b = st.columns(2)
        with col_a:
            ff_done_df = exited_df[exited_df["F&F Status"].astype(str).str.strip().str.upper() == "DONE"] if "F&F Status" in exited_df.columns else pd.DataFrame()
            sec("✅", f"F&F Completed — {len(ff_done_df)} employees")
            st.dataframe(ff_done_df, use_container_width=True, height=250)
        with col_b:
            ff_pend_df = exited_df[exited_df["F&F Status"].astype(str).str.strip().str.upper() == "PENDING"] if "F&F Status" in exited_df.columns else pd.DataFrame()
            sec("⏳", f"F&F Pending — {len(ff_pend_df)} employees")
            st.dataframe(ff_pend_df, use_container_width=True, height=250)
        if len(exited_df) > 0:
            st.download_button("⬇️ Download F&F Report", to_excel(exited_df), "ff_report.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ── Compliance ────────────────────────────────────────────────────────────────
def page_compliance():
    st.markdown('<p class="page-title">⚖️ Compliance</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">PF · ESIC · PT · LWF compliance status</p>', unsafe_allow_html=True)

    raw = section_file_uploader("compliance", "Compliance", BASE_RAW_DF, apply_filters=False)

    # ── Compliance Filters
    st.markdown('<div class="filter-panel"><div class="filter-header"><div class="filter-dot"></div><span class="filter-title-text">🔍 Compliance Filters</span></div></div>', unsafe_allow_html=True)
    cf1, cf2, cf3 = st.columns(3)
    with cf1:
        _yr_opts = ["All"] + sorted(raw["DOJ"].dropna().dt.year.astype(int).unique().tolist(), reverse=True) if "DOJ" in raw.columns and raw["DOJ"].notna().any() else ["All"]
        _comp_yr = st.selectbox("📅 Year", _yr_opts, key="comp_year")
    with cf2:
        _mn = ["All","January","February","March","April","May","June","July","August","September","October","November","December"]
        _comp_mo = st.selectbox("🗓️ Month", _mn, key="comp_month")
    with cf3:
        _dept_opts = ["All"] + sorted(str(d) for d in raw["Department"].unique() if str(d).strip() and str(d) != "nan") if "Department" in raw.columns else ["All"]
        _comp_dept = st.selectbox("🏢 Department", _dept_opts, key="comp_dept")

    df = raw.copy()
    if _comp_yr != "All" and "DOJ" in df.columns:
        df = df[df["DOJ"].dt.year == int(_comp_yr)]
    if _comp_mo != "All" and "DOJ" in df.columns:
        df = df[df["DOJ"].dt.month == _mn.index(_comp_mo)]
    if _comp_dept != "All" and "Department" in df.columns:
        df = df[df["Department"].astype(str) == _comp_dept]

    if df.empty:
        st.warning("No data matches current filters."); return

    comp_avail = [c for c in COMPLIANCE_COLS if c in df.columns]
    if not comp_avail:
        st.warning("No compliance columns (PF, ESIC, PT, LWF) found."); return

    pcts = {c: compliance_pct(df[c]) for c in comp_avail}
    overall = round(np.mean(list(pcts.values())), 1)

    cols = st.columns(len(comp_avail)+1)
    for i, c in enumerate(comp_avail):
        ac = P["green"] if pcts[c] >= 80 else (P["amber"] if pcts[c] >= 60 else P["red"])
        with cols[i]:
            st.markdown(kpi("📋", f"{pcts[c]}%", c, ac), unsafe_allow_html=True)
    with cols[-1]:
        ac = P["green"] if overall >= 80 else (P["amber"] if overall >= 60 else P["red"])
        st.markdown(kpi("⚖️", f"{overall}%", "Overall Compliance", ac), unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    col_a,col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=overall,
            title={"text":"Overall Compliance %","font":{"color":"#E2E8F0","size":13}},
            number={"font":{"color":"#F1F5F9","size":40},"suffix":"%"},
            gauge={
                "axis":{"range":[0,100],"tickfont":{"color":CHART_TEXT}},
                "bar":{"color":P["primary"],"thickness":0.8},
                "bgcolor":CHART_BG,
                "bordercolor":"rgba(123,47,247,0.3)",
                "steps":[{"range":[0,60],"color":"rgba(239,68,68,0.15)"},
                          {"range":[60,80],"color":"rgba(245,158,11,0.15)"},
                          {"range":[80,100],"color":"rgba(16,185,129,0.15)"}],
                "threshold":{"line":{"color":P["accent"],"width":3},"thickness":0.8,"value":80},
            }
        ))
        st.plotly_chart(chart_layout(fig, 300, ""), use_container_width=True,
                        config={"displayModeBar":False}, key="comp_gauge")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        bars = []
        for c in comp_avail:
            dn,pe,na = compliance_counts(df[c])
            bars.append({"Type":c, "Done":dn, "Pending":pe, "N/A":na})
        bdf = pd.DataFrame(bars)
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=bdf["Type"], y=bdf["Done"], name="Done",
                              marker_color=P["green"],
                              hovertemplate="<b>%{x}</b><br>Done: <b>%{y}</b><extra></extra>"))
        fig2.add_trace(go.Bar(x=bdf["Type"], y=bdf["Pending"], name="Pending",
                              marker_color=P["red"],
                              hovertemplate="<b>%{x}</b><br>Pending: <b>%{y}</b><extra></extra>"))
        fig2.update_layout(barmode="stack", legend=dict(orientation="h", y=1.1, x=0))
        st.plotly_chart(chart_layout(fig2, 300, "📊 Compliance Status Breakdown"),
                        use_container_width=True, config={"displayModeBar":False}, key="comp_stack")
        st.markdown('</div>', unsafe_allow_html=True)

    if "Department" in df.columns:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        dept_rows = []
        for d in sorted(df["Department"].unique()):
            sub = df[df["Department"]==d]
            row = {"Department":d}
            for c in comp_avail:
                row[c] = compliance_pct(sub[c])
            row["Overall %"] = round(np.mean([row[c] for c in comp_avail]),1)
            dept_rows.append(row)
        ddf2 = pd.DataFrame(dept_rows)
        fig3 = go.Figure()
        for i, c in enumerate(comp_avail):
            fig3.add_trace(go.Bar(x=ddf2["Department"], y=ddf2[c], name=c,
                                  marker_color=PALETTE[i],
                                  hovertemplate=f"<b>%{{x}}</b><br>{c}: <b>%{{y}}%</b><extra></extra>"))
        fig3.add_hline(y=80, line_dash="dash", line_color=P["accent"], opacity=0.7,
                       annotation_text="80% target", annotation_font_color=P["accent"])
        fig3.update_layout(barmode="group", legend=dict(orientation="h", y=1.1, x=0))
        st.plotly_chart(chart_layout(fig3, 300, "🏢 Department-wise Compliance %"),
                        use_container_width=True, config={"displayModeBar":False}, key="comp_dept")
        st.dataframe(ddf2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    sec("⏳", "Pending Compliance by Employee")
    pend_rows = []
    for _, row in df.iterrows():
        missing = [c for c in comp_avail if str(row[c]).strip()==""]
        if missing:
            pend_rows.append({"Emp Code":row.get("Emp Code",""),
                              "Employee Name":row.get("Employee Name",""),
                              "Department":row.get("Department",""),
                              "Pending":", ".join(missing), "Count":len(missing)})
    pdf = pd.DataFrame(pend_rows)
    if len(pdf) > 0:
        st.markdown(f"**{len(pdf)} employees** have pending compliance items")
        st.dataframe(pdf.sort_values("Count",ascending=False), use_container_width=True, height=350)
        st.download_button("⬇️ Download", to_excel(pdf), "compliance_pending.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.success("🎉 All compliance items are complete for current filters!")


# ── Labour Compliance ──────────────────────────────────────────────────────────
def _parse_labour_excel(df_raw):
    """Parse multi-section labour compliance Excel.
    The file may have repeated State/City columns with different compliance
    sections (S&E, Trade License, Form A under POG Act) spread across.
    This function detects and consolidates them into a unified dataframe."""
    cols = list(df_raw.columns)
    cols_lower = [str(c).strip().lower() for c in cols]

    # Fuzzy keyword matchers
    def is_state(c): return c.strip().lower() in ["state", "states"]
    def is_city(c): return any(k in c.strip().lower() for k in ["city", "store location", "store", "location"])
    def is_se(c): return any(k in c.strip().lower() for k in ["s&e", "s & e", "se ", "shops & establishment", "shops and establishment", "s&e rc", "s&e status"])
    def is_trade(c): return any(k in c.strip().lower() for k in ["trade", "trade license", "trade licence", "trade lic"])
    def is_pog(c): return any(k in c.strip().lower() for k in ["form a", "pog", "pog act", "form a under pog"])

    # Find state column indices to detect sections
    state_indices = [i for i, c in enumerate(cols) if is_state(str(c))]

    if len(state_indices) <= 1:
        # Single section — just do fuzzy column rename
        return None  # signal to use standard logic

    # Multi-section mode: parse each section
    sections = []
    for idx, si in enumerate(state_indices):
        end = state_indices[idx + 1] if idx + 1 < len(state_indices) else len(cols)
        section_cols = cols[si:end]
        section_df = df_raw.iloc[:, si:end].copy()
        section_df.columns = section_cols

        # Find state and city columns in this section
        s_col = next((c for c in section_cols if is_state(str(c))), None)
        c_col = next((c for c in section_cols if is_city(str(c))), None)

        # Find compliance column in this section
        comp_col = None
        comp_name = None
        for c in section_cols:
            if is_se(str(c)) and not is_state(str(c)) and not is_city(str(c)):
                comp_col = c; comp_name = "S&E"; break
            elif is_trade(str(c)):
                comp_col = c; comp_name = "Trade Licence"; break
            elif is_pog(str(c)):
                comp_col = c; comp_name = "Form A under POG Act"; break

        # Also check for status columns (like "RC Status", "Status") as the compliance value
        if comp_col is None:
            for c in section_cols:
                cl = str(c).strip().lower()
                if cl not in [str(s_col).strip().lower(), str(c_col).strip().lower() if c_col else ""] and "status" in cl:
                    # Determine which compliance this status belongs to based on section position
                    if idx == 0: comp_col = c; comp_name = "S&E"
                    elif idx == 1: comp_col = c; comp_name = "Trade Licence"
                    elif idx == 2: comp_col = c; comp_name = "Form A under POG Act"
                    break

        if s_col and comp_col and comp_name:
            temp = pd.DataFrame()
            temp["State"] = section_df[s_col].astype(str).str.strip()
            temp["City"] = section_df[c_col].astype(str).str.strip() if c_col else ""
            temp[comp_name] = section_df[comp_col].astype(str).str.strip()
            sections.append((comp_name, temp))

    if not sections:
        return None

    # Merge sections on State + City
    merged = None
    for comp_name, temp in sections:
        if merged is None:
            merged = temp[["State", "City", comp_name]].copy()
        else:
            # Left join on State+City
            section_part = temp[["State", "City", comp_name]].copy()
            merged = merged.merge(section_part, on=["State", "City"], how="outer", suffixes=("", "_dup"))
            # Remove duplicate columns
            merged = merged[[c for c in merged.columns if not c.endswith("_dup")]]

    # Fill blanks
    if merged is not None:
        merged = merged.fillna("")
    return merged


def page_labour():
    st.markdown('<p class="page-title">🏭 Labour Compliance</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Store-wise · S&E · Trade Licence · Form A under POG Act</p>', unsafe_allow_html=True)

    df = section_file_uploader("labour_compliance", "Labour Compliance", BASE_DF)

    # Try to parse multi-section labour Excel format
    parsed = _parse_labour_excel(df)
    if parsed is not None:
        df = parsed

    # Detect store-wise mode: file has State + City columns but no employee fields
    STORE_STATE_COL = next((c for c in df.columns if str(c).strip().lower() in ["state", "states"]), None)
    STORE_CITY_COL  = next((c for c in df.columns if str(c).strip().lower() in
                            ["city", "city / store location", "city/store location", "city ", "store location"]), None)
    is_store_mode = (STORE_STATE_COL is not None and STORE_CITY_COL is not None
                     and "Employee Name" not in df.columns and "Emp Code" not in df.columns)

    # Handle alternate column names for labour compliance (fuzzy)
    col_map = {}
    if "S&E" not in df.columns:
        for c in df.columns:
            cl = str(c).strip().lower()
            if any(k in cl for k in ["s&e", "s & e", "shops & establishment", "shops and establishment"]):
                col_map[c] = "S&E"; break
    if "Trade Licence" not in df.columns:
        for c in df.columns:
            cl = str(c).strip().lower()
            if any(k in cl for k in ["trade license", "trade licence", "trade lic", "trade"]):
                if "state" not in cl and "city" not in cl:
                    col_map[c] = "Trade Licence"; break
    if "Form A under POG Act" not in df.columns:
        for c in df.columns:
            cl = str(c).strip().lower()
            if any(k in cl for k in ["form a", "pog act", "pog", "form a under pog"]):
                col_map[c] = "Form A under POG Act"; break
    if col_map:
        df = df.rename(columns=col_map)

    lab_avail = [c for c in LABOUR_COLS if c in df.columns]
    if not lab_avail:
        st.warning("No labour compliance columns found (expected: S&E, Trade Licence, Form A under POG Act)."); return

    # ── Labour Compliance Filters
    st.markdown('<div class="filter-panel"><div class="filter-header"><div class="filter-dot"></div><span class="filter-title-text">🔍 Labour Compliance Filters</span></div></div>', unsafe_allow_html=True)
    lf1, lf2 = st.columns(2)
    with lf1:
        if STORE_STATE_COL and STORE_STATE_COL in df.columns:
            _st_opts = ["All"] + sorted(str(s) for s in df[STORE_STATE_COL].unique() if str(s).strip() and str(s) != "nan")
        else:
            _st_opts = ["All"]
        _lab_state = st.selectbox("🏢 State", _st_opts, key="lab_state")
    with lf2:
        if STORE_CITY_COL and STORE_CITY_COL in df.columns:
            _ct_opts = ["All"] + sorted(str(c) for c in df[STORE_CITY_COL].unique() if str(c).strip() and str(c) != "nan")
        else:
            _ct_opts = ["All"]
        _lab_city = st.selectbox("📍 City", _ct_opts, key="lab_city")

    if _lab_state != "All" and STORE_STATE_COL and STORE_STATE_COL in df.columns:
        df = df[df[STORE_STATE_COL].astype(str) == _lab_state]
    if _lab_city != "All" and STORE_CITY_COL and STORE_CITY_COL in df.columns:
        df = df[df[STORE_CITY_COL].astype(str) == _lab_city]

    if df.empty:
        st.warning("No data matches current filters."); return

    # ── KPI row
    pcts = {c: compliance_pct(df[c]) for c in lab_avail}
    overall = round(np.mean(list(pcts.values())), 1)

    cols = st.columns(len(lab_avail) + 1)
    for i, c in enumerate(lab_avail):
        ac = P["green"] if pcts[c] >= 80 else (P["amber"] if pcts[c] >= 60 else P["red"])
        with cols[i]:
            st.markdown(kpi("🏭", f"{pcts[c]}%", c, ac), unsafe_allow_html=True)
    with cols[-1]:
        st.markdown(kpi("📊", f"{overall}%", "Overall Labour", P["primary"]), unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Charts row
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        data = []
        for c in lab_avail:
            dn, pe, na = compliance_counts(df[c])
            data.append({"Type": c, "Done": dn, "Pending": pe})
        ldf = pd.DataFrame(data)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=ldf["Type"], y=ldf["Done"], name="Done",
                             marker_color=P["green"],
                             hovertemplate="<b>%{x}</b><br>Done: <b>%{y}</b><extra></extra>"))
        fig.add_trace(go.Bar(x=ldf["Type"], y=ldf["Pending"], name="Pending",
                             marker_color=P["red"],
                             hovertemplate="<b>%{x}</b><br>Pending: <b>%{y}</b><extra></extra>"))
        fig.update_layout(barmode="stack", legend=dict(orientation="h", y=1.1, x=0))
        st.plotly_chart(chart_layout(fig, 300, "📊 Labour Compliance Status (Store-wise)"),
                        use_container_width=True, config={"displayModeBar": False}, key="lab_stack")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig2 = go.Figure(go.Bar(
            x=list(pcts.keys()), y=list(pcts.values()),
            marker=dict(color=list(pcts.values()),
                        colorscale=[[0, P["red"]], [0.6, P["amber"]], [1, P["green"]]],
                        cmin=0, cmax=100),
            text=[f"{v}%" for v in pcts.values()], textposition="outside",
            textfont=dict(color="#CBD5E1"),
            hovertemplate="<b>%{x}</b><br>Completion: <b>%{y}%</b><extra></extra>",
        ))
        fig2.update_layout(yaxis=dict(range=[0, 115]))
        st.plotly_chart(chart_layout(fig2, 300, "✅ Completion % by Type"),
                        use_container_width=True, config={"displayModeBar": False}, key="lab_pct")
        st.markdown('</div>', unsafe_allow_html=True)

    # ── State-wise heatmap (store mode) or Department heatmap (employee mode)
    group_col   = STORE_STATE_COL if is_store_mode else ("Department" if "Department" in df.columns else None)
    group_label = "State" if is_store_mode else "Department"

    if group_col:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        rows = []
        for g in sorted(df[group_col].dropna().unique()):
            sub = df[df[group_col] == g]
            row = {group_label: g}
            for c in lab_avail:
                row[c] = compliance_pct(sub[c])
            row["Overall %"] = round(np.mean([row[c] for c in lab_avail]), 1)
            rows.append(row)
        ddf2 = pd.DataFrame(rows)
        fig3 = px.imshow(
            ddf2.set_index(group_label)[lab_avail].T,
            color_continuous_scale=[[0, "#14162B"], [0.4, P["red"]], [0.7, P["amber"]], [1, P["green"]]],
            zmin=0, zmax=100, text_auto=True,
        )
        fig3.update_traces(
            textfont=dict(color="#E2E8F0"),
            hovertemplate="<b>%{x}</b><br>%{y}: <b>%{z}%</b><extra></extra>",
        )
        st.plotly_chart(chart_layout(fig3, 300, f"🗺️ Labour Compliance Heatmap by {group_label}"),
                        use_container_width=True, config={"displayModeBar": False}, key="lab_heat")
        st.dataframe(ddf2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ── Pending stores table
    sec("⏳", "Pending Labour Compliance by Store" if is_store_mode else "Pending Labour Compliance")
    pend = []
    for _, row in df.iterrows():
        missing = [c for c in lab_avail if str(row.get(c, "")).strip().upper() != "DONE"]
        if missing:
            if is_store_mode:
                pend.append({
                    "State":         row.get(STORE_STATE_COL, ""),
                    "City / Store":  row.get(STORE_CITY_COL, ""),
                    "Pending Items": ", ".join(missing),
                    "Count":         len(missing),
                })
            else:
                pend.append({
                    "State":         row.get("State", ""),
                    "City / Store":  row.get("City / Store Location", row.get("Location", "")),
                    "Pending Items": ", ".join(missing),
                    "Count":         len(missing),
                })
    pdf = pd.DataFrame(pend)
    if len(pdf) > 0:
        st.dataframe(pdf.sort_values("Count", ascending=False), use_container_width=True, height=350)
        fname = "labour_pending_stores.xlsx" if is_store_mode else "labour_pending.xlsx"
        st.download_button("⬇️ Download Pending Stores", to_excel(pdf), fname,
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.success("🎉 All stores have completed labour compliance!")


# ── Pending Documents ──────────────────────────────────────────────────────────
def page_pending():
    st.markdown('<p class="page-title">❗ Pending Documents</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Employees with outstanding documentation</p>', unsafe_allow_html=True)

    all_tracked = [c for c in DOC_COLS+COMPLIANCE_COLS+LABOUR_COLS if c in df.columns]
    if not all_tracked:
        st.warning("No tracked columns found."); return

    rows = []
    for _, row in df.iterrows():
        missing = [c for c in all_tracked if str(row.get(c,"")).strip()==""]
        if missing:
            rows.append({
                "Emp Code": row.get("Emp Code",""),
                "Employee Name": row.get("Employee Name",""),
                "Department": row.get("Department",""),
                STATUS_COL: row.get(STATUS_COL,""),
                "Missing Documents": ", ".join(missing),
                "Pending Count": len(missing)
            })
    pdf = pd.DataFrame(rows)

    c1,c2,c3 = st.columns(3)
    with c1: st.markdown(kpi("❗", len(pdf),                                              "Employees w/ Pending",  P["red"]),     unsafe_allow_html=True)
    with c2: st.markdown(kpi("📋", int(pdf["Pending Count"].sum()) if len(pdf)>0 else 0,  "Total Pending Items",   P["amber"]),   unsafe_allow_html=True)
    with c3: st.markdown(kpi("✅", len(df)-len(pdf),                                      "Fully Compliant",       P["green"]),   unsafe_allow_html=True)

    if len(pdf) == 0:
        st.success("🎉 All documents are complete for all employees in current view!"); return

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    col_a,col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if "Department" in pdf.columns:
            dg = pdf.groupby("Department")["Pending Count"].sum().reset_index()
            fig = go.Figure(go.Bar(
                x=dg["Pending Count"], y=dg["Department"], orientation="h",
                marker=dict(color=dg["Pending Count"],
                            colorscale=[[0,P["amber"]],[1,P["red"]]], showscale=False),
                text=dg["Pending Count"], textposition="outside",
                hovertemplate="<b>%{y}</b><br>Pending: <b>%{x}</b><extra></extra>",
            ))
            st.plotly_chart(chart_layout(fig, 320, "🏢 Pending by Department"),
                            use_container_width=True, config={"displayModeBar":False}, key="pend_dept")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        doc_freq = {}
        for _, row in pdf.iterrows():
            for d in str(row["Missing Documents"]).split(", "):
                if d: doc_freq[d] = doc_freq.get(d, 0) + 1
        if doc_freq:
            dff = pd.DataFrame(list(doc_freq.items()), columns=["Document","Count"])
            dff = dff.sort_values("Count", ascending=True)
            fig2 = go.Figure(go.Bar(
                x=dff["Count"], y=dff["Document"], orientation="h",
                marker=dict(color=P["red"], opacity=0.8),
                text=dff["Count"], textposition="outside",
                hovertemplate="<b>%{y}</b><br>Missing for: <b>%{x}</b> employees<extra></extra>",
            ))
            st.plotly_chart(chart_layout(fig2, 320, "📋 Most Frequently Pending Documents"),
                            use_container_width=True, config={"displayModeBar":False}, key="pend_freq")
        st.markdown('</div>', unsafe_allow_html=True)

    sec("📋", "Employee-wise Pending List")
    f_dept_p = st.selectbox(
        "Filter Department",
        ["All"] + sorted(pdf["Department"].unique().tolist()) if "Department" in pdf.columns else ["All"],
        key="pend_dept_f"
    )
    show_pdf = pdf[pdf["Department"]==f_dept_p] if f_dept_p!="All" else pdf
    st.dataframe(show_pdf.sort_values("Pending Count", ascending=False), use_container_width=True, height=400)
    c1,c2 = st.columns(2)
    with c1: st.download_button("⬇️ Excel", to_excel(show_pdf), "pending_docs.xlsx",
                                  "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    with c2: st.download_button("⬇️ CSV", show_pdf.to_csv(index=False).encode(), "pending_docs.csv","text/csv")


# ── Reports ────────────────────────────────────────────────────────────────────
def page_reports():
    st.markdown('<p class="page-title">📊 Reports & Exports</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Export filtered data in various formats</p>', unsafe_allow_html=True)

    tab1,tab2,tab3,tab4 = st.tabs(["📋 Full Dataset","⚖️ Compliance","📑 Documentation","💰 Payroll"])

    with tab1:
        st.markdown(f"**{len(df)} employee records** in current filtered view")
        st.dataframe(df, use_container_width=True, height=420)
        c1,c2 = st.columns(2)
        with c1: st.download_button("⬇️ Excel", to_excel(df), "hr_full_data.xlsx",
                                     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        with c2: st.download_button("⬇️ CSV", df.to_csv(index=False).encode(), "hr_full_data.csv","text/csv")

    with tab2:
        comp_avail = [c for c in COMPLIANCE_COLS+LABOUR_COLS if c in df.columns]
        if comp_avail and "Department" in df.columns:
            rows = []
            for d in sorted(df["Department"].unique()):
                sub = df[df["Department"]==d]
                row = {"Department":d, "Employees":len(sub)}
                for c in comp_avail:
                    dn,pe,na = compliance_counts(sub[c])
                    row[f"{c} Done"]=dn; row[f"{c} Pending"]=pe; row[f"{c} %"]=compliance_pct(sub[c])
                row["Overall %"] = round(np.mean([compliance_pct(sub[c]) for c in comp_avail]),1)
                rows.append(row)
            cdf = pd.DataFrame(rows)
            st.dataframe(cdf, use_container_width=True)
            st.download_button("⬇️ Compliance Report", to_excel(cdf), "compliance_report.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    with tab3:
        doc_avail = [c for c in DOC_COLS if c in df.columns]
        if doc_avail:
            rows = []
            for c in doc_avail:
                dn,pe,na = compliance_counts(df[c])
                tot = dn+pe
                rows.append({"Document":c, "Done":dn, "Pending":pe, "N/A":na,
                             "Completion %": round(dn/tot*100,1) if tot>0 else 0})
            ddf2 = pd.DataFrame(rows)
            st.dataframe(ddf2, use_container_width=True)
            st.download_button("⬇️ Doc Report", to_excel(ddf2), "documentation_report.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    with tab4:
        pay_cols = ["Emp Code","Employee Name","Department","DOJ","New Joining","Resign","F&F",STATUS_COL]
        pay_df = df[[c for c in pay_cols if c in df.columns]]
        st.dataframe(pay_df, use_container_width=True, height=400)
        st.download_button("⬇️ Payroll Report", to_excel(pay_df), "payroll_report.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


# ── Settings ───────────────────────────────────────────────────────────────────
def page_settings():
    st.markdown('<p class="page-title">⚙️ Settings</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Configure data source and view system information</p>', unsafe_allow_html=True)

    tab1,tab2 = st.tabs(["📁 Data Source","ℹ️ About"])
    with tab1:
        st.markdown("### Upload Master Excel File")
        st.markdown('<div class="upload-box"><p style="color:#A855F7;font-weight:700;font-size:14px">📂 Upload HR Master Excel (.xlsx / .xls / .csv)</p><p style="font-size:12px;color:#7B2FF7">All metrics update automatically on upload</p></div>', unsafe_allow_html=True)
        nf = st.file_uploader("Choose file", type=["xlsx","xls","csv"], label_visibility="collapsed")
        if nf:
            st.session_state.uploaded_file = nf
            load_data.clear()
            st.success(f"✅ {nf.name} loaded! Navigate to Dashboard to see updated metrics.")

        st.markdown("### Current Dataset Info")
        if not df.empty:
            info = pd.DataFrame({"Property":["Total Records","Columns","Departments","Locations","Recruiters","Date Range"],
                                 "Value":[
                                     len(raw_df), len(raw_df.columns),
                                     raw_df["Department"].nunique() if "Department" in raw_df.columns else "—",
                                     raw_df["Location"].nunique() if "Location" in raw_df.columns else "—",
                                     raw_df["Recruiter Name"].nunique() if "Recruiter Name" in raw_df.columns else "—",
                                     f"{raw_df['DOJ'].min().date()} → {raw_df['DOJ'].max().date()}" if "DOJ" in raw_df.columns and raw_df["DOJ"].notna().any() else "—"
                                 ]})
            st.dataframe(info, use_container_width=True, hide_index=True)

        st.markdown("### Column Reference Guide")
        ref = pd.DataFrame({
            "Category":["Payroll"]*3+["Compliance"]*4+["Labour"]*3+["Documentation"]*5+["Recruitment"]*4,
            "Column":PAYROLL_COLS+COMPLIANCE_COLS+LABOUR_COLS+DOC_COLS+["Location","Profile Position","Recruiter Name","Profile Source"],
            "Expected Values":["DONE / blank"]*15+["Any text"]*4
        })
        st.dataframe(ref, use_container_width=True, hide_index=True)

    with tab2:
        st.markdown(f"""
        <div style='background:linear-gradient(135deg,#14162B,#1E1040);border-radius:16px;padding:28px;border:1px solid rgba(123,47,247,0.3);box-shadow:0 8px 30px rgba(0,0,0,0.4)'>
            <div style='display:flex;align-items:center;gap:16px;margin-bottom:24px'>
                <div>{LOGO_HTML}</div>
                <div>
                    <div style='font-size:20px;font-weight:900;color:#F1F5F9'>Purple United Sales Limited</div>
                    <div style='font-size:13px;color:#A855F7;font-weight:600;margin-top:4px'>HR Analytics Dashboard — Premium Edition</div>
                </div>
            </div>
            <div style='display:grid;grid-template-columns:1fr 1fr;gap:12px;font-size:13px;color:#94A3B8'>
                <div><b style='color:#C4B5FD'>Built with:</b> Python · Streamlit · Plotly</div>
                <div><b style='color:#C4B5FD'>Data:</b> Single Excel / CSV master file</div>
                <div><b style='color:#C4B5FD'>Status Logic:</b> DONE / Blank / N/A</div>
                <div><b style='color:#C4B5FD'>Compliance:</b> DONE ÷ (DONE + Blank)</div>
                <div><b style='color:#C4B5FD'>Filters:</b> Year · Month · Recruiter · Location</div>
                <div><b style='color:#C4B5FD'>Theme:</b> Royal Purple #7B2FF7</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


# ── HRIS Page ──────────────────────────────────────────────────────────────────
def page_hris():
    st.markdown('<p class="page-title">📑 HRIS</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">Employee document verification · Appointment Letters · KYC tracking</p>', unsafe_allow_html=True)

    raw = section_file_uploader("hris", "HRIS", BASE_RAW_DF, apply_filters=False)

    # Fuzzy column detection
    def _find_col(df_cols, keywords):
        for c in df_cols:
            cl = str(c).strip().lower()
            for kw in keywords:
                if kw in cl:
                    return c
        return None

    _hris_date_col = _find_col(raw.columns, ["date of joining", "doj", "joining date", "date of join"])
    _pan_col = _find_col(raw.columns, ["pan"])
    _aadhar_col = _find_col(raw.columns, ["aadhar", "aadhaar", "aadhar card", "aadhaar card"])
    _bank_col = _find_col(raw.columns, ["bank"])
    _appt_col = _find_col(raw.columns, ["appointment", "appt"])

    if _hris_date_col and _hris_date_col in raw.columns:
        raw[_hris_date_col] = pd.to_datetime(raw[_hris_date_col], errors="coerce")

    # ── HRIS Filters (4 max)
    st.markdown('<div class="filter-panel"><div class="filter-header"><div class="filter-dot"></div><span class="filter-title-text">🔍 HRIS Filters</span></div></div>', unsafe_allow_html=True)
    hf1, hf2, hf3, hf4 = st.columns(4)
    with hf1:
        _yr_opts = ["All"] + sorted(raw[_hris_date_col].dropna().dt.year.astype(int).unique().tolist(), reverse=True) if _hris_date_col and raw[_hris_date_col].notna().any() else ["All"]
        _hris_yr = st.selectbox("📅 Year", _yr_opts, key="hris_year")
    with hf2:
        _mn = ["All","January","February","March","April","May","June","July","August","September","October","November","December"]
        _hris_mo = st.selectbox("🗓️ Month", _mn, key="hris_month")
    with hf3:
        _emp_opts = ["All"] + sorted(str(e) for e in raw["Employee Name"].unique() if str(e).strip() and str(e) != "nan") if "Employee Name" in raw.columns else ["All"]
        _hris_emp = st.selectbox("👤 Employee Name", _emp_opts, key="hris_emp")
    with hf4:
        _dept_opts = ["All"] + sorted(str(d) for d in raw["Department"].unique() if str(d).strip() and str(d) != "nan") if "Department" in raw.columns else ["All"]
        _hris_dept = st.selectbox("🏢 Department", _dept_opts, key="hris_dept")

    hdf = raw.copy()
    if _hris_yr != "All" and _hris_date_col:
        hdf = hdf[hdf[_hris_date_col].dt.year == int(_hris_yr)]
    if _hris_mo != "All" and _hris_date_col:
        hdf = hdf[hdf[_hris_date_col].dt.month == _mn.index(_hris_mo)]
    if _hris_emp != "All" and "Employee Name" in hdf.columns:
        hdf = hdf[hdf["Employee Name"].astype(str) == _hris_emp]
    if _hris_dept != "All" and "Department" in hdf.columns:
        hdf = hdf[hdf["Department"].astype(str) == _hris_dept]

    if hdf.empty:
        st.warning("No data matches current filters."); return

    def hris_pct(col_name):
        if col_name in hdf.columns:
            s = hdf[col_name].astype(str).str.strip().str.upper()
            done = (s == "DONE").sum()
            total = ((s == "DONE") | (s == "") | (s == "NOT DONE")).sum()
            return round(done / total * 100, 1) if total > 0 else 0.0
        return 0.0

    appt_pct = hris_pct(_appt_col) if _appt_col else 0.0
    pan_pct = hris_pct(_pan_col) if _pan_col else 0.0
    aadhar_pct = hris_pct(_aadhar_col) if _aadhar_col else 0.0
    bank_pct = hris_pct(_bank_col) if _bank_col else 0.0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        ac = P["green"] if appt_pct >= 80 else (P["amber"] if appt_pct >= 60 else P["red"])
        st.markdown(kpi("📄", f"{appt_pct}%", "Appointment Letter", ac), unsafe_allow_html=True)
    with c2:
        ac = P["green"] if pan_pct >= 80 else (P["amber"] if pan_pct >= 60 else P["red"])
        st.markdown(kpi("🆔", f"{pan_pct}%", "PAN", ac), unsafe_allow_html=True)
    with c3:
        ac = P["green"] if aadhar_pct >= 80 else (P["amber"] if aadhar_pct >= 60 else P["red"])
        st.markdown(kpi("🆔", f"{aadhar_pct}%", "Aadhar", ac), unsafe_allow_html=True)
    with c4:
        ac = P["green"] if bank_pct >= 80 else (P["amber"] if bank_pct >= 60 else P["red"])
        st.markdown(kpi("🏦", f"{bank_pct}%", "Bank", ac), unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Charts
    hris_cols = [c for c in [_appt_col, _pan_col, _aadhar_col, _bank_col, "PF Form", "ESIC Form", "BGV"] if c and c in hdf.columns]
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        data = []
        for c in hris_cols:
            dn, pe, na = compliance_counts(hdf[c])
            data.append({"Document": c, "Done": dn, "Pending": pe})
        ddf2 = pd.DataFrame(data)
        fig = go.Figure()
        fig.add_trace(go.Bar(x=ddf2["Document"], y=ddf2["Done"], name="Done",
                             marker_color=P["green"],
                             hovertemplate="<b>%{x}</b><br>Done: <b>%{y}</b><extra></extra>"))
        fig.add_trace(go.Bar(x=ddf2["Document"], y=ddf2["Pending"], name="Pending",
                             marker_color=P["red"],
                             hovertemplate="<b>%{x}</b><br>Pending: <b>%{y}</b><extra></extra>"))
        fig.update_layout(barmode="stack", xaxis=dict(tickangle=-20),
                          legend=dict(orientation="h", y=1.1, x=0))
        st.plotly_chart(chart_layout(fig, 320, "📊 HRIS Document Status"),
                        use_container_width=True, config={"displayModeBar":False}, key="hris_stack")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        pcts = []
        for c in hris_cols:
            dn, pe, _ = compliance_counts(hdf[c])
            tot = dn + pe
            pcts.append(round(dn/tot*100, 1) if tot > 0 else 0)
        fig2 = go.Figure(go.Bar(
            x=hris_cols, y=pcts,
            marker=dict(color=pcts, colorscale=[[0,P["red"]],[0.6,P["amber"]],[1,P["green"]]], cmin=0, cmax=100),
            text=[f"{p}%" for p in pcts], textposition="outside",
            textfont=dict(color="#CBD5E1"),
            hovertemplate="<b>%{x}</b><br>Completion: <b>%{y}%</b><extra></extra>",
        ))
        fig2.update_layout(xaxis=dict(tickangle=-20), yaxis=dict(range=[0, 115]))
        st.plotly_chart(chart_layout(fig2, 320, "✅ Completion % per Document"),
                        use_container_width=True, config={"displayModeBar":False}, key="hris_pct")
        st.markdown('</div>', unsafe_allow_html=True)

    # Pending employees table
    sec("⏳", "Pending HRIS Documents by Employee")
    pend_rows = []
    for _, row in hdf.iterrows():
        missing = [c for c in hris_cols if str(row.get(c, "")).strip() == ""]
        if missing:
            pend_rows.append({"Emp Code": row.get("Emp Code", ""),
                              "Employee Name": row.get("Employee Name", ""),
                              "Department": row.get("Department", ""),
                              "Pending": ", ".join(missing), "Count": len(missing)})
    pdf = pd.DataFrame(pend_rows)
    if len(pdf) > 0:
        st.markdown(f"**{len(pdf)} employees** have pending HRIS documents")
        st.dataframe(pdf.sort_values("Count", ascending=False), use_container_width=True, height=350)
        st.download_button("⬇️ Download", to_excel(pdf), "hris_pending.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.success("🎉 All HRIS documents are complete for current filters!")


# ── Payroll Compliance Page ────────────────────────────────────────────────────
def page_payroll_compliance():
    st.markdown('<p class="page-title">⚖️ Payroll Compliance</p>', unsafe_allow_html=True)
    st.markdown('<p class="page-sub">PF · ESIC · PT · LWF compliance status</p>', unsafe_allow_html=True)

    raw = section_file_uploader("payroll_compliance", "Payroll Compliance", BASE_RAW_DF, apply_filters=False)

    # ── Payroll Compliance Filters (4 max)
    st.markdown('<div class="filter-panel"><div class="filter-header"><div class="filter-dot"></div><span class="filter-title-text">🔍 Payroll Compliance Filters</span></div></div>', unsafe_allow_html=True)
    pf1, pf2, pf3, pf4 = st.columns(4)
    with pf1:
        _yr_opts = ["All"] + sorted(raw["DOJ"].dropna().dt.year.astype(int).unique().tolist(), reverse=True) if "DOJ" in raw.columns and raw["DOJ"].notna().any() else ["All"]
        _pc_yr = st.selectbox("📅 Year", _yr_opts, key="pc_year")
    with pf2:
        _mn = ["All","January","February","March","April","May","June","July","August","September","October","November","December"]
        _pc_mo = st.selectbox("🗓️ Month", _mn, key="pc_month")
    with pf3:
        _dept_opts = ["All"] + sorted(str(d) for d in raw["Department"].unique() if str(d).strip() and str(d) != "nan") if "Department" in raw.columns else ["All"]
        _pc_dept = st.selectbox("🏢 Department", _dept_opts, key="pc_dept")
    with pf4:
        _loc_opts = ["All"] + sorted(str(l) for l in raw["Location"].unique() if str(l).strip() and str(l) != "nan") if "Location" in raw.columns else ["All"]
        _pc_loc = st.selectbox("📍 Location", _loc_opts, key="pc_loc")

    pcdf = raw.copy()
    if _pc_yr != "All" and "DOJ" in pcdf.columns:
        pcdf = pcdf[pcdf["DOJ"].dt.year == int(_pc_yr)]
    if _pc_mo != "All" and "DOJ" in pcdf.columns:
        pcdf = pcdf[pcdf["DOJ"].dt.month == _mn.index(_pc_mo)]
    if _pc_dept != "All" and "Department" in pcdf.columns:
        pcdf = pcdf[pcdf["Department"].astype(str) == _pc_dept]
    if _pc_loc != "All" and "Location" in pcdf.columns:
        pcdf = pcdf[pcdf["Location"].astype(str) == _pc_loc]

    if pcdf.empty:
        st.warning("No data matches current filters."); return

    comp_avail = [c for c in COMPLIANCE_COLS if c in pcdf.columns]
    if not comp_avail:
        st.warning("No compliance columns (PF, ESIC, PT, LWF) found."); return

    # KPIs: percentage of DONE for each compliance column
    pcts = {c: compliance_pct(pcdf[c]) for c in comp_avail}
    overall = round(np.mean(list(pcts.values())), 1)

    cols = st.columns(len(comp_avail) + 1)
    for i, c in enumerate(comp_avail):
        ac = P["green"] if pcts[c] >= 80 else (P["amber"] if pcts[c] >= 60 else P["red"])
        with cols[i]:
            st.markdown(kpi("📋", f"{pcts[c]}%", c, ac), unsafe_allow_html=True)
    with cols[-1]:
        ac = P["green"] if overall >= 80 else (P["amber"] if overall >= 60 else P["red"])
        st.markdown(kpi("⚖️", f"{overall}%", "Overall Compliance", ac), unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Charts
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=overall,
            title={"text":"Overall Compliance %","font":{"color":"#E2E8F0","size":13}},
            number={"font":{"color":"#F1F5F9","size":40},"suffix":"%"},
            gauge={
                "axis":{"range":[0,100],"tickfont":{"color":CHART_TEXT}},
                "bar":{"color":P["primary"],"thickness":0.8},
                "bgcolor":CHART_BG,
                "bordercolor":"rgba(123,47,247,0.3)",
                "steps":[{"range":[0,60],"color":"rgba(239,68,68,0.15)"},
                          {"range":[60,80],"color":"rgba(245,158,11,0.15)"},
                          {"range":[80,100],"color":"rgba(16,185,129,0.15)"}],
                "threshold":{"line":{"color":P["accent"],"width":3},"thickness":0.8,"value":80},
            }
        ))
        st.plotly_chart(chart_layout(fig, 300, ""), use_container_width=True,
                        config={"displayModeBar":False}, key="pc_gauge")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        bars = []
        for c in comp_avail:
            dn, pe, na = compliance_counts(pcdf[c])
            bars.append({"Type": c, "Done": dn, "Pending": pe, "N/A": na})
        bdf = pd.DataFrame(bars)
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(x=bdf["Type"], y=bdf["Done"], name="Done",
                              marker_color=P["green"],
                              hovertemplate="<b>%{x}</b><br>Done: <b>%{y}</b><extra></extra>"))
        fig2.add_trace(go.Bar(x=bdf["Type"], y=bdf["Pending"], name="Pending",
                              marker_color=P["red"],
                              hovertemplate="<b>%{x}</b><br>Pending: <b>%{y}</b><extra></extra>"))
        fig2.update_layout(barmode="stack", legend=dict(orientation="h", y=1.1, x=0))
        st.plotly_chart(chart_layout(fig2, 300, "📊 Compliance Status Breakdown"),
                        use_container_width=True, config={"displayModeBar":False}, key="pc_stack")
        st.markdown('</div>', unsafe_allow_html=True)

    # Department-wise breakdown
    if "Department" in pcdf.columns:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        dept_rows = []
        for d in sorted(pcdf["Department"].unique()):
            sub = pcdf[pcdf["Department"] == d]
            row = {"Department": d}
            for c in comp_avail:
                row[c] = compliance_pct(sub[c])
            row["Overall %"] = round(np.mean([row[c] for c in comp_avail]), 1)
            dept_rows.append(row)
        ddf2 = pd.DataFrame(dept_rows)
        fig3 = go.Figure()
        for i, c in enumerate(comp_avail):
            fig3.add_trace(go.Bar(x=ddf2["Department"], y=ddf2[c], name=c,
                                  marker_color=PALETTE[i],
                                  hovertemplate=f"<b>%{{x}}</b><br>{c}: <b>%{{y}}%</b><extra></extra>"))
        fig3.add_hline(y=80, line_dash="dash", line_color=P["accent"], opacity=0.7,
                       annotation_text="80% target", annotation_font_color=P["accent"])
        fig3.update_layout(barmode="group", legend=dict(orientation="h", y=1.1, x=0))
        st.plotly_chart(chart_layout(fig3, 300, "🏢 Department-wise Compliance %"),
                        use_container_width=True, config={"displayModeBar":False}, key="pc_dept")
        st.dataframe(ddf2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # Pending table
    sec("⏳", "Pending Compliance by Employee")
    pend_rows = []
    for _, row in pcdf.iterrows():
        missing = [c for c in comp_avail if str(row.get(c, "")).strip() == ""]
        if missing:
            pend_rows.append({"Emp Code": row.get("Emp Code", ""),
                              "Employee Name": row.get("Employee Name", ""),
                              "Department": row.get("Department", ""),
                              "Pending": ", ".join(missing), "Count": len(missing)})
    pdf = pd.DataFrame(pend_rows)
    if len(pdf) > 0:
        st.markdown(f"**{len(pdf)} employees** have pending compliance items")
        st.dataframe(pdf.sort_values("Count", ascending=False), use_container_width=True, height=350)
        st.download_button("⬇️ Download", to_excel(pdf), "payroll_compliance_pending.xlsx",
                           "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.success("🎉 All compliance items are complete for current filters!")


# ── ROUTER ─────────────────────────────────────────────────────────────────────
page = st.session_state.page
try:
    if   page == "Dashboard":          page_dashboard()
    elif page == "HRIS":               page_hris()
    elif page == "HR Documentation":   page_documentation()
    elif page == "Payroll":            page_payroll()
    elif page == "Payroll Compliance": page_payroll_compliance()
    elif page == "Compliance":         page_compliance()
    elif page == "Labour Compliance":  page_labour()
    elif page == "Recruitment":        page_recruitment()
    elif page == "Pending Documents":  page_pending()
    elif page == "Reports":            page_reports()
    elif page == "Settings":           page_settings()
    else:                              page_dashboard()
except Exception as e:
    st.error(f"⚠️ Error on page '{page}': {e}")
    import traceback
    st.code(traceback.format_exc())
