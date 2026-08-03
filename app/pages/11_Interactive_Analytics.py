import streamlit as st
import pandas as pd
import plotly.express as px

from utils.theme import (
    load_css,
    page_header,
    section_header,
    dashboard_divider,
    dashboard_footer,
    render_kpi_row,
    render_insight_card,
)
from utils.data_loader import load_analysis_data
from utils.helpers import format_currency, format_number
from utils.metrics import get_sales_kpis, get_basket_kpis, get_dataset_summary
from utils.chart_utils import (
    create_bar_chart,
    create_horizontal_bar_chart,
    create_line_chart,
    create_scatter_chart,
    create_histogram,
    create_heatmap,
)

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

page_header("📊 Interactive Analytics", "RetailPulse • Self-Service Business Analytics")

dashboard_divider()

# ==========================================================
# Load Dataset
# ==========================================================

df = load_analysis_data()

if df.empty:
    st.error("Analysis dataset not found.")
    st.stop()

# ==========================================================
# Sidebar Filters
# ==========================================================

st.sidebar.header("🔎 Interactive Filters")

countries = sorted(df["Country"].dropna().unique())
selected_countries = st.sidebar.multiselect("Country", countries, default=countries)

years = sorted(df["InvoiceYear"].unique())
selected_years = st.sidebar.multiselect("Invoice Year", years, default=years)

filtered_df = df[
    (df["Country"].isin(selected_countries)) &
    (df["InvoiceYear"].isin(selected_years))
]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# ==========================================================
# KPI Cards
# ==========================================================

section_header("📈 Interactive Overview")

sales_kpis = get_sales_kpis(filtered_df)
basket_kpis = get_basket_kpis(filtered_df)

render_kpi_row([
    {"title": "Revenue", "value": format_currency(sales_kpis["Revenue"]), "icon": "💰"},
    {"title": "Orders", "value": format_number(sales_kpis["Orders"]), "icon": "📦"},
    {"title": "Customers", "value": format_number(filtered_df["CustomerID"].nunique()), "icon": "👥"}
])

render_kpi_row([
    {"title": "Products", "value": format_number(filtered_df["StockCode"].nunique()), "icon": "🏷️"},
    {"title": "Countries", "value": format_number(filtered_df["Country"].nunique()), "icon": "🌍"},
    {"title": "Average Basket", "value": format_currency(basket_kpis["Average Basket Value"]), "icon": "🛒"}
])

dashboard_divider()

# ==========================================================
# Interactive Chart Builder
# ==========================================================

section_header("📊 Interactive Chart Builder")

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
    selected_dimension = st.selectbox("Group By", dimension_columns)

with right_control:
    selected_metric = st.selectbox("Metric", numeric_columns, index=2)

summary_df = (
    filtered_df.groupby(selected_dimension, as_index=False)[selected_metric].sum()
)

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
fig_builder = create_bar_chart(
    summary_df,
    x=selected_dimension,
    y=selected_metric,
    title=f"{selected_metric} by {selected_dimension}",
    color=selected_metric,
    text_auto=".2s"
)
st.plotly_chart(fig_builder, use_container_width=True, key="interactive_chart_builder")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Monthly Revenue Trend
# ==========================================================

section_header("📈 Monthly Revenue Trend")

monthly_sales = (
    filtered_df.groupby("InvoiceMonthYear", as_index=False)["TotalAmount"].sum()
)

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
fig_monthly = create_line_chart(
    monthly_sales,
    x="InvoiceMonthYear",
    y="TotalAmount",
    title="Monthly Revenue",
    markers=True
)
st.plotly_chart(fig_monthly, use_container_width=True, key="interactive_monthly_sales")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Country Revenue
# ==========================================================

left_country, right_product = st.columns(2)

with left_country:
    section_header("🌍 Revenue by Country")
    
    country_sales = (
        filtered_df.groupby("Country", as_index=False)["TotalAmount"].sum()
        .sort_values("TotalAmount", ascending=False).head(10)
    )

    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    fig_country = create_horizontal_bar_chart(
        country_sales,
        x="TotalAmount",
        y="Country",
        title="Top Countries",
        color="TotalAmount",
        text_auto=".2s"
    )
    st.plotly_chart(fig_country, use_container_width=True, key="interactive_country_sales")
    st.markdown('</div>', unsafe_allow_html=True)

