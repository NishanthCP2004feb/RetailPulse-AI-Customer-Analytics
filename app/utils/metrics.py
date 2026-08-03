"""
RetailPulse Metrics Utility

Reusable KPI calculation functions for the
RetailPulse Streamlit dashboard.

All functions operate on read-only DataFrames.
"""

from typing import Dict


def get_total_revenue(df) -> float:
    """Return total revenue."""
    return float(df["TotalAmount"].sum())


def get_total_orders(df) -> int:
    """Return total unique orders."""
    return int(df["InvoiceID"].nunique())


def get_total_customers(df) -> int:
    """Return total unique customers."""
    return int(df["CustomerID"].nunique())


def get_total_products(df) -> int:
    """Return total unique products."""
    return int(df["StockCode"].nunique())


def get_basic_kpis(df) -> Dict[str, float]:
    """
    Return all basic KPIs in a single dictionary.
    """
    return {
        "Total Revenue": get_total_revenue(df),
        "Orders": get_total_orders(df),
        "Customers": get_total_customers(df),
        "Products": get_total_products(df),
    }