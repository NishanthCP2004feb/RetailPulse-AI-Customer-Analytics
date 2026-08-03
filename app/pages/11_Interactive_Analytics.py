# ==========================================================
# Imports
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.theme import load_css

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Interactive Analytics",
    page_icon="📊",
    layout="wide",
)

load_css()

# ==========================================================
# Header
# ==========================================================

st.title("📊 Interactive Analytics")

st.caption(
    "RetailPulse • Self-Service Business Analytics"
)

st.markdown("---")

# ==========================================================
# Load Dataset
# ==========================================================

@st.cache_data
def load_data():

    df = pd.read_csv(
        "data/processed/analysis_data.csv"
    )

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"]
    )

    return df

df = load_data()

if df.empty:
    st.error("Analysis dataset not found.")
    st.stop()

# ==========================================================
# Sidebar Filters
# ==========================================================

st.sidebar.header("🔎 Interactive Filters")

countries = sorted(
    df["Country"].dropna().unique()
)

selected_countries = st.sidebar.multiselect(
    "Country",
    countries,
    default=countries,
)

years = sorted(
    df["InvoiceYear"].unique()
)

selected_years = st.sidebar.multiselect(
    "Invoice Year",
    years,
    default=years,
)

filtered_df = df[
    (df["Country"].isin(selected_countries))
    &
    (df["InvoiceYear"].isin(selected_years))
]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# ==========================================================
# KPI Cards
# ==========================================================

st.subheader("📈 Interactive Overview")

k1, k2, k3 = st.columns(3)

k1.metric(
    "Revenue",
    f"£{filtered_df['TotalAmount'].sum():,.2f}"
)

k2.metric(
    "Orders",
    f"{filtered_df['InvoiceID'].nunique():,}"
)

k3.metric(
    "Customers",
    f"{filtered_df['CustomerID'].nunique():,}"
)

k4, k5, k6 = st.columns(3)

k4.metric(
    "Products",
    f"{filtered_df['StockCode'].nunique():,}"
)

k5.metric(
    "Countries",
    f"{filtered_df['Country'].nunique():,}"
)

k6.metric(
    "Average Basket",
    f"£{filtered_df['BasketValue'].mean():,.2f}"
)

st.markdown("---")

# ==========================================================
# Interactive Chart Builder
# ==========================================================

st.subheader("📊 Interactive Chart Builder")

numeric_columns = [
    "Quantity",
    "UnitPrice",
    "TotalAmount",
    "BasketSize",
    "BasketValue",
]

dimension_columns = [
    "Country",
    "MonthName",
    "InvoiceYear",
    "InvoiceQuarter",
    "DayName",
]

left_control, right_control = st.columns(2)

with left_control:

    selected_dimension = st.selectbox(
        "Group By",
        dimension_columns,
    )

with right_control:

    selected_metric = st.selectbox(
        "Metric",
        numeric_columns,
        index=2,
    )

summary_df = (
    filtered_df
    .groupby(selected_dimension, as_index=False)[selected_metric]
    .sum()
)

fig_builder = px.bar(
    summary_df,
    x=selected_dimension,
    y=selected_metric,
    color=selected_metric,
    text_auto=".2s",
    title=f"{selected_metric} by {selected_dimension}"
)

fig_builder.update_layout(
    template="plotly_white",
    height=500,
    title_x=0.5,
)

st.plotly_chart(
    fig_builder,
    use_container_width=True,
    key="interactive_chart_builder",
)

st.markdown("---")

# ==========================================================
# Monthly Revenue Trend
# ==========================================================

st.subheader("📈 Monthly Revenue Trend")

monthly_sales = (
    filtered_df
    .groupby(
        "InvoiceMonthYear",
        as_index=False
    )["TotalAmount"]
    .sum()
)

fig_monthly = px.line(
    monthly_sales,
    x="InvoiceMonthYear",
    y="TotalAmount",
    markers=True,
    title="Monthly Revenue"
)

