import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from utils.theme import (
    load_css, 
    page_header, 
    section_header, 
    dashboard_divider, 
    dashboard_footer,
    kpi_card
)
from utils.data_loader import load_retail_data
from utils.helpers import (
    format_currency, 
    format_number, 
    format_percentage, 
    format_compact_currency
)
from utils.metrics import (
    get_product_kpis, 
    get_total_revenue, 
    get_total_products, 
    get_total_quantity, 
    get_average_order_value
)
from utils.chart_utils import (
    create_bar_chart, 
    create_horizontal_bar_chart, 
    create_pie_chart, 
    create_scatter_chart, 
    create_histogram, 
    create_line_chart, 
    create_box_plot, 
    apply_chart_layout
)

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

page_header("📦 Product Performance", "RetailPulse • Product Revenue & Performance Analytics")
dashboard_divider()

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

if not product_summary.empty:
    highest_revenue_product = product_summary.iloc[0]["ProductDescription"]
    highest_quantity_product = (
        product_summary
        .sort_values("Quantity", ascending=False)
        .iloc[0]["ProductDescription"]
    )
else:
    highest_revenue_product = "N/A"
    highest_quantity_product = "N/A"

# ==========================================================
# KPI Cards
# ==========================================================

section_header("📊 Product Overview")

st.markdown('<div class="rp-kpi-grid">', unsafe_allow_html=True)
kpi1, kpi2, kpi3 = st.columns(3)

with kpi1:
    st.markdown(kpi_card("Products", format_number(total_products), icon="📦", color="#2563EB"), unsafe_allow_html=True)

with kpi2:
    st.markdown(kpi_card("Revenue", format_currency(total_revenue), icon="💰", color="#0EA5E9"), unsafe_allow_html=True)

