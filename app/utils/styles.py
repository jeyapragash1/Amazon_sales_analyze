# Shared CSS, color palette, and chart layout constants
# Imported by app.py and all pages/*.py

COLORS   = ["#6C63FF","#48CAE4","#a78bfa","#f472b6","#34d399","#fb923c","#facc15","#60a5fa"]
BG_CHART = "rgba(0,0,0,0)"
FONT_CLR = "#c8c8ff"
GRID_CLR = "rgba(108,99,255,0.1)"

LAYOUT_BASE = dict(
    paper_bgcolor = BG_CHART,
    plot_bgcolor  = BG_CHART,
    font          = dict(family="Inter", color=FONT_CLR, size=12),
    margin        = dict(l=16, r=16, t=50, b=16),
    hoverlabel    = dict(bgcolor="#1e1e3a", font_color="#e0e0ff",
                         bordercolor="rgba(108,99,255,0.5)"),
    legend        = dict(bgcolor="rgba(0,0,0,0)", font=dict(color="#a0a0c0")),
)

AXIS_STYLE = dict(
    gridcolor  = GRID_CLR,
    linecolor  = "rgba(255,255,255,0.08)",
    tickfont   = dict(color="#8888aa"),
)

SEG_COLORS = {
    "Champions": "#6C63FF",
    "Active":    "#48CAE4",
    "New/Cold":  "#f472b6",
}


def make_layout(**overrides):
    """Return a copy of LAYOUT_BASE merged with any overrides (avoids duplicate-kwarg errors)."""
    return {**LAYOUT_BASE, **overrides}


def get_css() -> str:
    return """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header { visibility: hidden; }

.stApp {
    background: linear-gradient(135deg, #0a0a1a 0%, #0d0d2b 50%, #0a1628 100%);
    min-height: 100vh;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0f23 0%, #1a1a3e 100%) !important;
    border-right: 1px solid rgba(108,99,255,0.3);
}

/* Hero */
.hero-wrap {
    background: linear-gradient(135deg, rgba(108,99,255,0.15) 0%, rgba(72,202,228,0.1) 100%);
    border: 1px solid rgba(108,99,255,0.3);
    border-radius: 20px;
    padding: 32px 40px 24px 40px;
    margin-bottom: 26px;
    position: relative;
    overflow: hidden;
}
.hero-wrap::before {
    content:''; position:absolute; top:-60px; right:-60px;
    width:220px; height:220px;
    background: radial-gradient(circle, rgba(108,99,255,0.25) 0%, transparent 70%);
    border-radius:50%;
}
.hero-wrap::after {
    content:''; position:absolute; bottom:-40px; left:-40px;
    width:160px; height:160px;
    background: radial-gradient(circle, rgba(72,202,228,0.2) 0%, transparent 70%);
    border-radius:50%;
}
.hero-title {
    font-size: 2.4rem; font-weight: 800;
    background: linear-gradient(90deg, #6C63FF 0%, #48CAE4 50%, #a78bfa 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    background-clip: text; margin: 0; line-height: 1.1;
}
.hero-sub  { font-size:0.96rem; color:#7878aa; margin-top:6px; }
.hero-badge {
    display:inline-block;
    background:rgba(108,99,255,0.2); border:1px solid rgba(108,99,255,0.5);
    border-radius:20px; padding:3px 14px; font-size:0.7rem;
    color:#a78bfa; margin-top:10px; letter-spacing:0.06em; text-transform:uppercase;
}

/* KPI cards */
div[data-testid="metric-container"] {
    background: linear-gradient(145deg,rgba(255,255,255,0.06),rgba(255,255,255,0.02));
    backdrop-filter:blur(10px);
    border:1px solid rgba(108,99,255,0.25); border-radius:16px;
    padding:20px 22px !important;
    transition: transform .2s, border-color .2s, box-shadow .2s;
    box-shadow: 0 4px 24px rgba(0,0,0,0.3);
}
div[data-testid="metric-container"]:hover {
    transform:translateY(-3px);
    border-color:rgba(108,99,255,0.6);
    box-shadow:0 8px 32px rgba(108,99,255,0.2);
}
div[data-testid="metric-container"] label {
    font-size:0.72rem!important; font-weight:600!important;
    letter-spacing:0.1em!important; text-transform:uppercase!important; color:#7878aa!important;
}
div[data-testid="metric-container"] [data-testid="stMetricValue"] {
    font-size:1.7rem!important; font-weight:800!important; color:#e8e8ff!important;
}

/* Section header */
.section-header { display:flex; align-items:center; gap:10px; margin:28px 0 14px 0; }
.section-title  { font-size:1.1rem; font-weight:700; color:#c8c8ff; margin:0; }
.section-line   { flex:1; height:1px;
                  background:linear-gradient(90deg,rgba(108,99,255,0.5) 0%,transparent 100%); }

/* Divider */
hr { border:none!important; border-top:1px solid rgba(108,99,255,0.15)!important; margin:24px 0!important; }

/* Charts */
[data-testid="stPlotlyChart"] { border-radius:16px; overflow:hidden; box-shadow:0 4px 24px rgba(0,0,0,0.3); }

/* DataFrames */
[data-testid="stDataFrame"] { border-radius:12px; overflow:hidden; border:1px solid rgba(108,99,255,0.2)!important; }

/* Tabs */
[data-testid="stTabs"] [role="tab"] { color:#7878aa; font-weight:600; }
[data-testid="stTabs"] [role="tab"][aria-selected="true"] { color:#6C63FF; border-bottom:2px solid #6C63FF; }

/* Download button */
[data-testid="stDownloadButton"] button {
    background:linear-gradient(90deg,#6C63FF 0%,#48CAE4 100%)!important;
    color:white!important; border:none!important; border-radius:10px!important;
    font-weight:600!important; padding:10px 24px!important; width:100%;
}
[data-testid="stDownloadButton"] button:hover { opacity:0.88; }

/* Alerts */
[data-testid="stAlert"] { border-radius:12px!important; }

/* Caption */
[data-testid="stCaptionContainer"] p { color:#55557a!important; font-size:0.78rem!important; }

/* Footer */
.footer {
    text-align:center; padding:18px 0 8px 0;
    color:#44446a; font-size:0.78rem;
    border-top:1px solid rgba(108,99,255,0.1); margin-top:20px;
}
.footer span { color:#6C63FF; }
</style>
"""


def section(title: str) -> str:
    """Return a styled HTML section header."""
    return f"""
<div class="section-header">
  <div class="section-title">{title}</div>
  <div class="section-line"></div>
</div>"""


def sidebar_brand(subtitle: str = "") -> str:
    return f"""
<div style='text-align:center; padding:10px 0 20px 0;'>
  <div style='font-size:1.4rem; font-weight:800;
              background:linear-gradient(90deg,#6C63FF,#48CAE4);
              -webkit-background-clip:text; -webkit-text-fill-color:transparent;'>
    ⚙️ Filters
  </div>
  <div style='font-size:0.72rem; color:#55557a; margin-top:4px;'>{subtitle}</div>
</div>"""
