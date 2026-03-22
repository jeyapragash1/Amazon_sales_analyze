import os
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils.data_utils import load_orders, filter_df
from utils.styles import get_css, section, sidebar_brand, make_layout, AXIS_STYLE

st.set_page_config(page_title="Dashboard | Geography", page_icon="🌍", layout="wide")
st.markdown(get_css(), unsafe_allow_html=True)

DATA_PATH = os.environ.get("ORDERS_CSV", os.path.join(os.path.dirname(__file__), "..", "..", "data", "orders.csv"))

@st.cache_data(show_spinner=False)
def load_data():
    return load_orders(DATA_PATH)

df = load_data()

with st.sidebar:
    st.markdown(sidebar_brand("Global Sales"), unsafe_allow_html=True)
    date_range = st.date_input("📅 Date Range", value=(df["order_date"].dt.date.min(), df["order_date"].dt.date.max()))
    channels   = st.multiselect("📣 Channels", sorted(df["channel"].unique().tolist()))
    fdf = filter_df(df, date_range, channels=channels)

st.markdown("""
<div class="hero-wrap">
  <div class="hero-title">🌍 Geographical Intelligence</div>
  <div class="hero-sub">Global Sales Distribution & Market Penetration</div>
</div>
""", unsafe_allow_html=True)

if fdf.empty:
    st.warning("⚠️ No data for selected filters.")
    st.stop()

# ── Feature 2: Choropleth World Map ──────────────────────────────────────────
st.markdown(section("🗺️ Global Revenue Heatmap"), unsafe_allow_html=True)
geo_country = fdf.groupby("country")["revenue"].sum().reset_index()

fig_map = px.choropleth(geo_country, locations="country", locationmode="country names",
                        color="revenue", hover_name="country",
                        color_continuous_scale="Viridis")
fig_map.update_layout(**make_layout(height=600, coloraxis_showscale=True))
fig_map.update_geos(bgcolor="rgba(0,0,0,0)", showcountries=True, countrycolor="rgba(108,99,255,0.2)")
st.plotly_chart(fig_map, use_container_width=True)

st.markdown("---")

c1, c2 = st.columns([2, 1])

# ── Treemap ──────────────────────────────────────────────────────────────────
with c1:
    st.markdown(section("🌳 Country → City Distribution"), unsafe_allow_html=True)
    geo_tree = fdf.groupby(["country", "city"])["revenue"].sum().reset_index()
    fig_tree = px.treemap(geo_tree, path=["country", "city"], values="revenue",
                         color="revenue", color_continuous_scale="Blues")
    fig_tree.update_layout(**make_layout(height=450, coloraxis_showscale=False))
    st.plotly_chart(fig_tree, use_container_width=True)

# ── Top Countries Bar ────────────────────────────────────────────────────────
with c2:
    st.markdown(section("📊 Top 10 Countries"), unsafe_allow_html=True)
    top_countries = geo_country.sort_values("revenue", ascending=True).tail(10)
    fig_bar = go.Figure(go.Bar(x=top_countries["revenue"], y=top_countries["country"], orientation="h",
                             marker=dict(color="#48CAE4")))
    fig_bar.update_layout(**make_layout(height=450, xaxis=AXIS_STYLE, yaxis=AXIS_STYLE))
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("""<div class="footer">Geographical Intelligence &nbsp;·&nbsp; <span>© 2026 Kisho Jeyapragash</span></div>""", unsafe_allow_html=True)