with right_product:
    section_header("📦 Top Products")
    
    product_sales = (
        filtered_df.groupby("ProductDescription", as_index=False)["TotalAmount"].sum()
        .sort_values("TotalAmount", ascending=False).head(10)
    )

    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    fig_products = create_horizontal_bar_chart(
        product_sales,
        x="TotalAmount",
        y="ProductDescription",
        title="Top Products",
        color="TotalAmount",
        text_auto=".2s"
    )
    st.plotly_chart(fig_products, use_container_width=True, key="interactive_products")
    st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Advanced Interactive Filters
# ==========================================================

section_header("🔎 Advanced Exploration")

left_filter, right_filter = st.columns(2)

with left_filter:
    search_product = st.text_input("Search Product", placeholder="Enter product name...")

with right_filter:
    search_customer = st.text_input("Search Customer ID", placeholder="Enter customer ID...")

explore_df = filtered_df.copy()

if search_product:
    explore_df = explore_df[
        explore_df["ProductDescription"].astype(str).str.contains(search_product, case=False, na=False)
    ]

if search_customer:
    explore_df = explore_df[
        explore_df["CustomerID"].astype(str).str.contains(search_customer, case=False, na=False)
    ]

date_range = st.date_input(
    "Invoice Date Range",
    value=(explore_df["InvoiceDate"].min().date(), explore_df["InvoiceDate"].max().date()),
)

if len(date_range) == 2:
    start_date = pd.Timestamp(date_range[0])
    end_date = pd.Timestamp(date_range[1])
    explore_df = explore_df[
        (explore_df["InvoiceDate"] >= start_date) &
        (explore_df["InvoiceDate"] <= end_date)
    ]

if explore_df.empty:
    st.warning("No records found for the selected filters.")
    st.stop()

dashboard_divider()

# ==========================================================
# Pivot Style Summary
# ==========================================================

section_header("📋 Interactive Summary")

