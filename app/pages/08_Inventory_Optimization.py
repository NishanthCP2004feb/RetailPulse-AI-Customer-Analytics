# ==========================================================
# Imports
# ==========================================================

import streamlit as st
import pandas as pd

from utils.theme import (
    load_css, 
    page_header, 
    section_header, 
    dashboard_divider, 
    dashboard_footer, 
    render_kpi_row, 
    render_insight_card, 
    success_banner, 
    warning_banner
)
from utils.data_loader import load_inventory_reports
from utils.helpers import format_currency, format_number
from utils.chart_utils import (
    create_bar_chart, 
    create_horizontal_bar_chart, 
    create_pie_chart, 
    create_scatter_chart
)

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

page_header('📦 Inventory Optimization', 'RetailPulse • Stock Management & Optimization Analytics')

dashboard_divider()

# ==========================================================
# Load Reports
# ==========================================================

@st.cache_data
def get_data():
    return load_inventory_reports()

summary_df, recommendation_df = get_data()

if summary_df.empty:
    st.error("Inventory report not found.")
    st.stop()

# ==========================================================
# Sidebar Filters
# ==========================================================

st.sidebar.header("📦 Inventory Filters")

status_options = sorted(
    summary_df["InventoryStatus"].dropna().unique()
)

selected_status = st.sidebar.multiselect(
    "Inventory Status",
    status_options,
    default=status_options,
    key="inventory_status_filter"
)

recommendation_options = sorted(
    summary_df["Recommendation"].dropna().unique()
)

selected_recommendation = st.sidebar.multiselect(
    "Recommendation",
    recommendation_options,
    default=recommendation_options,
    key="inventory_recommendation_filter"
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
    warning_banner("No products found.")
    st.stop()

# ==========================================================
# KPI Calculations
# ==========================================================

total_products = len(filtered_df)
total_quantity = filtered_df["TotalQuantity"].sum()
total_revenue = filtered_df["TotalRevenue"].sum()
total_orders = filtered_df["TotalOrders"].sum()
average_revenue = filtered_df["TotalRevenue"].mean() if total_products > 0 else 0
high_demand_products = (filtered_df["InventoryStatus"] == "High Demand").sum()

# ==========================================================
# KPI Cards
# ==========================================================

section_header("📊 Inventory Overview")

# Top row
kpi_row_1 = [
    {"title": "Products", "value": format_number(total_products), "icon": "📦"},
    {"title": "Quantity", "value": format_number(total_quantity), "icon": "🔢"},
    {"title": "Revenue", "value": format_currency(total_revenue), "icon": "💰"}
]
render_kpi_row(kpi_row_1)

# Bottom row
kpi_row_2 = [
    {"title": "Orders", "value": format_number(total_orders), "icon": "🛍️"},
    {"title": "Average Revenue", "value": format_currency(average_revenue), "icon": "📈"},
    {"title": "High Demand", "value": format_number(high_demand_products), "icon": "🔥"}
]
render_kpi_row(kpi_row_2)

dashboard_divider()

# ==========================================================
# Inventory Status Distribution
# ==========================================================

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
left_chart, right_chart = st.columns(2)

with left_chart:
    section_header("📊 Inventory Status Distribution")
    status_distribution = filtered_df["InventoryStatus"].value_counts().reset_index()
    status_distribution.columns = ["InventoryStatus", "Products"]
    
    fig_inventory_status = create_pie_chart(
        status_distribution,
        names="InventoryStatus",
        values="Products",
        title="Inventory Status",
        hole=0.45
    )
    st.plotly_chart(fig_inventory_status, use_container_width=True, key="inventory_status_chart")

# ==========================================================
# Recommendation Distribution
# ==========================================================

with right_chart:
    section_header("💡 Recommendation Distribution")
    recommendation_distribution = filtered_df["Recommendation"].value_counts().reset_index()
    recommendation_distribution.columns = ["Recommendation", "Products"]
    
    fig_recommendation = create_bar_chart(
        recommendation_distribution,
        x="Recommendation",
        y="Products",
        color="Products",
        title="Inventory Recommendations",
        text_auto=True
    )
    st.plotly_chart(fig_recommendation, use_container_width=True, key="recommendation_distribution_chart")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Top Products
# ==========================================================

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
left_products, right_products = st.columns(2)

with left_products:
    section_header("📦 Top Products by Quantity")
    top_quantity = filtered_df.sort_values("TotalQuantity", ascending=False).head(10)
    
    fig_quantity = create_horizontal_bar_chart(
        top_quantity,
        x="TotalQuantity",
        y="ProductDescription",
        color="TotalQuantity",
        title="Highest Quantity Products",
        text_auto=True
    )
    st.plotly_chart(fig_quantity, use_container_width=True, key="inventory_quantity_chart")

with right_products:
    section_header("💰 Top Products by Revenue")
    top_revenue = filtered_df.sort_values("TotalRevenue", ascending=False).head(10)
    
    fig_revenue = create_horizontal_bar_chart(
        top_revenue,
        x="TotalRevenue",
        y="ProductDescription",
        color="TotalRevenue",
        title="Highest Revenue Products",
        text_auto=".2s"
    )
    st.plotly_chart(fig_revenue, use_container_width=True, key="inventory_revenue_chart")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Orders by Product
# ==========================================================

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("📈 Top Products by Orders")
top_orders = filtered_df.sort_values("TotalOrders", ascending=False).head(15)

fig_orders = create_bar_chart(
    top_orders,
    x="ProductDescription",
    y="TotalOrders",
    color="TotalOrders",
    title="Top Ordered Products",
    text_auto=True
)
st.plotly_chart(fig_orders, use_container_width=True, key="inventory_orders_chart")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Product Search
# ==========================================================

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("🔍 Product Search")

search_product = st.text_input(
    "Search Product",
    placeholder="Enter product name or stock code...",
    key="product_search_input"
)

display_df = filtered_df.copy()

if search_product:
    display_df = display_df[
        (display_df["ProductDescription"].str.contains(search_product, case=False, na=False)) |
        (display_df["StockCode"].astype(str).str.contains(search_product, case=False, na=False))
    ]

# ==========================================================
# Quantity vs Revenue Analysis
# ==========================================================

left_scatter, right_scatter = st.columns(2)

with left_scatter:
    section_header("📊 Quantity vs Revenue")
    fig_quantity_revenue = create_scatter_chart(
        filtered_df,
        x="TotalQuantity",
        y="TotalRevenue",
        color="InventoryStatus",
        size="TotalOrders",
        hover_name="ProductDescription",
        title="Quantity vs Revenue"
    )
    st.plotly_chart(fig_quantity_revenue, use_container_width=True, key="inventory_quantity_revenue_chart")

with right_scatter:
    section_header("📈 Orders vs Revenue")
    fig_orders_revenue = create_scatter_chart(
        filtered_df,
        x="TotalOrders",
        y="TotalRevenue",
        color="Recommendation",
        size="TotalQuantity",
        hover_name="ProductDescription",
        title="Orders vs Revenue"
    )
    st.plotly_chart(fig_orders_revenue, use_container_width=True, key="inventory_orders_revenue_chart")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Inventory Summary Table
# ==========================================================

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("📋 Inventory Summary")

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
    display_df[display_columns].sort_values("TotalRevenue", ascending=False),
    use_container_width=True,
    hide_index=True,
)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Download Inventory Report
# ==========================================================

