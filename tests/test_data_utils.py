import pytest
import pandas as pd
import numpy as np
import os
from datetime import date
from app.utils.data_utils import load_orders, filter_df, compute_kpis, cohort_analysis, rfm_segmentation, top_customers, forecast_revenue

# ── Mock Data Helper ─────────────────────────────────────────────────────────
def get_mock_df():
    data = {
        "order_id": [1, 2, 3, 4],
        "order_date": ["2023-01-01", "2023-02-01", "2023-03-01", "2023-04-01"],
        "customer_id": [101, 102, 101, 103],
        "country": ["USA", "India", "USA", "UK"],
        "city": ["NY", "Delhi", "NY", "London"],
        "channel": ["Web", "Mobile", "Web", "Web"],
        "product_id": ["P1", "P2", "P3", "P4"],
        "category": ["Electronics", "Fashion", "Electronics", "Home"],
        "subcategory": ["S1", "S2", "S3", "S4"],
        "unit_price": [100, 50, 200, 150],
        "quantity": [1, 2, 1, 1],
        "discount": [0, 0.1, 0, 0.05],
        "revenue": [100, 90, 200, 142.5],
        "cost": [70, 40, 150, 100],
    }
    df = pd.DataFrame(data)
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["order_month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    df["profit"] = df["revenue"] - df["cost"]
    df["day_of_week"] = df["order_date"].dt.day_name()
    df["discount_pct"] = (df["discount"] * 100).round(1)
    return df

# ── Tests ────────────────────────────────────────────────────────────────────

def test_compute_kpis_normal():
    df = get_mock_df()
    kpis = compute_kpis(df)
    assert kpis["Revenue"] == 532.5
    assert kpis["Orders"] == 4
    assert kpis["Customers"] == 3

def test_compute_kpis_empty():
    df = pd.DataFrame(columns=["revenue", "profit", "order_id", "customer_id"])
    kpis = compute_kpis(df)
    assert kpis["Revenue"] == 0
    assert kpis["AOV"] == 0

def test_filter_df_single_date():
    df = get_mock_df()
    # Test our guard for single-date tuple
    fdf = filter_df(df, (date(2023, 1, 1),))
    assert len(fdf) == 1
    assert fdf.iloc[0]["order_id"] == 1

def test_rfm_segmentation_insufficient():
    df = get_mock_df().head(2) # Only 2 customers
    rfm = rfm_segmentation(df)
    assert rfm.empty

def test_cohort_analysis_insufficient():
    df = get_mock_df().head(1)
    c_abs, c_ret = cohort_analysis(df)
    assert c_abs is None

def test_top_customers():
    df = get_mock_df()
    top = top_customers(df, 2)
    assert len(top) == 2
    assert top.iloc[0]["customer_id"] == 101 # Revenue 300
    assert top.iloc[0]["Revenue"] == 300

def test_forecast_revenue_insufficient():
    df = get_mock_df() # Only 4 months
    hist, fcast = forecast_revenue(df, 3)
    assert fcast is None
