# ==========================================================
# Imports
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.theme import load_css
from utils.data_loader import load_retail_data

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Customer Analytics",
    page_icon="👥",
    layout="wide",
)

load_css()

# ==========================================================
# Header
# ==========================================================

st.title("👥 Customer Analytics")

st.caption(
    "RetailPulse • Customer Analytics Dashboard"
)

st.markdown("---")

# ==========================================================
# Load Data
# ==========================================================

df = load_retail_data()

if df.empty:
    st.error("Dataset is empty.")
    st.stop()

# ==========================================================
# Sidebar Filters
# ==========================================================

st.sidebar.header("🔍 Customer Filters")

countries = sorted(
    df["Country"].dropna().unique()
)

years = sorted(
    df["InvoiceYear"].unique()
)

months = sorted(
    df["MonthName"].unique()
)

selected_countries = st.sidebar.multiselect(
    "Country",
    countries,
    default=countries,
)

selected_years = st.sidebar.multiselect(
    "Invoice Year",
    years,
    default=years,
)

selected_months = st.sidebar.multiselect(
    "Month",
    months,
    default=months,
)

filtered_df = df[
    (
        df["Country"].isin(selected_countries)
    )
    &
    (
        df["InvoiceYear"].isin(selected_years)
    )
    &
    (
        df["MonthName"].isin(selected_months)
    )
]

if filtered_df.empty:
    st.warning(
        "No records available for selected filters."
    )
    st.stop()

# ==========================================================
# Customer Summary
# ==========================================================

customer_summary = (
    filtered_df
    .groupby(
        "CustomerID",
        as_index=False
    )
    .agg(
        Revenue=("TotalAmount", "sum"),
        Orders=("InvoiceID", "nunique"),
        Quantity=("Quantity", "sum"),
        BasketValue=("BasketValue", "mean"),
        Country=("Country", "first"),
    )
)

# ==========================================================
# KPI Calculations
# ==========================================================

total_customers = len(customer_summary)

total_revenue = customer_summary["Revenue"].sum()

average_customer_revenue = (
    total_revenue / total_customers
)

average_orders = (
    customer_summary["Orders"].mean()
)

average_basket = (
    customer_summary["BasketValue"].mean()
)

highest_customer = (
    customer_summary
    .sort_values(
        "Revenue",
        ascending=False
    )
    .iloc[0]["CustomerID"]
)

# ==========================================================
# KPI Cards
# ==========================================================

st.subheader("📊 Customer Overview")

c1, c2, c3 = st.columns(3)

c1.metric(
    "Customers",
    f"{total_customers:,}"
)

c2.metric(
    "Revenue",
    f"£{total_revenue:,.2f}"
)

c3.metric(
    "Average Revenue",
    f"£{average_customer_revenue:,.2f}"
)

c4, c5, c6 = st.columns(3)

c4.metric(
    "Avg Orders",
    f"{average_orders:.2f}"
)

c5.metric(
    "Average Basket",
    f"£{average_basket:,.2f}"
)

c6.metric(
    "Top Customer",
    str(highest_customer),
)

st.markdown("---")

# ==========================================================
# Top Customers by Revenue
# ==========================================================

left_chart, right_chart = st.columns(2)

with left_chart:

    st.subheader("🏆 Top 10 Customers by Revenue")

    top_customers = (
        customer_summary
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(10)
    )

    fig_top_customers = px.bar(
        top_customers,
        x="Revenue",
        y="CustomerID",
        orientation="h",
        color="Revenue",
        text_auto=".2s",
        title="Top Customers by Revenue"
    )

    fig_top_customers.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
        xaxis_title="Revenue (£)",
        yaxis_title=""
    )

    st.plotly_chart(
        fig_top_customers,
        use_container_width=True,
        key="top_customers_revenue"
    )

with right_chart:

    st.subheader("🛒 Top 10 Customers by Orders")

    top_orders = (
        customer_summary
        .sort_values(
            "Orders",
            ascending=False
        )
        .head(10)
    )

    fig_top_orders = px.bar(
        top_orders,
        x="Orders",
        y="CustomerID",
        orientation="h",
        color="Orders",
        text_auto=True,
        title="Top Customers by Orders"
    )

    fig_top_orders.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
        yaxis_title=""
    )

    st.plotly_chart(
        fig_top_orders,
        use_container_width=True,
        key="top_customer_orders"
    )

st.markdown("---")

# ==========================================================
# Revenue Distribution
# ==========================================================

left_hist, right_hist = st.columns(2)

with left_hist:

    st.subheader("💰 Customer Revenue Distribution")

    fig_revenue_distribution = px.histogram(
        customer_summary,
        x="Revenue",
        nbins=40,
        title="Revenue Distribution"
    )

    fig_revenue_distribution.update_layout(
        template="plotly_white",
        height=450,
        title_x=0.5,
    )

    st.plotly_chart(
        fig_revenue_distribution,
        use_container_width=True,
        key="customer_revenue_distribution"
    )

