from pathlib import Path
import pandas as pd
import streamlit as st

# ==========================================================
# Base Directories
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
MODELS_DIR = PROJECT_ROOT / "models"

# ==========================================================
# Generic CSV Loader
# ==========================================================

@st.cache_data(show_spinner=False)
def _load_csv(path: Path, parse_dates=None):

    if not path.exists():
        st.error(f"Missing file:\n{path}")
        st.stop()

    try:
        return pd.read_csv(path, parse_dates=parse_dates)

    except Exception as e:
        st.error(f"Unable to load\n{path.name}\n\n{e}")
        st.stop()

# ==========================================================
# Retail Dataset
# ==========================================================

@st.cache_data(show_spinner=False)
def load_retail_data():

    return _load_csv(
        PROCESSED_DIR / "retail_cleaned.csv",
        parse_dates=["InvoiceDate"]
    )

# ==========================================================
# Customer RFM
# ==========================================================

@st.cache_data(show_spinner=False)
def load_customer_rfm():

    return _load_csv(
        PROCESSED_DIR / "customer_rfm.csv"
    )

# ==========================================================
# Customer Features
# ==========================================================

@st.cache_data(show_spinner=False)
def load_customer_features():

    return _load_csv(
        PROCESSED_DIR / "customer_features.csv"
    )

# ==========================================================
# Daily Sales
# ==========================================================

@st.cache_data(show_spinner=False)
def load_daily_sales():

    return _load_csv(
        PROCESSED_DIR / "daily_sales.csv",
        parse_dates=["Date"]
    )

# ==========================================================
# Analysis Dataset
# ==========================================================

@st.cache_data(show_spinner=False)
def load_analysis_data():

    return _load_csv(
        PROCESSED_DIR / "analysis_data.csv",
        parse_dates=["InvoiceDate"]
    )

# ==========================================================
# Forecast Reports
# ==========================================================

@st.cache_data(show_spinner=False)
def load_forecast_results():

    return _load_csv(
        REPORTS_DIR / "forecast_results.csv",
        parse_dates=["Date"]
    )

@st.cache_data(show_spinner=False)
def load_forecast_model_comparison():

    return _load_csv(
        REPORTS_DIR / "forecasting_model_comparison.csv"
    )

@st.cache_data(show_spinner=False)
def load_forecast_dataset_summary():

    return _load_csv(
        REPORTS_DIR / "forecasting_dataset_summary.csv"
    )

# ==========================================================
# Churn
# ==========================================================

@st.cache_data(show_spinner=False)
def load_churn_data():

    df = _load_csv(
        REPORTS_DIR / "high_risk_customers.csv"
    )

    if "FirstPurchase" in df.columns:
        df["FirstPurchase"] = pd.to_datetime(df["FirstPurchase"])

    if "LastPurchase" in df.columns:
        df["LastPurchase"] = pd.to_datetime(df["LastPurchase"])

    return df

# ==========================================================
# Inventory
# ==========================================================

@st.cache_data(show_spinner=False)
def load_inventory_summary():

    return _load_csv(
        REPORTS_DIR / "inventory_summary.csv"
    )

@st.cache_data(show_spinner=False)
def load_inventory_recommendations():

    return _load_csv(
        REPORTS_DIR / "inventory_recommendations.csv"
    )

# ==========================================================
# Recommendation System
# ==========================================================

@st.cache_data(show_spinner=False)
def load_recommendations():

    return _load_csv(
        REPORTS_DIR / "customer_product_recommendations.csv"
    )

# ==========================================================
# Business Recommendations
# ==========================================================

@st.cache_data(show_spinner=False)
def load_business_recommendations():

    return _load_csv(
        REPORTS_DIR / "business_recommendations.csv"
    )

# ==========================================================
# Combined Loaders
# ==========================================================

@st.cache_data(show_spinner=False)
def load_forecast_reports():

    return (
        load_forecast_results(),
        load_forecast_model_comparison(),
        load_forecast_dataset_summary()
    )

@st.cache_data(show_spinner=False)
def load_inventory_reports():

    return (
        load_inventory_summary(),
        load_inventory_recommendations()
    )

@st.cache_data(show_spinner=False)
def load_business_reports():

    return (
        load_forecast_results(),
        load_forecast_model_comparison(),
        load_churn_data(),
        load_inventory_summary(),
        load_recommendations(),
        load_business_recommendations()
    )