import pandas as pd
import numpy as np


# ---------------------------------------------------------------------------
# Data Loading
# ---------------------------------------------------------------------------

def load_orders(csv_path: str) -> pd.DataFrame:
    try:
        df = pd.read_csv(csv_path, parse_dates=["order_date"])
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Dataset not found at: {csv_path}\n"
            "Set the ORDERS_CSV environment variable to point to your file."
        )

    required_cols = {
        "order_id", "order_date", "customer_id", "country", "city",
        "channel", "product_id", "category", "subcategory",
        "unit_price", "quantity", "discount", "revenue", "cost",
    }
    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing columns: {missing}")

    df["order_month"]  = df["order_date"].values.astype("datetime64[M]")
    df["profit"]       = df["revenue"] - df["cost"]
    df["day_of_week"]  = df["order_date"].dt.day_name()
    df["discount_pct"] = (df["discount"] * 100).round(1)
    return df


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

def filter_df(df, date_range, countries=None, channels=None, categories=None):
    """Apply sidebar filters. Handles both 1-date and 2-date range selections."""
    if len(date_range) == 2:
        start, end = date_range[0], date_range[1]
    else:
        start = end = date_range[0]

    mask = (df["order_date"].dt.date >= start) & (df["order_date"].dt.date <= end)
    if countries:
        mask &= df["country"].isin(countries)
    if channels:
        mask &= df["channel"].isin(channels)
    if categories:
        mask &= df["category"].isin(categories)
    return df.loc[mask].copy()


# ---------------------------------------------------------------------------
# KPI Computation
# ---------------------------------------------------------------------------

def compute_kpis(df):
    """Compute top-level KPIs. Returns zeroed dict on empty DataFrame."""
    if df.empty:
        return {
            "Revenue": 0, "Profit": 0, "Orders": 0,
            "Customers": 0, "AOV": 0, "Margin%": 0,
        }
    total_revenue = df["revenue"].sum()
    total_profit  = df["profit"].sum()
    per_order_rev = df.groupby("order_id")["revenue"].sum()
    return {
        "Revenue":   total_revenue,
        "Profit":    total_profit,
        "Orders":    df["order_id"].nunique(),
        "Customers": df["customer_id"].nunique(),
        "AOV":       per_order_rev.mean() if not per_order_rev.empty else 0,
        "Margin%":   (total_profit / total_revenue) if total_revenue > 0 else 0,
    }


# ---------------------------------------------------------------------------
# Cohort Analysis
# ---------------------------------------------------------------------------

def cohort_analysis(df):
    """
    Build cohort retention tables.
    Returns (cohort_abs, cohort_ret) or (None, None) if insufficient data.
    """
    if df.empty or df["customer_id"].nunique() < 2:
        return None, None

    first = df.groupby("customer_id")["order_month"].min().rename("cohort_month")
    tmp = df.merge(first, on="customer_id", how="left")
    
    tmp["cohort_index"] = (
        (tmp["order_month"].dt.year  - tmp["cohort_month"].dt.year)  * 12 +
        (tmp["order_month"].dt.month - tmp["cohort_month"].dt.month)
    ) + 1

    cohort = (
        tmp.groupby(["cohort_month", "cohort_index"])["customer_id"]
        .nunique().reset_index()
    )
    cohort_pivot = (
        cohort.pivot(index="cohort_month", columns="cohort_index", values="customer_id")
        .fillna(0).astype(int)
    )

    if 1 not in cohort_pivot.columns:
        return None, None

    cohort_ret = cohort_pivot.divide(cohort_pivot[1], axis=0).round(3)
    return cohort_pivot, cohort_ret


# ---------------------------------------------------------------------------
# RFM Segmentation
# ---------------------------------------------------------------------------

def rfm_segmentation(df, as_of=None):
    """Compute RFM scores. Returns empty DataFrame if fewer than 3 customers."""
    n_customers = df["customer_id"].nunique()
    if df.empty or n_customers < 3:
        return pd.DataFrame(columns=["customer_id", "R", "F", "M", "RFM_Score", "Segment"])

    if as_of is None:
        as_of = df["order_date"].max().normalize() + pd.Timedelta(days=1)

    recency   = df.groupby("customer_id")["order_date"].max().apply(lambda d: (as_of - d).days)
    frequency = df.groupby("customer_id")["order_id"].nunique()
    monetary  = df.groupby("customer_id")["revenue"].sum()

    r = pd.qcut(recency,                       3, labels=[3, 2, 1], duplicates="drop")
    f = pd.qcut(frequency.rank(method="first"), 3, labels=[1, 2, 3], duplicates="drop")
    m = pd.qcut(monetary.rank(method="first"),  3, labels=[1, 2, 3], duplicates="drop")

    rfm = pd.DataFrame({"R": r.astype(float), "F": f.astype(float), "M": m.astype(float)})
    rfm.dropna(inplace=True)
    rfm = rfm.astype(int)
    rfm["RFM_Score"] = rfm.sum(axis=1)
    rfm["Segment"] = pd.cut(
        rfm["RFM_Score"],
        bins=[2, 5, 7, 9],
        labels=["New/Cold", "Active", "Champions"],
        include_lowest=True,
    )
    rfm.index.name = "customer_id"
    return rfm.reset_index()


