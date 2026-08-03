# ==========================================================
# Imports
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.theme import load_css
from utils.data_loader import load_retail_data

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Product Performance",
    page_icon="📦",
    layout="wide",
)

load_css()

# ==========================================================
# Page Header
# ==========================================================

st.title("📦 Product Performance")
st.caption("RetailPulse • Product Performance Dashboard")

st.markdown("---")

# ==========================================================
# Load Dataset
# ==========================================================

df = load_retail_data()

if df.empty:
    st.error("No data available.")
    st.stop()

# ==========================================================
# Sidebar Filters
# ==========================================================

st.sidebar.header("🔍 Product Filters")

countries = sorted(df["Country"].dropna().unique())
years = sorted(df["InvoiceYear"].unique())
months = sorted(df["MonthName"].unique())

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
    (df["Country"].isin(selected_countries))
    &
    (df["InvoiceYear"].isin(selected_years))
    &
    (df["MonthName"].isin(selected_months))
]

if filtered_df.empty:
    st.warning("No records found for the selected filters.")
    st.stop()

# ==========================================================
# Product Aggregation
# ==========================================================

product_summary = (
    filtered_df
    .groupby("ProductDescription", as_index=False)
    .agg(
        Revenue=("TotalAmount", "sum"),
        Quantity=("Quantity", "sum"),
        Orders=("InvoiceID", "nunique"),
        AveragePrice=("UnitPrice", "mean"),
    )
)

product_summary = (
    product_summary
    .sort_values("Revenue", ascending=False)
    .reset_index(drop=True)
)

# ==========================================================
# KPI Calculations
# ==========================================================

total_products = product_summary.shape[0]

total_revenue = product_summary["Revenue"].sum()

total_quantity = product_summary["Quantity"].sum()

average_product_revenue = (
    total_revenue / total_products
    if total_products else 0
)

highest_revenue_product = (
    product_summary.iloc[0]["ProductDescription"]
)

highest_quantity_product = (
    product_summary
    .sort_values("Quantity", ascending=False)
    .iloc[0]["ProductDescription"]
)

# ==========================================================
# KPI Cards
# ==========================================================

st.subheader("📊 Product Overview")

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric(
    "Products",
    f"{total_products:,}"
)

kpi2.metric(
    "Revenue",
    f"£{total_revenue:,.2f}"
)

kpi3.metric(
    "Quantity Sold",
    f"{int(total_quantity):,}"
)

kpi4, kpi5, kpi6 = st.columns(3)

kpi4.metric(
    "Avg Product Revenue",
    f"£{average_product_revenue:,.2f}"
)

kpi5.metric(
    "Highest Revenue Product",
    highest_revenue_product,
)

kpi6.metric(
    "Highest Quantity Product",
    highest_quantity_product,
)

st.markdown("---")

# ==========================================================
# Top Revenue & Quantity Charts
# ==========================================================

left_chart, right_chart = st.columns(2)

with left_chart:

    st.subheader("💰 Top 10 Products by Revenue")

    top_revenue = (
        product_summary
        .head(10)
    )

    fig_top_revenue = px.bar(
        top_revenue,
        x="Revenue",
        y="ProductDescription",
        orientation="h",
        color="Revenue",
        title="Top Revenue Products",
        text_auto=".2s",
    )

    fig_top_revenue.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
        yaxis_title="",
        xaxis_title="Revenue (£)",
    )

    st.plotly_chart(
        fig_top_revenue,
        use_container_width=True,
        key="top_revenue_products",
    )


with right_chart:

    st.subheader("📦 Top 10 Products by Quantity")

    top_quantity = (
        product_summary
        .sort_values(
            "Quantity",
            ascending=False,
        )
        .head(10)
    )

    fig_top_quantity = px.bar(
        top_quantity,
        x="Quantity",
        y="ProductDescription",
        orientation="h",
        color="Quantity",
        title="Top Quantity Products",
        text_auto=True,
    )

    fig_top_quantity.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
        yaxis_title="",
    )

    st.plotly_chart(
        fig_top_quantity,
        use_container_width=True,
        key="top_quantity_products",
    )

st.markdown("---")

# ==========================================================
# Revenue vs Quantity Analysis
# ==========================================================

st.subheader("📈 Revenue vs Quantity")

fig_scatter = px.scatter(
    product_summary,
    x="Quantity",
    y="Revenue",
    hover_name="ProductDescription",
    size="Revenue",
    color="Revenue",
)

fig_scatter.update_layout(
    template="plotly_white",
    height=600,
    title="Revenue vs Quantity Sold",
    title_x=0.5,
)

st.plotly_chart(
    fig_scatter,
    use_container_width=True,
    key="revenue_quantity_scatter",
)

st.markdown("---")