fig_monthly.update_layout(
    template="plotly_white",
    height=500,
    title_x=0.5,
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True,
    key="interactive_monthly_sales",
)

st.markdown("---")

# ==========================================================
# Country Revenue
# ==========================================================

left_country, right_product = st.columns(2)

with left_country:

    st.subheader("🌍 Revenue by Country")

    country_sales = (
        filtered_df
        .groupby("Country", as_index=False)
        ["TotalAmount"]
        .sum()
        .sort_values(
            "TotalAmount",
            ascending=False,
        )
        .head(10)
    )

    fig_country = px.bar(
        country_sales,
        x="TotalAmount",
        y="Country",
        orientation="h",
        color="TotalAmount",
        text_auto=".2s",
        title="Top Countries"
    )

    fig_country.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
        yaxis_title=""
    )

    st.plotly_chart(
        fig_country,
        use_container_width=True,
        key="interactive_country_sales",
    )

with right_product:

    st.subheader("📦 Top Products")

    product_sales = (
        filtered_df
        .groupby(
            "ProductDescription",
            as_index=False
        )["TotalAmount"]
        .sum()
        .sort_values(
            "TotalAmount",
            ascending=False,
        )
        .head(10)
    )

    fig_products = px.bar(
        product_sales,
        x="TotalAmount",
        y="ProductDescription",
        orientation="h",
        color="TotalAmount",
        text_auto=".2s",
        title="Top Products"
    )

    fig_products.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
        yaxis_title=""
    )

    st.plotly_chart(
        fig_products,
        use_container_width=True,
        key="interactive_products",
    )

st.markdown("---")

# ==========================================================
# Advanced Interactive Filters
# ==========================================================

st.subheader("🔎 Advanced Exploration")

left_filter, right_filter = st.columns(2)

with left_filter:

    search_product = st.text_input(
        "Search Product",
        placeholder="Enter product name..."
    )

with right_filter:

    search_customer = st.text_input(
        "Search Customer ID",
        placeholder="Enter customer ID..."
    )

explore_df = filtered_df.copy()

if search_product:

    explore_df = explore_df[
        explore_df["ProductDescription"]
        .astype(str)
        .str.contains(
            search_product,
            case=False,
            na=False,
        )
    ]

if search_customer:

    explore_df = explore_df[
        explore_df["CustomerID"]
        .astype(str)
        .str.contains(
            search_customer,
            case=False,
            na=False,
        )
    ]

date_range = st.date_input(
    "Invoice Date Range",
    value=(
        explore_df["InvoiceDate"].min().date(),
        explore_df["InvoiceDate"].max().date(),
    ),
)

if len(date_range) == 2:

    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])

    explore_df = explore_df[
        (
            explore_df["InvoiceDate"] >= start_date
        )
        &
        (
            explore_df["InvoiceDate"] <= end_date
        )
    ]

if explore_df.empty:
    st.warning("No records found for the selected filters.")
    st.stop()

st.markdown("---")

# ==========================================================
# Pivot Style Summary
# ==========================================================

st.subheader("📋 Interactive Summary")

summary_table = (
    explore_df
    .groupby(
        ["Country", "InvoiceYear"],
        as_index=False
    )
    .agg(
        Revenue=("TotalAmount", "sum"),
        Orders=("InvoiceID", "nunique"),
        Customers=("CustomerID", "nunique"),
    )
)

