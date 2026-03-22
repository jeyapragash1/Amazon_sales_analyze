# 📊 Premium Data Storytelling Dashboard: Real Amazon Insights

An interactive, enterprise-grade **e-commerce analytics platform** that transforms **Real Amazon Sales Data** into **actionable business narratives**. 

This version features a complete **Premium UI overhaul** (glassmorphism), **INR Currency Integration**, and high-fidelity mapping of 1,400+ real products (Electronics, Home, Kitchen) across 5,000 transactions.

Built with **Python**, **Streamlit**, and **Plotly**.

---

## 🌟 Premium Features

- **💎 High-Fidelity Data**: Powered by the **Real Amazon Sales Dataset**—real prices, real products, and real categories.
- **💎 Glassmorphism Design**: Modern, high-end dark theme with frosted glass effects, animated headers, and vibrant gradients.
- **📑 Multi-Page Architecture**: Organized into focused domains: Overview, Customers, Geography, and Forecasting.
- **🔮 Sales Forecasting**: 6-month revenue predictions using Holt-Winters Exponential Smoothing.
- **🗺️ Global Choropleth**: Interactive world map for real-time geographical revenue intelligence.
- **🎯 Predictive Targets**: Dynamic gauge charts tracking performance against 115% growth targets.
- **👤 Customer Intelligence**: Deep-dive analysis including Top 20 ranking, RFM Segmentation, and Cohort Retention.

---

## 📁 Project Structure

```text
Data-Storytelling-Dashboard/
├── app/
├── data/
│   ├── amazon.csv              # Source: Real Amazon Sales Dataset
│   └── orders.csv              # Processed: 5,000 Transactions (INR)
├── scripts/
│   └── process_amazon.py       # Data migration & cleaning script
├── tests/
│   └── test_data_utils.py      # Pytest suite (7/7 passing)
├── requirements.txt            # Project dependencies
└── README.md
```

---

## 🚀 Getting Started

1. **Environment & Dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: .\venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Run the Dashboard**:
   ```bash
   streamlit run app/app.py
   ```

---

## 🛡️ License & Copyright
© 2026 **Kisho Jeyapragash**. All rights reserved.

---

## 🎯 Analytical Highlights (Real Data)
- **Top Categories**: Electronics (64% Revenue), Home & Kitchen, Computers.
- **Revenue Units**: INR (Indian Rupee) mapping from Amazon source.
- **Segments**: Champions, Active, New/Cold (via real RFM behavior).
