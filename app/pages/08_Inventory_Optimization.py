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
    page_title="Inventory Optimization",
    page_icon="📦",
    layout="wide",
)

load_css()

# ==========================================================
# Header
# ==========================================================

st.title("📦 Inventory Optimization")

st.caption(
    "RetailPulse • Inventory Intelligence Dashboard"
)

st.markdown("---")

# ==========================================================
# Load Reports
# ==========================================================

@st.cache_data
def load_inventory_reports():

    summary_df = pd.read_csv(
        "reports/inventory_summary.csv"
    )

    recommendation_df = pd.read_csv(
        "reports/inventory_recommendations.csv"
    )

    return summary_df, recommendation_df


summary_df, recommendation_df = load_inventory_reports()

if summary_df.empty:
    st.error("Inventory report not found.")
    st.stop()

# ==========================================================
# Sidebar Filters
# ==========================================================

st.sidebar.header("📦 Inventory Filters")

status_options = sorted(
    summary_df["InventoryStatus"].unique()
)

selected_status = st.sidebar.multiselect(
    "Inventory Status",
    status_options,
    default=status_options,
)

recommendation_options = sorted(
    summary_df["Recommendation"].unique()
)

selected_recommendation = st.sidebar.multiselect(
    "Recommendation",
    recommendation_options,
    default=recommendation_options,
)

filtered_df = summary_df[
    (
        summary_df["InventoryStatus"]
        .isin(selected_status)
    )
    &
    (
        summary_df["Recommendation"]
        .isin(selected_recommendation)
    )
]

if filtered_df.empty:
    st.warning("No products found.")
    st.stop()

# ==========================================================
# KPI Calculations
# ==========================================================

total_products = len(filtered_df)

total_quantity = (
    filtered_df["TotalQuantity"].sum()
)

total_revenue = (
    filtered_df["TotalRevenue"].sum()
)

total_orders = (
    filtered_df["TotalOrders"].sum()
)

average_revenue = (
    filtered_df["TotalRevenue"].mean()
)

high_demand_products = (
    (
        filtered_df["InventoryStatus"]
        == "High Demand"
    ).sum()
)

# ==========================================================
# KPI Cards
# ==========================================================

st.subheader("📊 Inventory Overview")

k1, k2, k3 = st.columns(3)

k1.metric(
    "Products",
    f"{total_products:,}"
)

k2.metric(
    "Quantity",
    f"{int(total_quantity):,}"
)

k3.metric(
    "Revenue",
    f"£{total_revenue:,.2f}"
)

k4, k5, k6 = st.columns(3)

k4.metric(
    "Orders",
    f"{int(total_orders):,}"
)

k5.metric(
    "Average Revenue",
    f"£{average_revenue:,.2f}"
)

k6.metric(
    "High Demand",
    f"{high_demand_products:,}"
)

st.markdown("---")

# ==========================================================
# Inventory Status Distribution
# ==========================================================

left_chart, right_chart = st.columns(2)

with left_chart:

    st.subheader("📊 Inventory Status Distribution")

    status_distribution = (
        filtered_df["InventoryStatus"]
        .value_counts()
        .reset_index()
    )

    status_distribution.columns = [
        "InventoryStatus",
        "Products",
    ]

    fig_inventory_status = px.pie(
        status_distribution,
        names="InventoryStatus",
        values="Products",
        hole=0.45,
        title="Inventory Status"
    )

    fig_inventory_status.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
    )

    st.plotly_chart(
        fig_inventory_status,
        use_container_width=True,
        key="inventory_status_chart"
    )

# ==========================================================
# Recommendation Distribution
# ==========================================================

with right_chart:

    st.subheader("💡 Recommendation Distribution")

    recommendation_distribution = (
        filtered_df["Recommendation"]
        .value_counts()
        .reset_index()
    )

    recommendation_distribution.columns = [
        "Recommendation",
        "Products",
    ]

    fig_recommendation = px.bar(
        recommendation_distribution,
        x="Recommendation",
        y="Products",
        color="Products",
        text_auto=True,
        title="Inventory Recommendations"
    )

    fig_recommendation.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
        xaxis_title="Recommendation",
        yaxis_title="Products"
    )

    st.plotly_chart(
        fig_recommendation,
        use_container_width=True,
        key="recommendation_distribution_chart"
    )

st.markdown("---")

# ==========================================================
# Top Products
# ==========================================================