with right_hist:

    st.subheader("📦 Order Frequency")

    fig_order_frequency = px.histogram(
        customer_summary,
        x="Orders",
        nbins=30,
        title="Customer Order Frequency"
    )

    fig_order_frequency.update_layout(
        template="plotly_white",
        height=450,
        title_x=0.5,
    )

    st.plotly_chart(
        fig_order_frequency,
        use_container_width=True,
        key="customer_order_frequency"
    )

st.markdown("---")

# ==========================================================
# Country Distribution
# ==========================================================

left_country, right_country = st.columns(2)

with left_country:

    st.subheader("🌍 Revenue by Country")

    country_summary = (
        customer_summary
        .groupby(
            "Country",
            as_index=False
        )
        .agg(
            Revenue=("Revenue", "sum")
        )
        .sort_values(
            "Revenue",
            ascending=False
        )
        .head(10)
    )

    fig_country = px.bar(
        country_summary,
        x="Revenue",
        y="Country",
        orientation="h",
        color="Revenue",
        title="Top Countries by Customer Revenue"
    )

    fig_country.update_layout(
        template="plotly_white",
        height=450,
        title_x=0.5,
        yaxis_title=""
    )

    st.plotly_chart(
        fig_country,
        use_container_width=True,
        key="country_customer_revenue"
    )

with right_country:

    st.subheader("📅 Monthly Active Customers")

    monthly_customers = (
        filtered_df
        .groupby(
            "InvoiceMonthYear"
        )["CustomerID"]
        .nunique()
        .reset_index(name="Customers")
    )

    fig_monthly_customers = px.line(
        monthly_customers,
        x="InvoiceMonthYear",
        y="Customers",
        markers=True,
        title="Monthly Active Customers"
    )

    fig_monthly_customers.update_layout(
        template="plotly_white",
        height=450,
        title_x=0.5,
        xaxis_title="Month",
        yaxis_title="Customers"
    )

    st.plotly_chart(
        fig_monthly_customers,
        use_container_width=True,
        key="monthly_active_customers"
    )

st.markdown("---")

# ==========================================================
# Customer Search
# ==========================================================

st.subheader("🔍 Customer Search")

search_customer = st.text_input(
    "Search Customer ID",
    placeholder="Enter Customer ID..."
)

display_table = customer_summary.copy()

if search_customer:
    display_table = display_table[
        display_table["CustomerID"]
        .astype(str)
        .str.contains(
            search_customer,
            case=False,
            na=False,
        )
    ]

# ==========================================================
# Customer Performance Table
# ==========================================================

st.subheader("📋 Customer Summary")

display_table = display_table.sort_values(
    "Revenue",
    ascending=False,
)

st.dataframe(
    display_table,
    use_container_width=True,
    hide_index=True,
)

# ==========================================================
# Download Report
# ==========================================================

csv = (
    display_table
    .to_csv(index=False)
    .encode("utf-8")
)

st.download_button(
    label="📥 Download Customer Report",
    data=csv,
    file_name="customer_analytics.csv",
    mime="text/csv",
)

st.markdown("---")

# ==========================================================
# Business Insights
# ==========================================================

highest_revenue_customer = (
    customer_summary
    .sort_values("Revenue", ascending=False)
    .iloc[0]
)

highest_orders_customer = (
    customer_summary
    .sort_values("Orders", ascending=False)
    .iloc[0]
)

active_countries = (
    customer_summary["Country"]
    .nunique()
)

average_revenue = (
    customer_summary["Revenue"]
    .mean()
)

average_orders = (
    customer_summary["Orders"]
    .mean()
)

average_basket = (
    customer_summary["BasketValue"]
    .mean()
)

left_info, right_info = st.columns(2)

with left_info:

    st.success(
        f"""
### 💰 Revenue Insights

Highest Revenue Customer

**{highest_revenue_customer['CustomerID']}**

Revenue

**£{highest_revenue_customer['Revenue']:,.2f}**

Average Customer Revenue

**£{average_revenue:,.2f}**
"""
    )

with right_info:

    st.success(
        f"""
### 👥 Customer Insights

Highest Order Customer

**{highest_orders_customer['CustomerID']}**

Orders

**{highest_orders_customer['Orders']}**

Active Countries

**{active_countries}**

Average Orders

**{average_orders:.2f}**
"""
    )

st.markdown("---")

# ==========================================================
# Executive Summary
# ==========================================================

st.info(
    f"""
### 📊 Executive Summary

• Customers Analysed:
**{total_customers:,}**

• Revenue Generated:
**£{total_revenue:,.2f}**

• Average Basket Value:
**£{average_basket:,.2f}**

• Top Customer:
**{highest_revenue_customer['CustomerID']}**
"""
)

st.markdown("---")

# ==========================================================
# Footer
# ==========================================================

st.caption(
    """
RetailPulse

Customer Analytics Dashboard

Notebook Outputs : Read Only

Dataset : retail_cleaned.csv

Version : 1.0
"""
)