import os
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.data_utils import load_orders, filter_df, top_customers, rfm_segmentation, cohort_analysis, discount_analysis, orders_by_dayofweek
from utils.styles import get_css, section, sidebar_brand, make_layout, SEG_COLORS, AXIS_STYLE, FONT_CLR

st.set_page_config(page_title="Dashboard | Customers", page_icon="👤", layout="wide")
st.markdown(get_css(), unsafe_allow_html=True)

DATA_PATH = os.environ.get("ORDERS_CSV", os.path.join(os.path.dirname(__file__), "..", "..", "data", "orders.csv"))

@st.cache_data(show_spinner=False)
def load_data():
    return load_orders(DATA_PATH)

df = load_data()

with st.sidebar:
    st.markdown(sidebar_brand("Customer Insights"), unsafe_allow_html=True)
    date_range = st.date_input("📅 Date Range", value=(df["order_date"].dt.date.min(), df["order_date"].dt.date.max()))
    countries  = st.multiselect("🌍 Countries", sorted(df["country"].unique().tolist()))
    fdf = filter_df(df, date_range, countries)

st.markdown("""
<div class="hero-wrap">
  <div class="hero-title">👤 Customer Intelligence</div>
  <div class="hero-sub">Segmentation, Retention & Purchasing Behavior</div>
</div>
""", unsafe_allow_html=True)

if fdf.empty:
    st.warning("⚠️ No data for selected filters.")
    st.stop()

# ── Feature 3: Top Customers Table ───────────────────────────────────────────
st.markdown(section("🏆 Top 20 Customers by Revenue"), unsafe_allow_html=True)
top_c = top_customers(fdf, 20)
st.dataframe(top_c.style.background_gradient(subset=["Revenue"], cmap="Purples"), use_container_width=True)

st.markdown("---")

t1, t2 = st.columns(2)

# ── Feature 5: Day-of-Week Heatmap ─────────────────────────────────────────────
with t1:
    st.markdown(section("📅 Orders by Weekday"), unsafe_allow_html=True)
    dow = orders_by_dayofweek(fdf)
    if not dow.empty:
        fig_dow = px.imshow(dow, text_auto=True, color_continuous_scale="Purples", aspect="auto")
        fig_dow.update_layout(**make_layout(height=400, coloraxis_showscale=False))
        st.plotly_chart(fig_dow, use_container_width=True)
    else:
        st.info("Insufficient data for heatmap")

# ── Feature 6: Discount Impact Analysis ────────────────────────────────────────
with t2:
    st.markdown(section("🏷️ Discount vs Revenue"), unsafe_allow_html=True)
    disc = discount_analysis(fdf)
    fig_disc = px.scatter(disc, x="discount_pct", y="revenue", color="category", size="revenue",
                         hover_data=["order_id"], color_discrete_sequence=px.colors.qualitative.Vivid)
    fig_disc.update_layout(**make_layout(height=400, xaxis={**AXIS_STYLE, "title":"Discount %"}, yaxis={**AXIS_STYLE, "title":"Revenue ($)"}))
    st.plotly_chart(fig_disc, use_container_width=True)

st.markdown("---")

# ── RFM Segmentation ──────────────────────────────────────────────────────────
st.markdown(section("🎯 RFM Segmentation"), unsafe_allow_html=True)
rfm = rfm_segmentation(fdf)
if not rfm.empty:
    seg_counts = rfm["Segment"].value_counts().reset_index()
    seg_counts.columns = ["Segment", "Count"]
    
    sc1, sc2, sc3 = st.columns(3)
    for col, seg in zip([sc1, sc2, sc3], ["Champions", "Active", "New/Cold"]):
        cnt = seg_counts[seg_counts["Segment"]==seg]["Count"].values[0] if seg in seg_counts["Segment"].values else 0
        color = SEG_COLORS[seg]
        col.markdown(f"""
        <div style="background:rgba(255,255,255,0.03); border:1px solid {color}44; border-radius:12px; padding:15px; text-align:center;">
          <div style="color:#7878aa; font-size:0.7rem; text-transform:uppercase;">{seg}</div>
          <div style="color:{color}; font-size:1.8rem; font-weight:800;">{cnt:,}</div>
        </div>
        """, unsafe_allow_html=True)
        
    fig_rfm = go.Figure(go.Bar(x=seg_counts["Segment"], y=seg_counts["Count"], 
                              marker=dict(color=[SEG_COLORS.get(s, "#aaa") for s in seg_counts["Segment"]])))
    fig_rfm.update_layout(**make_layout(height=350, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE))
    st.plotly_chart(fig_rfm, use_container_width=True)

# ── Cohort Analysis ───────────────────────────────────────────────────────────
st.markdown(section("🔁 Retention (Cohort Analysis)"), unsafe_allow_html=True)
c_abs, c_ret = cohort_analysis(fdf)
if c_abs is not None:
    ct1, ct2 = st.tabs(["Absolute Counts", "Retention %"])
    with ct1: st.dataframe(c_abs.style.background_gradient(cmap="Blues"), use_container_width=True)
    with ct2: st.dataframe((c_ret*100).round(1).style.background_gradient(cmap="Greens"), use_container_width=True)
else:
    st.info("Insufficient data for cohort analysis")

st.markdown("""<div class="footer">Customer Intelligence &nbsp;·&nbsp; <span>© 2026 Kisho Jeyapragash</span></div>""", unsafe_allow_html=True)