left_products, right_products = st.columns(2)

with left_products:

    st.subheader("📦 Top Products by Quantity")

    top_quantity = (
        filtered_df
        .sort_values(
            "TotalQuantity",
            ascending=False
        )
        .head(10)
    )

    fig_quantity = px.bar(
        top_quantity,
        x="TotalQuantity",
        y="ProductDescription",
        orientation="h",
        color="TotalQuantity",
        text_auto=True,
        title="Highest Quantity Products"
    )

    fig_quantity.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
        yaxis_title=""
    )

    st.plotly_chart(
        fig_quantity,
        use_container_width=True,
        key="inventory_quantity_chart"
    )

with right_products:

    st.subheader("💰 Top Products by Revenue")

    top_revenue = (
        filtered_df
        .sort_values(
            "TotalRevenue",
            ascending=False
        )
        .head(10)
    )

    fig_revenue = px.bar(
        top_revenue,
        x="TotalRevenue",
        y="ProductDescription",
        orientation="h",
        color="TotalRevenue",
        text_auto=".2s",
        title="Highest Revenue Products"
    )

    fig_revenue.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
        yaxis_title="",
        xaxis_title="Revenue (£)"
    )

    st.plotly_chart(
        fig_revenue,
        use_container_width=True,
        key="inventory_revenue_chart"
    )

st.markdown("---")

# ==========================================================
# Orders by Product
# ==========================================================

st.subheader("📈 Top Products by Orders")

top_orders = (
    filtered_df
    .sort_values(
        "TotalOrders",
        ascending=False
    )
    .head(15)
)

fig_orders = px.bar(
    top_orders,
    x="ProductDescription",
    y="TotalOrders",
    color="TotalOrders",
    text_auto=True,
    title="Top Ordered Products"
)

fig_orders.update_layout(
    template="plotly_white",
    height=500,
    title_x=0.5,
    xaxis_title="Product",
    yaxis_title="Orders",
)

st.plotly_chart(
    fig_orders,
    use_container_width=True,
    key="inventory_orders_chart"
)

st.markdown("---")

# ==========================================================
# Product Search
# ==========================================================

st.subheader("🔍 Product Search")

search_product = st.text_input(
    "Search Product",
    placeholder="Enter product name or stock code..."
)

display_df = filtered_df.copy()

if search_product:

    display_df = display_df[
        (
            display_df["ProductDescription"]
            .str.contains(
                search_product,
                case=False,
                na=False,
            )
        )
        |
        (
            display_df["StockCode"]
            .astype(str)
            .str.contains(
                search_product,
                case=False,
                na=False,
            )
        )
    ]

# ==========================================================
# Quantity vs Revenue Analysis
# ==========================================================

left_scatter, right_scatter = st.columns(2)

with left_scatter:

    st.subheader("📊 Quantity vs Revenue")

    fig_quantity_revenue = px.scatter(
        filtered_df,
        x="TotalQuantity",
        y="TotalRevenue",
        size="TotalOrders",
        color="InventoryStatus",
        hover_name="ProductDescription",
        title="Quantity vs Revenue"
    )

    fig_quantity_revenue.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
        xaxis_title="Total Quantity",
        yaxis_title="Revenue (£)"
    )

    st.plotly_chart(
        fig_quantity_revenue,
        use_container_width=True,
        key="inventory_quantity_revenue_chart"
    )

with right_scatter:

    st.subheader("📈 Orders vs Revenue")

    fig_orders_revenue = px.scatter(
        filtered_df,
        x="TotalOrders",
        y="TotalRevenue",
        size="TotalQuantity",
        color="Recommendation",
        hover_name="ProductDescription",
        title="Orders vs Revenue"
    )

    fig_orders_revenue.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
        xaxis_title="Orders",
        yaxis_title="Revenue (£)"
    )

    st.plotly_chart(
        fig_orders_revenue,
        use_container_width=True,
        key="inventory_orders_revenue_chart"
    )

st.markdown("---")

# ==========================================================
# Inventory Summary Table
# ==========================================================

st.subheader("📋 Inventory Summary")

display_columns = [
    "StockCode",
    "ProductDescription",
    "TotalQuantity",
    "TotalRevenue",
    "TotalOrders",
    "InventoryStatus",
    "Recommendation",
]

