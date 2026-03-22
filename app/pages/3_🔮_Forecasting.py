import os
import streamlit as st
import plotly.graph_objects as go
from utils.data_utils import load_orders, filter_df, forecast_revenue
from utils.styles import get_css, section, sidebar_brand, make_layout, AXIS_STYLE, GRID_CLR, FONT_CLR

st.set_page_config(page_title="Dashboard | Forecasting", page_icon="🔮", layout="wide")
st.markdown(get_css(), unsafe_allow_html=True)

DATA_PATH = os.environ.get("ORDERS_CSV", os.path.join(os.path.dirname(__file__), "..", "..", "data", "orders.csv"))

@st.cache_data(show_spinner=False)
def load_data():
    return load_orders(DATA_PATH)

df = load_data()

with st.sidebar:
    st.markdown(sidebar_brand("Predictive Insights"), unsafe_allow_html=True)
    countries = st.multiselect("🌍 Countries", sorted(df["country"].unique().tolist()))
    categories = st.multiselect("🗂️ Categories", sorted(df["category"].unique().tolist()))
    fdf = filter_df(df, (df["order_date"].dt.date.min(), df["order_date"].dt.date.max()), countries=countries, categories=categories)

st.markdown("""
<div class="hero-wrap">
  <div class="hero-title">🔮 Predictive Analytics</div>
  <div class="hero-sub">Revenue Forecasting & Target Tracking</div>
</div>
""", unsafe_allow_html=True)

# ── Feature 1: Sales Forecasting ─────────────────────────────────────────────
st.markdown(section("📈 6-Month Revenue Forecast"), unsafe_allow_html=True)
hist, forecast = forecast_revenue(fdf, 6)

if forecast is not None:
    fig_fcast = go.Figure()
    # Historical
    fig_fcast.add_trace(go.Scatter(x=hist.index, y=hist.values, name="Historical",
                                 line=dict(color="#6C63FF", width=3)))
    # Forecast
    fig_fcast.add_trace(go.Scatter(x=forecast.index, y=forecast.values, name="Forecast",
                                 line=dict(color="#48CAE4", width=3, dash="dash")))
    
    fig_fcast.update_layout(**make_layout(height=450, xaxis=AXIS_STYLE, yaxis={**AXIS_STYLE, "title":"Revenue ($)"}))
    st.plotly_chart(fig_fcast, use_container_width=True)
else:
    st.info("ℹ️ Not enough historical data to generate a forecast (minimum 6 months required).")

st.markdown("---")

c1, c2 = st.columns(2)

# ── Feature 4: Revenue vs Target Gauge ────────────────────────────────────────
with c1:
    st.markdown(section("🎯 Current vs Target Revenue"), unsafe_allow_html=True)
    # Synthetic target: 110% of previous period's total revenue
    current_rev = fdf["revenue"].sum()
    target_rev = current_rev * 1.15  # Let's say 15% growth target
    
    fig_gauge = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = current_rev,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': "Revenue vs Goal", 'font': {'size': 20, 'color':FONT_CLR}},
        delta = {'reference': target_rev, 'increasing': {'color': "#34d399"}},
        gauge = {
            'axis': {'range': [None, target_rev * 1.2], 'tickwidth': 1, 'tickcolor': "#8888aa"},
            'bar': {'color': "#6C63FF"},
            'bgcolor': "rgba(0,0,0,0)",
            'borderwidth': 2,
            'bordercolor': "rgba(108,99,255,0.3)",
            'steps': [
                {'range': [0, target_rev * 0.8], 'color': 'rgba(255,107,107,0.1)'},
                {'range': [target_rev * 0.8, target_rev], 'color': 'rgba(250,204,21,0.1)'}],
            'threshold': {
                'line': {'color': "#48CAE4", 'width': 4},
                'thickness': 0.75,
                'value': target_rev}
        }
    ))
    fig_gauge.update_layout(**make_layout(height=400))
    st.plotly_chart(fig_gauge, use_container_width=True)

# ── Growth Rate ─────────────────────────────────────────────────────────────
with c2:
    st.markdown(section("📊 Monthly Growth Rate"), unsafe_allow_html=True)
    hist_m = fdf.groupby("order_month")["revenue"].sum().sort_index()
    growth = hist_m.pct_change() * 100
    
    fig_growth = go.Figure(go.Bar(x=growth.index, y=growth.values,
                                marker=dict(color=growth.values, colorscale="RdYlGn", cmid=0)))
    fig_growth.update_layout(**make_layout(height=400, xaxis=AXIS_STYLE, yaxis={**AXIS_STYLE, "title":"Growth %"}))
    st.plotly_chart(fig_growth, use_container_width=True)

st.markdown("""<div class="footer">Forecasting & Targets &nbsp;·&nbsp; <span>© 2026 Kisho Jeyapragash</span></div>""", unsafe_allow_html=True)