with kpi3:
    st.markdown(kpi_card("Quantity Sold", format_number(int(total_quantity)), icon="📈", color="#22C55E"), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="rp-kpi-grid">', unsafe_allow_html=True)
kpi4, kpi5, kpi6 = st.columns(3)

with kpi4:
    st.markdown(kpi_card("Avg Product Revenue", format_currency(average_product_revenue), icon="📊", color="#F59E0B"), unsafe_allow_html=True)

with kpi5:
    st.markdown(kpi_card("Highest Revenue Product", highest_revenue_product, icon="⭐", color="#8B5CF6"), unsafe_allow_html=True)

with kpi6:
    st.markdown(kpi_card("Highest Quantity Product", highest_quantity_product, icon="🏆", color="#EC4899"), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Top Revenue & Quantity Charts
# ==========================================================

left_chart, right_chart = st.columns(2)

with left_chart:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("💰 Top 10 Products by Revenue")
    
    top_revenue = product_summary.head(10).sort_values("Revenue", ascending=True)
    
    fig_top_revenue = create_horizontal_bar_chart(
        data=top_revenue,
        x="Revenue",
        y="ProductDescription",
        title="",
        color="Revenue",
        text_auto=".2s"
    )
    
    fig_top_revenue = apply_chart_layout(fig_top_revenue, height=500)
    fig_top_revenue.update_layout(xaxis_title="Revenue (£)", yaxis_title="")
    
    st.plotly_chart(
        fig_top_revenue,
        width="stretch",
        key="top_revenue_products_chart",
    )
    st.markdown('</div>', unsafe_allow_html=True)

with right_chart:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("📦 Top 10 Products by Quantity")
    
    top_quantity = product_summary.sort_values("Quantity", ascending=False).head(10).sort_values("Quantity", ascending=True)
    
    fig_top_quantity = create_horizontal_bar_chart(
        data=top_quantity,
        x="Quantity",
        y="ProductDescription",
        title="",
        color="Quantity",
        text_auto=".2s"
    )
    
    fig_top_quantity = apply_chart_layout(fig_top_quantity, height=500)
    fig_top_quantity.update_layout(xaxis_title="Quantity", yaxis_title="")
    
    st.plotly_chart(
        fig_top_quantity,
        width="stretch",
        key="top_quantity_products_chart",
    )
    st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Revenue vs Quantity Analysis
# ==========================================================

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("📈 Revenue vs Quantity")

fig_scatter = create_scatter_chart(
    data=product_summary,
    x="Quantity",
    y="Revenue",
    title="",
    color="Revenue",
    size="Revenue",
    hover_name="ProductDescription"
)

fig_scatter = apply_chart_layout(fig_scatter, height=600)

st.plotly_chart(
    fig_scatter,
    width="stretch",
    key="revenue_quantity_scatter_chart",
)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Revenue Distribution
# ==========================================================

left_hist, right_hist = st.columns(2)

with left_hist:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("📊 Revenue Distribution")
    
    fig_histogram = create_histogram(
        data=product_summary,
        x="Revenue",
        title="",
        nbins=40
    )
    
    fig_histogram = apply_chart_layout(fig_histogram, height=450)
    
    st.plotly_chart(
        fig_histogram,
        width="stretch",
        key="revenue_distribution_chart",
    )
    st.markdown('</div>', unsafe_allow_html=True)

with right_hist:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("📉 Pareto Analysis (80/20 Rule)")
    
    pareto = product_summary.sort_values("Revenue", ascending=False).copy()
    pareto["CumulativeRevenue"] = pareto["Revenue"].cumsum()
    pareto["CumulativePercentage"] = pareto["CumulativeRevenue"] / pareto["Revenue"].sum() * 100
    
    fig_pareto = go.Figure()
    fig_pareto.add_trace(
        go.Bar(
            x=pareto["ProductDescription"],
            y=pareto["Revenue"],
            name="Revenue",
            marker_color="#2563EB"
        )
    )
    fig_pareto.add_trace(
        go.Scatter(
            x=pareto["ProductDescription"],
            y=pareto["CumulativePercentage"],
            mode="lines",
            name="Cumulative %",
            yaxis="y2",
            line=dict(color="#EF4444", width=3)
        )
    )
    
    fig_pareto = apply_chart_layout(fig_pareto, height=500)
    fig_pareto.update_layout(
        xaxis=dict(showticklabels=False),
        yaxis=dict(title="Revenue (£)"),
        yaxis2=dict(
            title="Cumulative %",
            overlaying="y",
            side="right",
            range=[0, 100],
        ),
        showlegend=False
    )
    
    st.plotly_chart(
        fig_pareto,
        width="stretch",
        key="pareto_analysis_chart",
    )
    st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Product Search
# ==========================================================

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("🔍 Product Search")

search_product = st.text_input(
    "Search Product",
    placeholder="Type product name...",
    key="product_search_input"
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

section_header("📋 Product Performance")

display_table = filtered_products.sort_values("Revenue", ascending=False)

st.dataframe(
    display_table,
    width="stretch",
    hide_index=True,
)

# ==========================================================
# Download Report
# ==========================================================

st.markdown('<div class="rp-download-btn">', unsafe_allow_html=True)
csv = display_table.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Product Report",
    data=csv,
    file_name="product_performance.csv",
    mime="text/csv",
    key="download_product_report"
)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Business Insights
# ==========================================================

highest_revenue = product_summary.sort_values("Revenue", ascending=False).iloc[0] if not product_summary.empty else None
highest_quantity = product_summary.sort_values("Quantity", ascending=False).iloc[0] if not product_summary.empty else None
average_price = product_summary["AveragePrice"].mean() if not product_summary.empty else 0
top10_revenue = product_summary.head(10)["Revenue"].sum() if not product_summary.empty else 0
overall_revenue = product_summary["Revenue"].sum() if not product_summary.empty else 0
top10_percentage = (top10_revenue / overall_revenue * 100) if overall_revenue > 0 else 0
active_products = len(product_summary)

left_info, right_info = st.columns(2)

with left_info:
    with st.expander("💰 Revenue Insights", expanded=True):
        st.write(f"**Highest Revenue Product:** {highest_revenue['ProductDescription'] if highest_revenue is not None else 'N/A'}")
        st.write(f"**Revenue:** {format_currency(highest_revenue['Revenue'] if highest_revenue is not None else 0)}")
        st.write(f"**Average Product Price:** {format_currency(average_price)}")

with right_info:
    with st.expander("📦 Product Insights", expanded=True):
        st.write(f"**Highest Quantity Product:** {highest_quantity['ProductDescription'] if highest_quantity is not None else 'N/A'}")
        st.write(f"**Units Sold:** {format_number(int(highest_quantity['Quantity']) if highest_quantity is not None else 0)}")
        st.write(f"**Active Products:** {format_number(active_products)}")
        st.write(f"**Top 10 Products contribute:** {format_percentage(top10_percentage)} of total revenue.")

dashboard_divider()

# ==========================================================
# Executive Summary
# ==========================================================

with st.expander("📊 Executive Summary", expanded=True):
    st.write(f"• **Products Analysed:** {format_number(active_products)}")
    st.write(f"• **Revenue Generated:** {format_currency(overall_revenue)}")
    st.write(f"• **Units Sold:** {format_number(int(total_quantity))}")
    st.write(f"• **Average Product Revenue:** {format_currency(average_product_revenue)}")
    st.write(f"• **Top Product:** {highest_revenue['ProductDescription'] if highest_revenue is not None else 'N/A'}")

dashboard_divider()

# ==========================================================
# Footer
# ==========================================================

dashboard_footer()