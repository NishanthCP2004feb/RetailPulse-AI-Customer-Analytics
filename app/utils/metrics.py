"""
RetailPulse Metrics Utility
===========================

Reusable KPI calculation functions for the
RetailPulse Streamlit Dashboard.

All functions are read-only.

Author:
RetailPulse
"""

from __future__ import annotations

from typing import Dict

import pandas as pd


# ==========================================================
# Revenue
# ==========================================================

def get_total_revenue(df: pd.DataFrame) -> float:
    """Return total revenue."""

    if df.empty:
        return 0.0

    return float(df["TotalAmount"].sum())


# ==========================================================
# Orders
# ==========================================================

def get_total_orders(df: pd.DataFrame) -> int:
    """Return total orders."""

    if df.empty:
        return 0

    return int(df["InvoiceID"].nunique())


# ==========================================================
# Customers
# ==========================================================

def get_total_customers(df: pd.DataFrame) -> int:
    """Return total customers."""

    if df.empty:
        return 0

    return int(df["CustomerID"].nunique())


# ==========================================================
# Products
# ==========================================================

def get_total_products(df: pd.DataFrame) -> int:
    """Return total products."""

    if df.empty:
        return 0

    return int(df["StockCode"].nunique())


# ==========================================================
# Quantity Sold
# ==========================================================

def get_total_quantity(df: pd.DataFrame) -> int:
    """Return total quantity sold."""

    if df.empty:
        return 0

    return int(df["Quantity"].sum())


# ==========================================================
# Average Order Value
# ==========================================================

def get_average_order_value(df: pd.DataFrame) -> float:
    """Average revenue per order."""

    orders = get_total_orders(df)

    if orders == 0:
        return 0.0

    return get_total_revenue(df) / orders


# ==========================================================
# Revenue Per Customer
# ==========================================================

def get_revenue_per_customer(df: pd.DataFrame) -> float:

    customers = get_total_customers(df)

    if customers == 0:
        return 0.0

    return get_total_revenue(df) / customers


# ==========================================================
# Revenue Per Product
# ==========================================================

def get_revenue_per_product(df: pd.DataFrame) -> float:

    products = get_total_products(df)

    if products == 0:
        return 0.0

    return get_total_revenue(df) / products

# ==========================================================
# Sales KPIs
# ==========================================================

def get_sales_kpis(df: pd.DataFrame) -> Dict[str, float]:
    """
    Return Sales Dashboard KPIs.
    """

    return {

        "Revenue": get_total_revenue(df),

        "Orders": get_total_orders(df),

        "Average Order Value": get_average_order_value(df),

        "Quantity Sold": get_total_quantity(df),

    }


# ==========================================================
# Customer KPIs
# ==========================================================

def get_customer_kpis(df: pd.DataFrame) -> Dict[str, float]:
    """
    Return Customer Dashboard KPIs.
    """

    return {

        "Customers": get_total_customers(df),

        "Revenue Per Customer": get_revenue_per_customer(df),

        "Orders": get_total_orders(df),

    }


# ==========================================================
# Product KPIs
# ==========================================================

def get_product_kpis(df: pd.DataFrame) -> Dict[str, float]:
    """
    Return Product Dashboard KPIs.
    """

    return {

        "Products": get_total_products(df),

        "Revenue": get_total_revenue(df),

        "Revenue Per Product": get_revenue_per_product(df),

        "Quantity Sold": get_total_quantity(df),

    }


# ==========================================================
# Country KPIs
# ==========================================================

def get_country_kpis(df: pd.DataFrame) -> Dict[str, float]:
    """
    Return Country Dashboard KPIs.
    """

    countries = 0

    if "Country" in df.columns:

        countries = int(df["Country"].nunique())

    return {

        "Countries": countries,

        "Revenue": get_total_revenue(df),

        "Customers": get_total_customers(df),

        "Orders": get_total_orders(df),

    }


# ==========================================================
# Basket KPIs
# ==========================================================

def get_basket_kpis(df: pd.DataFrame) -> Dict[str, float]:
    """
    Basket metrics used in Interactive Analytics.
    """

    avg_basket = 0.0
    avg_size = 0.0

    if "BasketValue" in df.columns:

        avg_basket = float(df["BasketValue"].mean())

    if "BasketSize" in df.columns:

        avg_size = float(df["BasketSize"].mean())

    return {

        "Average Basket Value": avg_basket,

        "Average Basket Size": avg_size,

    }