st.markdown('<div class="rp-download-btn">', unsafe_allow_html=True)
inventory_csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Inventory Report",
    data=inventory_csv,
    file_name="inventory_summary.csv",
    mime="text/csv",
    key="download_inventory_summary"
)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Inventory Business Insights
# ==========================================================

highest_revenue_product = filtered_df.sort_values("TotalRevenue", ascending=False).iloc[0] if not filtered_df.empty else None
highest_quantity_product = filtered_df.sort_values("TotalQuantity", ascending=False).iloc[0] if not filtered_df.empty else None
highest_orders_product = filtered_df.sort_values("TotalOrders", ascending=False).iloc[0] if not filtered_df.empty else None

if highest_revenue_product is not None:
    left_info, right_info = st.columns(2)
    
    with left_info:
        render_insight_card(
            "💰 Revenue Insights",
            f"**Highest Revenue Product**: {highest_revenue_product['ProductDescription']}\n\n"
            f"**Revenue**: {format_currency(highest_revenue_product['TotalRevenue'])}\n\n"
            f"**Inventory Status**: {highest_revenue_product['InventoryStatus']}"
        )
    
    with right_info:
        render_insight_card(
            "📦 Inventory Insights",
            f"**Highest Quantity Product**: {highest_quantity_product['ProductDescription']}\n\n"
            f"**Most Ordered Product**: {highest_orders_product['ProductDescription']}\n\n"
            f"**Recommendation**: {highest_orders_product['Recommendation']}"
        )

dashboard_divider()

# ==========================================================
# Executive Inventory Summary
# ==========================================================

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("📊 Executive Inventory Summary")

inventory_status_counts = filtered_df["InventoryStatus"].value_counts()
recommendation_counts = filtered_df["Recommendation"].value_counts()

summary_left, summary_right = st.columns(2)

with summary_left:
    render_insight_card(
        "📦 Inventory Overview",
        f"**Products Analysed**: {format_number(total_products)}\n\n"
        f"**Total Quantity**: {format_number(total_quantity)}\n\n"
        f"**Total Orders**: {format_number(total_orders)}\n\n"
        f"**Total Revenue**: {format_currency(total_revenue)}"
    )

with summary_right:
    render_insight_card(
        "📈 Operational Summary",
        f"**Inventory Categories**: {len(inventory_status_counts)}\n\n"
        f"**Recommendation Types**: {len(recommendation_counts)}\n\n"
        f"**Average Product Revenue**: {format_currency(average_revenue)}"
    )
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Inventory Optimization Recommendations
# ==========================================================

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("💡 Inventory Recommendations")

with st.expander("View Inventory Recommendations", expanded=True):
    recommendations = []
    status_text = filtered_df["InventoryStatus"].astype(str).str.lower()
    recommendation_text = filtered_df["Recommendation"].astype(str).str.lower()
    
    if status_text.str.contains("high").any():
        recommendations.append("Monitor high-demand products closely and maintain adequate stock levels.")
    if status_text.str.contains("low").any():
        recommendations.append("Review slow-moving inventory and consider promotional campaigns.")
    if recommendation_text.str.contains("restock").any():
        recommendations.append("Prioritize restocking products identified by the notebook recommendations.")
    if recommendation_text.str.contains("reduce").any():
        recommendations.append("Reduce excess inventory where recommended to optimize storage costs.")
    
    recommendations.append("Follow notebook-generated inventory recommendations rather than manually changing inventory strategy inside the dashboard.")
    
    for i, recommendation in enumerate(recommendations, start=1):
        st.write(f"{i}. {recommendation}")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Inventory Health Status
# ==========================================================

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("🚦 Inventory Health")

high_ratio = high_demand_products / total_products if total_products > 0 else 0

if high_ratio >= 0.60:
    success_banner("Inventory Health: Strong Demand")
elif high_ratio >= 0.35:
    st.info("Inventory Health: Balanced")
elif high_ratio >= 0.15:
    warning_banner("Inventory Health: Monitor Inventory")
else:
    st.error("Inventory Health: Needs Review")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Footer
# ==========================================================

dashboard_footer()