st.dataframe(
    display_df[display_columns]
    .sort_values(
        "TotalRevenue",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")

# ==========================================================
# Download Inventory Report
# ==========================================================

inventory_csv = (
    display_df
    .to_csv(index=False)
    .encode("utf-8")
)

st.download_button(
    label="📥 Download Inventory Report",
    data=inventory_csv,
    file_name="inventory_summary.csv",
    mime="text/csv",
)

st.markdown("---")

# ==========================================================
# Inventory Business Insights
# ==========================================================

highest_revenue_product = (
    filtered_df
    .sort_values(
        "TotalRevenue",
        ascending=False
    )
    .iloc[0]
)

highest_quantity_product = (
    filtered_df
    .sort_values(
        "TotalQuantity",
        ascending=False
    )
    .iloc[0]
)

highest_orders_product = (
    filtered_df
    .sort_values(
        "TotalOrders",
        ascending=False
    )
    .iloc[0]
)

left_info, right_info = st.columns(2)

with left_info:

    st.success(
        f"""
### 💰 Revenue Insights

Highest Revenue Product

**{highest_revenue_product['ProductDescription']}**

Revenue

**£{highest_revenue_product['TotalRevenue']:,.2f}**

Inventory Status

**{highest_revenue_product['InventoryStatus']}**
"""
    )

with right_info:

    st.success(
        f"""
### 📦 Inventory Insights

Highest Quantity Product

**{highest_quantity_product['ProductDescription']}**

Most Ordered Product

**{highest_orders_product['ProductDescription']}**

Recommendation

**{highest_orders_product['Recommendation']}**
"""
    )

st.markdown("---")

# ==========================================================
# Executive Inventory Summary
# ==========================================================

st.subheader("📊 Executive Inventory Summary")

inventory_status_counts = (
    filtered_df["InventoryStatus"]
    .value_counts()
)

recommendation_counts = (
    filtered_df["Recommendation"]
    .value_counts()
)

summary_left, summary_right = st.columns(2)

with summary_left:

    st.info(
        f"""
### 📦 Inventory Overview

Products Analysed

**{total_products:,}**

Total Quantity

**{int(total_quantity):,}**

Total Orders

**{int(total_orders):,}**

Total Revenue

**£{total_revenue:,.2f}**
"""
    )

with summary_right:

    st.info(
        f"""
### 📈 Operational Summary

Inventory Categories

**{len(inventory_status_counts)}**

Recommendation Types

**{len(recommendation_counts)}**

Average Product Revenue

**£{average_revenue:,.2f}**
"""
    )

st.markdown("---")

# ==========================================================
# Inventory Optimization Recommendations
# ==========================================================

st.subheader("💡 Inventory Recommendations")

recommendations = []

status_text = (
    filtered_df["InventoryStatus"]
    .astype(str)
    .str.lower()
)

recommendation_text = (
    filtered_df["Recommendation"]
    .astype(str)
    .str.lower()
)

if status_text.str.contains("high").any():
    recommendations.append(
        "Monitor high-demand products closely and maintain adequate stock levels."
    )

if status_text.str.contains("low").any():
    recommendations.append(
        "Review slow-moving inventory and consider promotional campaigns."
    )

if recommendation_text.str.contains("restock").any():
    recommendations.append(
        "Prioritize restocking products identified by the notebook recommendations."
    )

if recommendation_text.str.contains("reduce").any():
    recommendations.append(
        "Reduce excess inventory where recommended to optimize storage costs."
    )

recommendations.append(
    "Follow notebook-generated inventory recommendations rather than manually changing inventory strategy inside the dashboard."
)

for i, recommendation in enumerate(recommendations, start=1):
    st.write(f"{i}. {recommendation}")

st.markdown("---")

# ==========================================================
# Inventory Health Status
# ==========================================================

st.subheader("🚦 Inventory Health")

high_ratio = (
    high_demand_products / total_products
    if total_products > 0 else 0
)

if high_ratio >= 0.60:
    st.success("Inventory Health: Strong Demand")

elif high_ratio >= 0.35:
    st.info("Inventory Health: Balanced")

elif high_ratio >= 0.15:
    st.warning("Inventory Health: Monitor Inventory")

else:
    st.error("Inventory Health: Needs Review")

st.markdown("---")

# ==========================================================
# Footer
# ==========================================================

st.caption(
    """
RetailPulse

Inventory Optimization Dashboard

Notebook Outputs : Read Only

Reports:
inventory_summary.csv
inventory_recommendations.csv

Version : 1.0
"""
)
