import os
import streamlit as st
import plotly.graph_objects as go
from utils.data_utils import load_orders, filter_df, compute_kpis
from utils.styles import get_css, section, sidebar_brand, make_layout, COLORS, FONT_CLR, GRID_CLR, AXIS_STYLE

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(page_title="Dashboard | Overview", page_icon="📊", layout="wide")
st.markdown(get_css(), unsafe_allow_html=True)

# ── Data Loading (Cached) ─────────────────────────────────────────────────────
DATA_PATH = os.environ.get("ORDERS_CSV", os.path.join(os.path.dirname(__file__), "..", "data", "orders.csv"))

@st.cache_data(show_spinner=False)
def load_data():
    return load_orders(DATA_PATH)

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading dataset: {e}")
    st.stop()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(sidebar_brand("High-level performance"), unsafe_allow_html=True)
    date_range = st.date_input("📅 Date Range", value=(df["order_date"].dt.date.min(), df["order_date"].dt.date.max()))
    countries  = st.multiselect("🌍 Countries",  sorted(df["country"].unique().tolist()))
    channels   = st.multiselect("📣 Channels",   sorted(df["channel"].unique().tolist()))
    categories = st.multiselect("🗂️ Categories", sorted(df["category"].unique().tolist()))
    
    st.markdown("---")
    # Feature 8: Sidebar Summary Stats
    fdf = filter_df(df, date_range, countries, channels, categories)
    st.markdown(f"""
    <div style='background:rgba(108,99,255,0.1); border-radius:10px; padding:12px; border:1px solid rgba(108,99,255,0.2)'>
      <div style='color:#7878aa; font-size:0.7rem; text-transform:uppercase;'>Current Filter</div>
      <div style='color:#c8c8ff; font-size:0.85rem; font-weight:700; margin-top:4px;'>
        {len(fdf):,} <span style='font-weight:400; color:#55557a;'>Orders</span><br>
        {fdf['customer_id'].nunique():,} <span style='font-weight:400; color:#55557a;'>Customers</span><br>
        {fdf['country'].nunique():,} <span style='font-weight:400; color:#55557a;'>Countries</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-title">📊 Executive Overview</div>
  <div class="hero-sub">Key Performance Indicators & Market Trends</div>
  <div class="hero-badge">Snapshot &nbsp;·&nbsp; {0} - {1}</div>
</div>
""".format(date_range[0] if len(date_range)>0 else "", date_range[1] if len(date_range)>1 else ""), unsafe_allow_html=True)

if fdf.empty:
    st.warning("⚠️ No records match the current filters.")
    st.stop()

# ── KPI Cards ────────────────────────────────────────────────────────────────
st.markdown(section("📌 Key Performance Indicators"), unsafe_allow_html=True)
kpis = compute_kpis(fdf)
cols = st.columns(6)
kpi_items = [
    ("💰 Revenue", f"${kpis['Revenue']:,.0f}"),
    ("📈 Profit", f"${kpis['Profit']:,.0f}"),
    ("🛒 Orders", f"{kpis['Orders']:,}"),
    ("👤 Customers", f"{kpis['Customers']:,}"),
    ("🎯 AOV", f"${kpis['AOV']:,.0f}"),
    ("📊 Margin", f"{kpis['Margin%']*100:.1f}%"),
]
for col, (label, val) in zip(cols, kpi_items):
    col.metric(label, val)

st.markdown("---")

# ── Trends ───────────────────────────────────────────────────────────────────
st.markdown(section("📅 Monthly Revenue & Profit Trends"), unsafe_allow_html=True)
ts = fdf.groupby("order_month").agg(revenue=("revenue","sum"), profit=("profit","sum")).reset_index().sort_values("order_month")

fig_ts = go.Figure()
fig_ts.add_trace(go.Scatter(x=ts["order_month"], y=ts["revenue"], mode="lines+markers", name="Revenue",
                            line=dict(color="#6C63FF", width=3), fill="tozeroy", fillcolor="rgba(108,99,255,0.05)"))
fig_ts.add_trace(go.Scatter(x=ts["order_month"], y=ts["profit"], mode="lines+markers", name="Profit", yaxis="y2",
                            line=dict(color="#48CAE4", width=3, dash="dot")))
fig_ts.update_layout(**make_layout(
    height=400, xaxis=AXIS_STYLE, yaxis={**AXIS_STYLE, "title": "Revenue ($)"},
    yaxis2=dict(title="Profit ($)", overlaying="y", side="right", gridcolor=GRID_CLR, tickfont=dict(color="#8888aa")),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
))
st.plotly_chart(fig_ts, use_container_width=True)

st.markdown("---")

# ── Categories & Channels ─────────────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.markdown(section("🗂️ Revenue by Category"), unsafe_allow_html=True)
    cat_rev = fdf.groupby("category")["revenue"].sum().sort_values(ascending=False).reset_index()
    fig_cat = go.Figure(go.Bar(x=cat_rev["category"], y=cat_rev["revenue"],
                               marker=dict(color=cat_rev["revenue"], colorscale="Blues")))
    fig_cat.update_layout(**make_layout(height=350, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE))
    st.plotly_chart(fig_cat, use_container_width=True)

with c2:
    st.markdown(section("📣 Channel Share"), unsafe_allow_html=True)
    ch = fdf.groupby("channel")["revenue"].sum().reset_index()
    fig_ch = go.Figure(go.Pie(labels=ch["channel"], values=ch["revenue"], hole=0.5,
                              marker=dict(colors=COLORS, line=dict(color="#0a0a1a", width=2))))
    fig_ch.update_layout(**make_layout(height=350, showlegend=True, legend=dict(orientation="h", y=-0.1)))
    st.plotly_chart(fig_ch, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Executive Overview &nbsp;·&nbsp; 📊 Data Storytelling Dashboard &nbsp;·&nbsp; <span>© 2026 Kisho Jeyapragash</span>
</div>
""", unsafe_allow_html=True)
