# 📊 Project Fact Sheet: Premium Data Storytelling Dashboard

A high-fidelity project summary designed to help you build your presentation slides.

---

## 🎯 1. Project Objective
To transform raw e-commerce data (specifically from Amazon) into an **Executive-Level Business Intelligence (BI) Platform**. The project focuses on **three pillars**:
1.  **Data Storytelling**: Visualizing complex trends with high-impact charts.
2.  **Predictive Analytics**: Forecasting future revenue using statistical models.
3.  **Customer Intelligence**: Segmenting users to improve marketing ROI.

---

## 🛠️ 2. The Tech Stack
*   **Language**: Python 3.10+
*   **Web Framework**: Streamlit (Advanced Multi-Page architecture)
*   **Visualizations**: Plotly (D3.js based interactive charts)
*   **Statistics/DS**: Pandas, NumPy, Statsmodels (Holt-Winters), Scipy
*   **Testing**: Pytest (Full Unit Test Suite)

---

## 📦 3. Data Strategy (Real-World Integration)
*   **Dataset Source**: Real Amazon Sales Dataset ([amazon.csv](file:///d:/BF%20project/Data-Storytelling-Dashboard/data/amazon.csv)).
*   **Products**: 1,465 unique SKUs including Electronics, Home, and Kitchen categories.
*   **Transactions**: 5,000 orders mapped across 24 months (Jan 2023 – Dec 2024).
*   **Currency**: Fully localized to **INR** (Indian Rupee) mapping.
*   **Pricing**: Real-world Amazon prices cleaned and processed (actual vs discounted).

---

## 🚀 4. Major Features (Slide Highlights)
1.  **Executive Overview**: Animated Hero UI with real-time KPI card monitoring.
2.  **Sales Forecasting**: 6-month projected revenue path using **Triple Exponential Smoothing**.
3.  **RFM Segmentation**: Behavioral bucketing into "Champions", "Active", and "At-Risk" segments.
4.  **Cohort Analysis**: Retention heatmaps tracking user stickiness over time.
5.  **Geographical Hub**: Interactive World Choropleth map with country-level revenue scaling.
6.  **Revenue vs Target**: Dynamic gauges tracking against a 115% growth KPI.

---

## 💎 5. Design & UI/UX
*   **Aesthetic**: "Glassmorphism" — Using transparency, frosted-glass effects, and vibrant gradients.
*   **UX Features**: Multi-page navigation (4 distinct modules), Sidebar summary stats, and high-contrast dark theme.
*   **Performance**: Cached data loading (`@st.cache_data`) for sub-second page transitions.

---

## ✅ 6. Quality & Reliability
*   **Verification**: 7/7 core analytical tests passing.
*   **Error Handling**: Robust guards for empty data, single-date filtering, and insufficient data for modeling.
*   **Project Maintenance**: Clean repository structure with automated [.gitignore](file:///d:/BF%20project/Data-Storytelling-Dashboard/.gitignore) and professional [README.md](file:///d:/BF%20project/Data-Storytelling-Dashboard/README.md).

---

## 🛡️ License
© 2026 **Kisho Jeyapragash**. All rights reserved.