# ---------------------------------------------------------------------------
# Top Customers
# ---------------------------------------------------------------------------

def top_customers(df, n: int = 20) -> pd.DataFrame:
    """Return top-N customers ranked by total revenue."""
    if df.empty:
        return pd.DataFrame(columns=["customer_id", "Revenue", "Orders", "AOV", "Margin%"])

    grp = df.groupby("customer_id").agg(
        Revenue  = ("revenue", "sum"),
        Profit   = ("profit",  "sum"),
        Orders   = ("order_id", "nunique"),
    ).reset_index()
    grp["AOV"]     = (grp["Revenue"] / grp["Orders"]).round(2)
    grp["Margin%"] = ((grp["Profit"] / grp["Revenue"]) * 100).round(1)
    grp = grp.drop(columns=["Profit"])
    return grp.sort_values("Revenue", ascending=False).head(n).reset_index(drop=True)


# ---------------------------------------------------------------------------
# Discount Impact Analysis
# ---------------------------------------------------------------------------

def discount_analysis(df) -> pd.DataFrame:
    """Return per-order discount % and revenue for scatter analysis."""
    if df.empty:
        return pd.DataFrame(columns=["order_id", "discount_pct", "revenue", "category"])

    order_level = df.groupby(["order_id", "category"]).agg(
        discount_pct = ("discount_pct", "mean"),
        revenue      = ("revenue", "sum"),
    ).reset_index()
    return order_level


# ---------------------------------------------------------------------------
# Day-of-Week Order Heatmap
# ---------------------------------------------------------------------------

_DOW_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def orders_by_dayofweek(df) -> pd.DataFrame:
    """Return a pivot: day_of_week × category → order count for heatmap."""
    if df.empty or "day_of_week" not in df.columns:
        return pd.DataFrame()

    pivot = (
        df.groupby(["day_of_week", "category"])["order_id"]
        .nunique()
        .reset_index()
        .pivot(index="day_of_week", columns="category", values="order_id")
        .fillna(0)
        .astype(int)
    )
    # Ensure correct weekday order
    pivot = pivot.reindex([d for d in _DOW_ORDER if d in pivot.index])
    return pivot


# ---------------------------------------------------------------------------
# Revenue Forecasting (Holt-Winters Exponential Smoothing)
# ---------------------------------------------------------------------------

def forecast_revenue(df, periods: int = 6):
    """
    Forecast future monthly revenue using Holt-Winters ExponentialSmoothing.
    Returns (historical_series, forecast_series) as two pd.Series with DatetimeIndex.
    Returns (historical_series, None) if insufficient data.
    """
    from statsmodels.tsa.holtwinters import ExponentialSmoothing
    import warnings
    from statsmodels.tools.sm_exceptions import ConvergenceWarning
    warnings.simplefilter("ignore", ConvergenceWarning)

    ts = (
        df.groupby("order_month")["revenue"]
        .sum()
        .sort_index()
    )
    if hasattr(ts.index, "to_timestamp"):
        ts.index = ts.index.to_timestamp()

    # Explicitly set frequency to suppress ValueWarning
    ts.index.freq = "MS"

    if len(ts) < 6:
        return ts, None

    try:
        # Use simple trend if seasonality fails to converge
        model = ExponentialSmoothing(
            ts,
            trend="add",
            seasonal=None,
            initialization_method="estimated",
        )
        model_fit = model.fit(optimized=True)

        last_date  = ts.index[-1]
        future_idx = pd.date_range(
            start=last_date + pd.DateOffset(months=1),
            periods=periods,
            freq="MS",
        )
        forecast = pd.Series(model_fit.forecast(periods).values, index=future_idx)
        forecast = forecast.clip(lower=0)
    except Exception:
        return ts, None

    return ts, forecast