summary_table = (
    explore_df.groupby(["Country", "InvoiceYear"], as_index=False)
    .agg(
        Revenue=("TotalAmount", "sum"),
        Orders=("InvoiceID", "nunique"),
        Customers=("CustomerID", "nunique"),
    )
)

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
st.dataframe(summary_table, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Country × Month Heatmap
# ==========================================================

section_header("🌡️ Revenue Heatmap")

heatmap = (
    explore_df.pivot_table(
        values="TotalAmount",
        index="Country",
        columns="MonthName",
        aggfunc="sum",
        fill_value=0,
    )
)

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
fig_heatmap = create_heatmap(heatmap, title="Revenue Heatmap")
fig_heatmap.update_layout(height=650)
st.plotly_chart(fig_heatmap, use_container_width=True, key="interactive_heatmap")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Hourly Sales Analysis
# ==========================================================

section_header("🕒 Hourly Sales")

hourly_sales = explore_df.groupby("InvoiceHour", as_index=False)["TotalAmount"].sum()

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
fig_hour = create_line_chart(
    hourly_sales,
    x="InvoiceHour",
    y="TotalAmount",
    title="Sales by Hour",
    markers=True
)
fig_hour.update_layout(xaxis_title="Hour of Day", yaxis_title="Revenue (£)")
st.plotly_chart(fig_hour, use_container_width=True, key="interactive_hourly_sales")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Weekend vs Weekday Analysis
# ==========================================================

section_header("📅 Weekend vs Weekday Sales")

weekend_summary = (
    explore_df.groupby("IsWeekend", as_index=False)
    .agg(Revenue=("TotalAmount", "sum"), Orders=("InvoiceID", "nunique"))
)
weekend_summary["DayType"] = weekend_summary["IsWeekend"].map({True: "Weekend", False: "Weekday"})

left_weekend, right_weekend = st.columns(2)

with left_weekend:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    fig_weekend = create_bar_chart(
        weekend_summary,
        x="DayType",
        y="Revenue",
        title="Revenue Comparison",
        color="Revenue",
        text_auto=".2s"
    )
    st.plotly_chart(fig_weekend, use_container_width=True, key="interactive_weekend_revenue")
    st.markdown('</div>', unsafe_allow_html=True)

with right_weekend:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    fig_weekend_orders = create_bar_chart(
        weekend_summary,
        x="DayType",
        y="Orders",
        title="Order Comparison",
        color="Orders",
        text_auto=".2s"
    )
    st.plotly_chart(fig_weekend_orders, use_container_width=True, key="interactive_weekend_orders")
    st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Basket Value Analysis
# ==========================================================

left_basket, right_basket = st.columns(2)

with left_basket:
    section_header("🛒 Basket Value Distribution")
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    fig_basket = create_histogram(explore_df, x="BasketValue", nbins=30, title="Basket Value Distribution")
    st.plotly_chart(fig_basket, use_container_width=True, key="interactive_basket_distribution")
    st.markdown('</div>', unsafe_allow_html=True)

with right_basket:
    section_header("📦 Basket Size vs Basket Value")
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    fig_basket_scatter = create_scatter_chart(
        explore_df,
        x="BasketSize",
        y="BasketValue",
        color="Country",
        hover_name="ProductDescription",
        title="Basket Size vs Basket Value"
    )
    st.plotly_chart(fig_basket_scatter, use_container_width=True, key="interactive_basket_scatter")
    st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Country Comparison Dashboard
# ==========================================================

section_header("🌍 Country Comparison")

country_compare = (
    explore_df.groupby("Country", as_index=False)
    .agg(Revenue=("TotalAmount", "sum"), Customers=("CustomerID", "nunique"), Orders=("InvoiceID", "nunique"))
)

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
fig_country_compare = create_scatter_chart(
    country_compare,
    x="Customers",
    y="Revenue",
    size="Orders",
    color="Revenue",
    hover_name="Country",
    title="Country Performance Comparison"
)
fig_country_compare.update_layout(height=550)
st.plotly_chart(fig_country_compare, use_container_width=True, key="interactive_country_comparison")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Revenue vs Quantity Analysis
# ==========================================================

section_header("📊 Revenue vs Quantity")

product_analysis = (
    explore_df.groupby("ProductDescription", as_index=False)
    .agg(Revenue=("TotalAmount", "sum"), Quantity=("Quantity", "sum"))
)

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
fig_product_analysis = create_scatter_chart(
    product_analysis,
    x="Quantity",
    y="Revenue",
    color="Revenue",
    size="Revenue",
    hover_name="ProductDescription",
    title="Revenue vs Quantity"
)
fig_product_analysis.update_layout(height=550)
st.plotly_chart(fig_product_analysis, use_container_width=True, key="interactive_product_analysis")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Interactive Executive Summary
# ==========================================================

section_header("📊 Interactive Executive Summary")

summary_left, summary_right = st.columns(2)

with summary_left:
    render_insight_card(
        "Business Overview",
        [
            f"**Revenue:** {format_currency(explore_df['TotalAmount'].sum())}",
            f"**Orders:** {format_number(explore_df['InvoiceID'].nunique())}",
            f"**Customers:** {format_number(explore_df['CustomerID'].nunique())}",
            f"**Products:** {format_number(explore_df['StockCode'].nunique())}"
        ],
        card_type="info"
    )

with summary_right:
    render_insight_card(
        "Sales Performance",
        [
            f"**Average Basket Value:** {format_currency(explore_df['BasketValue'].mean())}",
            f"**Average Basket Size:** {format_number(explore_df['BasketSize'].mean())}",
            f"**Countries:** {format_number(explore_df['Country'].nunique())}",
            f"**Analysis Period:** {explore_df['InvoiceYear'].min()} - {explore_df['InvoiceYear'].max()}"
        ],
        card_type="info"
    )

dashboard_divider()

# ==========================================================
# Data Quality Dashboard
# ==========================================================

section_header("📈 Data Quality Summary")

ds_summary = get_dataset_summary(explore_df)
render_kpi_row([
    {"title": "Rows", "value": format_number(ds_summary.get("Rows", len(explore_df))), "icon": "📄"},
    {"title": "Missing Values", "value": format_number(ds_summary.get("Missing Values", int(explore_df.isna().sum().sum()))), "icon": "❓"},
    {"title": "Duplicate Rows", "value": format_number(ds_summary.get("Duplicate Rows", int(explore_df.duplicated().sum()))), "icon": "👯"}
])

dashboard_divider()

# ==========================================================
# Dashboard User Guide
# ==========================================================

section_header("📘 Dashboard User Guide")

st.markdown("""
### How to Use

- Use the sidebar filters to narrow the dataset.
- Build custom charts using the Interactive Chart Builder.
- Search for products or customers.
- Explore country, time, and basket-level analytics.
- Export the filtered dataset for additional analysis.

This dashboard is designed for interactive business exploration using the processed dataset generated by the notebook pipeline.
""")

# ==========================================================
# Export Filtered Dataset
# ==========================================================

section_header("📥 Export Filtered Dataset")

st.markdown('<div class="rp-download-btn">', unsafe_allow_html=True)
export_csv = explore_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Filtered Dataset",
    data=export_csv,
    file_name="interactive_filtered_data.csv",
    mime="text/csv",
)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Footer
# ==========================================================

dashboard_footer()