# ==========================================================
# Revenue Distribution
# ==========================================================

left_hist, right_hist = st.columns(2)

with left_hist:

    st.subheader("📊 Revenue Distribution")

    fig_histogram = px.histogram(
        product_summary,
        x="Revenue",
        nbins=40,
        title="Revenue Distribution",
    )

    fig_histogram.update_layout(
        template="plotly_white",
        height=450,
        title_x=0.5,
    )

    st.plotly_chart(
        fig_histogram,
        use_container_width=True,
        key="revenue_distribution",
    )

with right_hist:

    st.subheader("📉 Pareto Analysis (80/20 Rule)")

    pareto = (
        product_summary
        .sort_values(
            "Revenue",
            ascending=False,
        )
        .copy()
    )

    pareto["CumulativeRevenue"] = (
        pareto["Revenue"].cumsum()
    )

    pareto["CumulativePercentage"] = (
        pareto["CumulativeRevenue"]
        / pareto["Revenue"].sum()
        * 100
    )

    fig_pareto = go.Figure()

    fig_pareto.add_trace(
        go.Bar(
            x=pareto["ProductDescription"],
            y=pareto["Revenue"],
            name="Revenue",
        )
    )

    fig_pareto.add_trace(
        go.Scatter(
            x=pareto["ProductDescription"],
            y=pareto["CumulativePercentage"],
            mode="lines",
            name="Cumulative %",
            yaxis="y2",
        )
    )

    fig_pareto.update_layout(
        template="plotly_white",
        height=500,
        title="Pareto Analysis",
        title_x=0.5,
        xaxis=dict(showticklabels=False),
        yaxis=dict(title="Revenue (£)"),
        yaxis2=dict(
            title="Cumulative %",
            overlaying="y",
            side="right",
            range=[0, 100],
        ),
    )

    st.plotly_chart(
        fig_pareto,
        use_container_width=True,
        key="pareto_analysis",
    )

st.markdown("---")

# ==========================================================
# Product Search
# ==========================================================

st.subheader("🔍 Product Search")

search_product = st.text_input(
    "Search Product",
    placeholder="Type product name..."
)

filtered_products = product_summary.copy()

if search_product:

    filtered_products = filtered_products[
        filtered_products["ProductDescription"]
        .str.contains(
            search_product,
            case=False,
            na=False,
        )
    ]

# ==========================================================
# Product Performance Table
# ==========================================================

st.subheader("📋 Product Performance")

display_table = (
    filtered_products
    .sort_values(
        "Revenue",
        ascending=False,
    )
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
    label="📥 Download Product Report",
    data=csv,
    file_name="product_performance.csv",
    mime="text/csv",
)

st.markdown("---")

# ==========================================================
# Business Insights
# ==========================================================

highest_revenue = (
    product_summary
    .sort_values(
        "Revenue",
        ascending=False,
    )
    .iloc[0]
)

highest_quantity = (
    product_summary
    .sort_values(
        "Quantity",
        ascending=False,
    )
    .iloc[0]
)

average_price = (
    product_summary["AveragePrice"]
    .mean()
)

top10_revenue = (
    product_summary
    .head(10)["Revenue"]
    .sum()
)

overall_revenue = (
    product_summary["Revenue"]
    .sum()
)

top10_percentage = (
    top10_revenue
    / overall_revenue
    * 100
)

active_products = (
    len(product_summary)
)

left_info, right_info = st.columns(2)

with left_info:

    st.success(
        f"""
### 💰 Revenue Insights

Highest Revenue Product

**{highest_revenue['ProductDescription']}**

Revenue

**£{highest_revenue['Revenue']:,.2f}**

Average Product Price

**£{average_price:,.2f}**
"""
    )

with right_info:

    st.success(
        f"""
### 📦 Product Insights

Highest Quantity Product

**{highest_quantity['ProductDescription']}**

Units Sold

**{int(highest_quantity['Quantity']):,}**

Active Products

**{active_products:,}**

Top 10 Products contribute

**{top10_percentage:.2f}%**

of total revenue.
"""
    )

st.markdown("---")

# ==========================================================
# Executive Summary
# ==========================================================

st.info(
    f"""
### 📊 Executive Summary

• Products Analysed : **{active_products:,}**

• Revenue Generated : **£{overall_revenue:,.2f}**

• Units Sold : **{int(total_quantity):,}**

• Average Product Revenue :
**£{average_product_revenue:,.2f}**

• Top Product :
**{highest_revenue['ProductDescription']}**
"""
)

st.markdown("---")

# ==========================================================
# Footer
# ==========================================================

st.caption(
    """
RetailPulse

Product Performance Dashboard

Notebook Outputs : Read Only

Dataset : retail_cleaned.csv

Version : 1.0
"""
)