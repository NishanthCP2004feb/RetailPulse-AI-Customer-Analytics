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
    page_title="Country Analytics",
    page_icon="🌍",
    layout="wide",
)

load_css()

# ==========================================================
# Header
# ==========================================================

st.title("🌍 Country Analytics")
st.caption("RetailPulse • Country Performance Dashboard")

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

st.sidebar.header("🌍 Country Filters")

years = sorted(df["InvoiceYear"].unique())

selected_years = st.sidebar.multiselect(
    "Invoice Year",
    years,
    default=years,
)

months = sorted(df["MonthName"].unique())

selected_months = st.sidebar.multiselect(
    "Month",
    months,
    default=months,
)

filtered_df = df[
    (df["InvoiceYear"].isin(selected_years))
    &
    (df["MonthName"].isin(selected_months))
]

if filtered_df.empty:
    st.warning("No records found for selected filters.")
    st.stop()

# ==========================================================
# Country Summary
# ==========================================================

country_summary = (
    filtered_df
    .groupby("Country", as_index=False)
    .agg(
        Revenue=("TotalAmount", "sum"),
        Orders=("InvoiceID", "nunique"),
        Customers=("CustomerID", "nunique"),
        Quantity=("Quantity", "sum"),
        AvgBasket=("BasketValue", "mean"),
    )
)

country_summary["AverageOrderValue"] = (
    country_summary["Revenue"]
    / country_summary["Orders"]
)

country_summary = (
    country_summary
    .sort_values(
        "Revenue",
        ascending=False,
    )
    .reset_index(drop=True)
)

# ==========================================================
# KPI Calculations
# ==========================================================

total_countries = len(country_summary)

total_revenue = country_summary["Revenue"].sum()

total_orders = country_summary["Orders"].sum()

total_customers = country_summary["Customers"].sum()

average_country_revenue = (
    total_revenue / total_countries
    if total_countries else 0
)

top_country = country_summary.iloc[0]["Country"]

# ==========================================================
# KPI Cards
# ==========================================================

st.subheader("📊 Country Overview")

kpi1, kpi2, kpi3 = st.columns(3)

kpi1.metric(
    "Countries",
    f"{total_countries:,}"
)

kpi2.metric(
    "Revenue",
    f"£{total_revenue:,.2f}"
)

kpi3.metric(
    "Orders",
    f"{int(total_orders):,}"
)

kpi4, kpi5, kpi6 = st.columns(3)

kpi4.metric(
    "Customers",
    f"{int(total_customers):,}"
)

kpi5.metric(
    "Avg Revenue / Country",
    f"£{average_country_revenue:,.2f}"
)

kpi6.metric(
    "Top Country",
    top_country,
)

st.markdown("---")

# ==========================================================
# Revenue & Orders by Country
# ==========================================================

left_chart, right_chart = st.columns(2)

with left_chart:

    st.subheader("💰 Top Countries by Revenue")

    top_revenue = (
        country_summary
        .sort_values("Revenue", ascending=False)
        .head(10)
    )

    fig_country_revenue = px.bar(
        top_revenue,
        x="Revenue",
        y="Country",
        orientation="h",
        color="Revenue",
        text_auto=".2s",
        title="Top 10 Countries by Revenue"
    )

    fig_country_revenue.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
        yaxis_title="",
        xaxis_title="Revenue (£)"
    )

    st.plotly_chart(
        fig_country_revenue,
        use_container_width=True,
        key="country_revenue_chart"
    )

with right_chart:

    st.subheader("📦 Top Countries by Orders")

    top_orders = (
        country_summary
        .sort_values("Orders", ascending=False)
        .head(10)
    )

    fig_country_orders = px.bar(
        top_orders,
        x="Orders",
        y="Country",
        orientation="h",
        color="Orders",
        text_auto=True,
        title="Top 10 Countries by Orders"
    )

    fig_country_orders.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
        yaxis_title=""
    )

    st.plotly_chart(
        fig_country_orders,
        use_container_width=True,
        key="country_orders_chart"
    )

st.markdown("---")

# ==========================================================
# Customers & Average Order Value
# ==========================================================

left_customer, right_customer = st.columns(2)

with left_customer:

    st.subheader("👥 Customers by Country")

    top_customers = (
        country_summary
        .sort_values("Customers", ascending=False)
        .head(10)
    )

    fig_country_customers = px.bar(
        top_customers,
        x="Customers",
        y="Country",
        orientation="h",
        color="Customers",
        text_auto=True,
        title="Top Countries by Customers"
    )

    fig_country_customers.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
        yaxis_title=""
    )

    st.plotly_chart(
        fig_country_customers,
        use_container_width=True,
        key="country_customers_chart"
    )

with right_customer:

    st.subheader("💳 Average Order Value")

    top_aov = (
        country_summary
        .sort_values(
            "AverageOrderValue",
            ascending=False
        )
        .head(10)
    )

    fig_country_aov = px.bar(
        top_aov,
        x="AverageOrderValue",
        y="Country",
        orientation="h",
        color="AverageOrderValue",
        text_auto=".2s",
        title="Average Order Value"
    )

    fig_country_aov.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
        yaxis_title="",
        xaxis_title="Average Order Value (£)"
    )

    st.plotly_chart(
        fig_country_aov,
        use_container_width=True,
        key="country_aov_chart"
    )

st.markdown("---")

# ==========================================================
# Revenue vs Customers Analysis
# ==========================================================

left_scatter, right_pie = st.columns(2)

