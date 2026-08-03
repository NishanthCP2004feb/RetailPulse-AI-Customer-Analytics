"""
RetailPulse Data Loader

Centralized data loading functions for the production
Streamlit application.

All datasets are treated as read-only.
"""

from pathlib import Path

import pandas as pd
import streamlit as st


# Project Root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Data Folder
DATA_DIR = PROJECT_ROOT / "data" / "processed"


@st.cache_data
def load_retail_data():
    """
    Load the cleaned retail transaction dataset.
    """
    return pd.read_csv(
        DATA_DIR / "retail_cleaned.csv",
        parse_dates=["InvoiceDate"]
    )


@st.cache_data
def load_customer_rfm():
    """
    Load customer RFM segmentation data.
    """
    return pd.read_csv(DATA_DIR / "customer_rfm.csv")


@st.cache_data
def load_customer_features():
    """
    Load customer engineered features.
    """
    return pd.read_csv(DATA_DIR / "customer_features.csv")


@st.cache_data
def load_daily_sales():
    """
    Load daily sales dataset.
    """
    return pd.read_csv(
        DATA_DIR / "daily_sales.csv",
        parse_dates=["InvoiceDate"]
    )