# ==========================================================
# Dataset KPIs
# ==========================================================

def get_dataset_summary(df: pd.DataFrame) -> Dict[str, int]:
    """
    General dataset information.
    """

    return {

        "Rows": len(df),

        "Columns": len(df.columns),

        "Missing Values": int(df.isna().sum().sum()),

        "Duplicate Rows": int(df.duplicated().sum()),

    }
# ==========================================================
# Forecast KPIs
# ==========================================================

def get_forecast_kpis(df: pd.DataFrame) -> Dict[str, float]:
    """
    Forecast dashboard KPIs.
    """

    metrics = {}

    if df.empty:
        return metrics

    if "Forecast" in df.columns:
        metrics["Forecast Total"] = float(df["Forecast"].sum())

    if "Actual" in df.columns:
        metrics["Actual Total"] = float(df["Actual"].sum())

    if "Forecast" in df.columns and "Actual" in df.columns:
        metrics["Forecast Error"] = float(
            abs(df["Forecast"] - df["Actual"]).mean()
        )

    return metrics


# ==========================================================
# Churn KPIs
# ==========================================================

def get_churn_kpis(df: pd.DataFrame) -> Dict[str, float]:
    """
    Churn dashboard KPIs.
    """

    metrics = {}

    if df.empty:
        return metrics

    metrics["High Risk Customers"] = len(df)

    if "Probability" in df.columns:
        metrics["Average Risk"] = float(
            df["Probability"].mean()
        )

    return metrics


# ==========================================================
# Inventory KPIs
# ==========================================================

def get_inventory_kpis(df: pd.DataFrame) -> Dict[str, float]:
    """
    Inventory dashboard KPIs.
    """

    metrics = {}

    if df.empty:
        return metrics

    metrics["Products"] = len(df)

    if "CurrentStock" in df.columns:
        metrics["Total Stock"] = float(
            df["CurrentStock"].sum()
        )

    if "RecommendedStock" in df.columns:
        metrics["Recommended Stock"] = float(
            df["RecommendedStock"].sum()
        )

    return metrics


# ==========================================================
# Recommendation KPIs
# ==========================================================

def get_recommendation_kpis(df: pd.DataFrame) -> Dict[str, float]:
    """
    Recommendation dashboard KPIs.
    """

    metrics = {}

    if df.empty:
        return metrics

    metrics["Recommendations"] = len(df)

    if "CustomerID" in df.columns:
        metrics["Customers"] = int(
            df["CustomerID"].nunique()
        )

    return metrics


# ==========================================================
# Business KPIs
# ==========================================================

def get_business_kpis(df: pd.DataFrame) -> Dict[str, float]:
    """
    Executive Business KPIs.
    """

    return {

        "Revenue": get_total_revenue(df),

        "Orders": get_total_orders(df),

        "Customers": get_total_customers(df),

        "Products": get_total_products(df),

        "Average Order Value": get_average_order_value(df),

    }


# ==========================================================
# Basic KPIs
# ==========================================================

def get_basic_kpis(df: pd.DataFrame) -> Dict[str, float]:
    """
    Common KPIs used across dashboards.
    """

    return {

        "Revenue": get_total_revenue(df),

        "Orders": get_total_orders(df),

        "Customers": get_total_customers(df),

        "Products": get_total_products(df),

        "Quantity": get_total_quantity(df),

    }


# ==========================================================
# Export Functions
# ==========================================================

__all__ = [

    "get_total_revenue",

    "get_total_orders",

    "get_total_customers",

    "get_total_products",

    "get_total_quantity",

    "get_average_order_value",

    "get_revenue_per_customer",

    "get_revenue_per_product",

    "get_sales_kpis",

    "get_customer_kpis",

    "get_product_kpis",

    "get_country_kpis",

    "get_basket_kpis",

    "get_dataset_summary",

    "get_forecast_kpis",

    "get_churn_kpis",

    "get_inventory_kpis",

    "get_recommendation_kpis",

    "get_business_kpis",

    "get_basic_kpis",

]