with left_scatter:

    st.subheader("📈 Revenue vs Customers")

    fig_country_scatter = px.scatter(
        country_summary,
        x="Customers",
        y="Revenue",
        size="Orders",
        color="Revenue",
        hover_name="Country",
        title="Revenue vs Customer Count",
    )

    fig_country_scatter.update_layout(
        template="plotly_white",
        height=520,
        title_x=0.5,
        xaxis_title="Customers",
        yaxis_title="Revenue (£)",
    )

    st.plotly_chart(
        fig_country_scatter,
        use_container_width=True,
        key="country_scatter_chart",
    )

# ==========================================================
# Revenue Contribution
# ==========================================================

with right_pie:

    st.subheader("🥧 Revenue Contribution")

    top_pie = country_summary.head(10).copy()

    remaining = country_summary.iloc[10:]["Revenue"].sum()

    if remaining > 0:
        top_pie.loc[len(top_pie)] = {
            "Country": "Others",
            "Revenue": remaining,
            "Orders": 0,
            "Customers": 0,
            "Quantity": 0,
            "AvgBasket": 0,
            "AverageOrderValue": 0,
        }

    fig_country_pie = px.pie(
        top_pie,
        names="Country",
        values="Revenue",
        hole=0.45,
        title="Revenue Contribution by Country",
    )

    fig_country_pie.update_layout(
        template="plotly_white",
        height=520,
        title_x=0.5,
    )

    st.plotly_chart(
        fig_country_pie,
        use_container_width=True,
        key="country_pie_chart",
    )

st.markdown("---")

# ==========================================================
# Revenue Distribution
# ==========================================================

left_hist, right_pareto = st.columns(2)

with left_hist:

    st.subheader("📊 Revenue Distribution")

    fig_country_hist = px.histogram(
        country_summary,
        x="Revenue",
        nbins=25,
        title="Country Revenue Distribution",
    )

    fig_country_hist.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
    )

    st.plotly_chart(
        fig_country_hist,
        use_container_width=True,
        key="country_histogram_chart",
    )

# ==========================================================
# Pareto Analysis
# ==========================================================

with right_pareto:

    st.subheader("📉 Pareto Analysis (80/20 Rule)")

    pareto = country_summary.copy()

    pareto["CumulativeRevenue"] = pareto["Revenue"].cumsum()

    pareto["CumulativePercent"] = (
        pareto["CumulativeRevenue"]
        / pareto["Revenue"].sum()
        * 100
    )

    fig_country_pareto = go.Figure()

    fig_country_pareto.add_trace(
        go.Bar(
            x=pareto["Country"],
            y=pareto["Revenue"],
            name="Revenue",
        )
    )

    fig_country_pareto.add_trace(
        go.Scatter(
            x=pareto["Country"],
            y=pareto["CumulativePercent"],
            mode="lines+markers",
            name="Cumulative %",
            yaxis="y2",
        )
    )

    fig_country_pareto.update_layout(
        template="plotly_white",
        title="Country Pareto Analysis",
        title_x=0.5,
        height=500,
        xaxis=dict(showticklabels=False),
        yaxis=dict(title="Revenue (£)"),
        yaxis2=dict(
            overlaying="y",
            side="right",
            range=[0, 100],
            title="Cumulative %",
        ),
    )

    st.plotly_chart(
        fig_country_pareto,
        use_container_width=True,
        key="country_pareto_chart",
    )

st.markdown("---")

# ==========================================================
# Country Search
# ==========================================================

st.subheader("🔍 Country Search")

search_country = st.text_input(
    "Search Country",
    placeholder="Enter country name..."
)

display_table = country_summary.copy()

if search_country:

    display_table = display_table[
        display_table["Country"]
        .str.contains(
            search_country,
            case=False,
            na=False,
        )
    ]

# ==========================================================
# Country Summary Table
# ==========================================================

st.subheader("📋 Country Summary")

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
    label="📥 Download Country Report",
    data=csv,
    file_name="country_analytics.csv",
    mime="text/csv",
)

st.markdown("---")

# ==========================================================
# Business Insights
# ==========================================================

highest_revenue_country = (
    country_summary
    .sort_values("Revenue", ascending=False)
    .iloc[0]
)

highest_orders_country = (
    country_summary
    .sort_values("Orders", ascending=False)
    .iloc[0]
)

highest_customer_country = (
    country_summary
    .sort_values("Customers", ascending=False)
    .iloc[0]
)

average_order_value = (
    country_summary["AverageOrderValue"]
    .mean()
)

active_countries = len(country_summary)

top5_revenue = (
    country_summary
    .head(5)["Revenue"]
    .sum()
)

total_revenue_all = (
    country_summary["Revenue"]
    .sum()
)

top5_percentage = (
    top5_revenue
    / total_revenue_all
    * 100
)

left_info, right_info = st.columns(2)

with left_info:

    st.success(
        f"""
### 💰 Revenue Insights

Highest Revenue Country

**{highest_revenue_country['Country']}**

Revenue

**£{highest_revenue_country['Revenue']:,.2f}**

Average Order Value

**£{average_order_value:,.2f}**
"""
    )

with right_info:

    st.success(
        f"""
### 🌍 Country Insights

Most Orders

**{highest_orders_country['Country']}**

Most Customers

**{highest_customer_country['Country']}**

Active Countries

**{active_countries}**

Top 5 Countries contribute

**{top5_percentage:.2f}%**

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

• Countries Analysed

**{active_countries:,}**

• Total Revenue

**£{total_revenue:,.2f}**

• Total Orders

**{int(total_orders):,}**

• Total Customers

**{int(total_customers):,}**

• Highest Revenue Country

**{highest_revenue_country['Country']}**
"""
)

st.markdown("---")

# ==========================================================
# Footer
# ==========================================================

st.caption(
    """
RetailPulse

Country Analytics Dashboard

Notebook Outputs : Read Only

Dataset : retail_cleaned.csv

Version : 1.0
"""
)