st.dataframe(
    summary_table,
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")

# ==========================================================
# Country × Month Heatmap
# ==========================================================

st.subheader("🌡️ Revenue Heatmap")

heatmap = (
    explore_df
    .pivot_table(
        values="TotalAmount",
        index="Country",
        columns="MonthName",
        aggfunc="sum",
        fill_value=0,
    )
)

fig_heatmap = px.imshow(
    heatmap,
    aspect="auto",
    text_auto=".1f",
    title="Revenue Heatmap"
)

fig_heatmap.update_layout(
    template="plotly_white",
    height=650,
    title_x=0.5,
)

st.plotly_chart(
    fig_heatmap,
    use_container_width=True,
    key="interactive_heatmap"
)

st.markdown("---")

# ==========================================================
# Hourly Sales Analysis
# ==========================================================

st.subheader("🕒 Hourly Sales")

hourly_sales = (
    explore_df
    .groupby(
        "InvoiceHour",
        as_index=False
    )["TotalAmount"]
    .sum()
)

fig_hour = px.line(
    hourly_sales,
    x="InvoiceHour",
    y="TotalAmount",
    markers=True,
    title="Sales by Hour"
)

fig_hour.update_layout(
    template="plotly_white",
    height=450,
    title_x=0.5,
    xaxis_title="Hour of Day",
    yaxis_title="Revenue (£)"
)

st.plotly_chart(
    fig_hour,
    use_container_width=True,
    key="interactive_hourly_sales"
)

st.markdown("---")

# ==========================================================
# Weekend vs Weekday Analysis
# ==========================================================

st.subheader("📅 Weekend vs Weekday Sales")

weekend_summary = (
    explore_df
    .groupby("IsWeekend", as_index=False)
    .agg(
        Revenue=("TotalAmount", "sum"),
        Orders=("InvoiceID", "nunique"),
    )
)

weekend_summary["DayType"] = weekend_summary["IsWeekend"].map(
    {
        True: "Weekend",
        False: "Weekday",
    }
)

left_weekend, right_weekend = st.columns(2)

with left_weekend:

    fig_weekend = px.bar(
        weekend_summary,
        x="DayType",
        y="Revenue",
        color="Revenue",
        text_auto=".2s",
        title="Revenue Comparison"
    )

    fig_weekend.update_layout(
        template="plotly_white",
        height=450,
        title_x=0.5,
    )

    st.plotly_chart(
        fig_weekend,
        use_container_width=True,
        key="interactive_weekend_revenue"
    )

with right_weekend:

    fig_weekend_orders = px.bar(
        weekend_summary,
        x="DayType",
        y="Orders",
        color="Orders",
        text_auto=True,
        title="Order Comparison"
    )

    fig_weekend_orders.update_layout(
        template="plotly_white",
        height=450,
        title_x=0.5,
    )

    st.plotly_chart(
        fig_weekend_orders,
        use_container_width=True,
        key="interactive_weekend_orders"
    )

st.markdown("---")

# ==========================================================
# Basket Value Analysis
# ==========================================================

left_basket, right_basket = st.columns(2)

with left_basket:

    st.subheader("🛒 Basket Value Distribution")

    fig_basket = px.histogram(
        explore_df,
        x="BasketValue",
        nbins=30,
        title="Basket Value Distribution"
    )

    fig_basket.update_layout(
        template="plotly_white",
        height=450,
        title_x=0.5,
    )

    st.plotly_chart(
        fig_basket,
        use_container_width=True,
        key="interactive_basket_distribution"
    )

with right_basket:

    st.subheader("📦 Basket Size vs Basket Value")

    fig_basket_scatter = px.scatter(
        explore_df,
        x="BasketSize",
        y="BasketValue",
        color="Country",
        hover_name="ProductDescription",
        title="Basket Size vs Basket Value"
    )

    fig_basket_scatter.update_layout(
        template="plotly_white",
        height=450,
        title_x=0.5,
    )

    st.plotly_chart(
        fig_basket_scatter,
        use_container_width=True,
        key="interactive_basket_scatter"
    )

st.markdown("---")

# ==========================================================
# Country Comparison Dashboard
# ==========================================================

st.subheader("🌍 Country Comparison")

country_compare = (
    explore_df
    .groupby("Country", as_index=False)
    .agg(
        Revenue=("TotalAmount", "sum"),
        Customers=("CustomerID", "nunique"),
        Orders=("InvoiceID", "nunique"),
    )
)

fig_country_compare = px.scatter(
    country_compare,
    x="Customers",
    y="Revenue",
    size="Orders",
    color="Revenue",
    hover_name="Country",
    title="Country Performance Comparison"
)

fig_country_compare.update_layout(
    template="plotly_white",
    height=550,
    title_x=0.5,
)

st.plotly_chart(
    fig_country_compare,
    use_container_width=True,
    key="interactive_country_comparison"
)

st.markdown("---")

# ==========================================================
# Revenue vs Quantity Analysis
# ==========================================================

st.subheader("📊 Revenue vs Quantity")

product_analysis = (
    explore_df
    .groupby(
        "ProductDescription",
        as_index=False
    )
    .agg(
        Revenue=("TotalAmount", "sum"),
        Quantity=("Quantity", "sum"),
    )
)

fig_product_analysis = px.scatter(
    product_analysis,
    x="Quantity",
    y="Revenue",
    color="Revenue",
    size="Revenue",
    hover_name="ProductDescription",
    title="Revenue vs Quantity"
)

fig_product_analysis.update_layout(
    template="plotly_white",
    height=550,
    title_x=0.5,
)

st.plotly_chart(
    fig_product_analysis,
    use_container_width=True,
    key="interactive_product_analysis"
)

st.markdown("---")

# ==========================================================
# Export Filtered Dataset
# ==========================================================

st.subheader("📥 Export Filtered Dataset")

export_csv = (
    explore_df
    .to_csv(index=False)
    .encode("utf-8")
)

st.download_button(
    label="📥 Download Filtered Dataset",
    data=export_csv,
    file_name="interactive_filtered_data.csv",
    mime="text/csv",
)

st.markdown("---")

# ==========================================================
# Interactive Executive Summary
# ==========================================================

st.subheader("📊 Interactive Executive Summary")

summary_left, summary_right = st.columns(2)

with summary_left:

    st.info(
        f"""
### Business Overview

Revenue

**£{explore_df['TotalAmount'].sum():,.2f}**

Orders

**{explore_df['InvoiceID'].nunique():,}**

Customers

**{explore_df['CustomerID'].nunique():,}**

Products

**{explore_df['StockCode'].nunique():,}**
"""
    )

with summary_right:

    st.info(
        f"""
### Sales Performance

Average Basket Value

**£{explore_df['BasketValue'].mean():,.2f}**

Average Basket Size

**{explore_df['BasketSize'].mean():.2f}**

Countries

**{explore_df['Country'].nunique()}**

Analysis Period

**{explore_df['InvoiceYear'].min()} - {explore_df['InvoiceYear'].max()}**
"""
    )

st.markdown("---")

# ==========================================================
# Data Quality Dashboard
# ==========================================================

st.subheader("📈 Data Quality Summary")

missing_values = int(explore_df.isna().sum().sum())

duplicate_rows = int(explore_df.duplicated().sum())

quality_col1, quality_col2, quality_col3 = st.columns(3)

quality_col1.metric(
    "Rows",
    f"{len(explore_df):,}"
)

quality_col2.metric(
    "Missing Values",
    f"{missing_values:,}"
)

quality_col3.metric(
    "Duplicate Rows",
    f"{duplicate_rows:,}"
)

st.markdown("---")

# ==========================================================
# Dashboard User Guide
# ==========================================================

st.subheader("📘 Dashboard User Guide")

st.markdown("""
### How to Use

- Use the sidebar filters to narrow the dataset.
- Build custom charts using the Interactive Chart Builder.
- Search for products or customers.
- Explore country, time, and basket-level analytics.
- Export the filtered dataset for additional analysis.

This dashboard is designed for interactive business exploration using the processed dataset generated by the notebook pipeline.
""")

st.markdown("---")

# ==========================================================
# Footer
# ==========================================================

st.caption(
    """
RetailPulse

Interactive Analytics Dashboard

Data Source:
analysis_data.csv

Notebook Outputs : Read Only

Version : 1.0
"""
)