import streamlit as st
import pandas as pd

from utils.theme import (
    load_css, 
    page_header, 
    section_header, 
    dashboard_divider, 
    dashboard_footer,
    render_kpi_row,
    render_insight_card
)
from utils.data_loader import load_retail_data, load_customer_rfm
from utils.helpers import (
    format_currency, 
    format_number, 
    format_percentage, 
    format_compact_currency
)
from utils.metrics import (
    get_customer_kpis, 
    get_total_customers, 
    get_total_revenue, 
    get_revenue_per_customer
)
from utils.chart_utils import (
    create_bar_chart, 
    create_horizontal_bar_chart, 
    create_pie_chart, 
    create_scatter_chart, 
    create_histogram, 
    create_line_chart, 
    create_box_plot, 
    create_heatmap, 
    apply_chart_layout
)

load_css()

page_header('👥 Customer Analytics', 'RetailPulse • Customer Behavior & Segmentation Analysis')
dashboard_divider()

df = load_retail_data()

if df.empty:
    st.error("Dataset is empty.")
    st.stop()

st.sidebar.header("🔍 Customer Filters")

countries = sorted(df["Country"].dropna().unique())
years = sorted(df["InvoiceYear"].dropna().unique())
months = sorted(df["MonthName"].dropna().unique())

selected_countries = st.sidebar.multiselect("Country", countries, default=countries)
selected_years = st.sidebar.multiselect("Invoice Year", years, default=years)
selected_months = st.sidebar.multiselect("Month", months, default=months)

filtered_df = df[
    (df["Country"].isin(selected_countries)) &
    (df["InvoiceYear"].isin(selected_years)) &
    (df["MonthName"].isin(selected_months))
]

if filtered_df.empty:
    st.warning("No records available for selected filters.")
    st.stop()

customer_summary = (
    filtered_df
    .groupby("CustomerID", as_index=False)
    .agg(
        Revenue=("TotalAmount", "sum"),
        Orders=("InvoiceID", "nunique"),
        Quantity=("Quantity", "sum"),
        BasketValue=("BasketValue", "mean"),
        Country=("Country", "first"),
    )
)

total_customers = len(customer_summary)
total_revenue = customer_summary["Revenue"].sum()
average_customer_revenue = total_revenue / total_customers if total_customers > 0 else 0
average_orders = customer_summary["Orders"].mean() if not customer_summary.empty else 0
average_basket = customer_summary["BasketValue"].mean() if not customer_summary.empty else 0
highest_customer = customer_summary.sort_values("Revenue", ascending=False).iloc[0]["CustomerID"] if not customer_summary.empty else "N/A"

section_header("📊 Customer Overview")

kpis_row1 = [
    {"title": "Customers", "value": format_number(total_customers), "icon": "👥", "color": "primary"},
    {"title": "Revenue", "value": format_currency(total_revenue), "icon": "💰", "color": "success"},
    {"title": "Average Revenue", "value": format_currency(average_customer_revenue), "icon": "📈", "color": "info"},
]
render_kpi_row(kpis_row1)

kpis_row2 = [
    {"title": "Avg Orders", "value": f"{average_orders:.2f}", "icon": "📦", "color": "warning"},
    {"title": "Average Basket", "value": format_currency(average_basket), "icon": "🛒", "color": "primary"},
    {"title": "Top Customer", "value": str(highest_customer), "icon": "🏆", "color": "success"},
]
render_kpi_row(kpis_row2)

dashboard_divider()

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
left_chart, right_chart = st.columns(2)

with left_chart:
    section_header("🏆 Top 10 Customers by Revenue")
    top_customers = customer_summary.sort_values("Revenue", ascending=False).head(10)
    top_customers["CustomerID"] = top_customers["CustomerID"].astype(str)
    fig_top_customers = create_horizontal_bar_chart(
        top_customers,
        x="Revenue",
        y="CustomerID",
        title="Top Customers by Revenue",
        color="Revenue"
    )
    st.plotly_chart(fig_top_customers, use_container_width=True, key="top_customers_revenue")

with right_chart:
    section_header("🛒 Top 10 Customers by Orders")
    top_orders = customer_summary.sort_values("Orders", ascending=False).head(10)
    top_orders["CustomerID"] = top_orders["CustomerID"].astype(str)
    fig_top_orders = create_horizontal_bar_chart(
        top_orders,
        x="Orders",
        y="CustomerID",
        title="Top Customers by Orders",
        color="Orders"
    )
    st.plotly_chart(fig_top_orders, use_container_width=True, key="top_customer_orders")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
left_hist, right_hist = st.columns(2)

with left_hist:
    section_header("💰 Customer Revenue Distribution")
    fig_revenue_distribution = create_histogram(
        customer_summary,
        x="Revenue",
        nbins=40,
        title="Revenue Distribution"
    )
    st.plotly_chart(fig_revenue_distribution, use_container_width=True, key="customer_revenue_distribution")

with right_hist:
    section_header("📦 Order Frequency")
    fig_order_frequency = create_histogram(
        customer_summary,
        x="Orders",
        nbins=30,
        title="Customer Order Frequency"
    )
    st.plotly_chart(fig_order_frequency, use_container_width=True, key="customer_order_frequency")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
left_country, right_country = st.columns(2)

with left_country:
    section_header("🌍 Revenue by Country")
    country_summary = (
        customer_summary
        .groupby("Country", as_index=False)
        .agg(Revenue=("Revenue", "sum"))
        .sort_values("Revenue", ascending=False)
        .head(10)
    )
    fig_country = create_horizontal_bar_chart(
        country_summary,
        x="Revenue",
        y="Country",
        title="Top Countries by Customer Revenue",
        color="Revenue"
    )
    st.plotly_chart(fig_country, use_container_width=True, key="country_customer_revenue")

with right_country:
    section_header("📅 Monthly Active Customers")
    monthly_customers = (
        filtered_df
        .groupby("InvoiceMonthYear")["CustomerID"]
        .nunique()
        .reset_index(name="Customers")
    )
    monthly_customers["InvoiceMonthYear"] = monthly_customers["InvoiceMonthYear"].astype(str)
    fig_monthly_customers = create_line_chart(
        monthly_customers,
        x="InvoiceMonthYear",
        y="Customers",
        title="Monthly Active Customers",
        markers=True
    )
    st.plotly_chart(fig_monthly_customers, use_container_width=True, key="monthly_active_customers")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("🔍 Customer Search")

search_customer = st.text_input("Search Customer ID", placeholder="Enter Customer ID...")
display_table = customer_summary.copy()

if search_customer:
    display_table = display_table[
        display_table["CustomerID"].astype(str).str.contains(search_customer, case=False, na=False)
    ]

section_header("📋 Customer Summary")
display_table = display_table.sort_values("Revenue", ascending=False)
st.dataframe(display_table, use_container_width=True, hide_index=True)

st.markdown('<div class="rp-download-btn">', unsafe_allow_html=True)
csv = display_table.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Customer Report",
    data=csv,
    file_name="customer_analytics.csv",
    mime="text/csv",
    key="download_customer_report"
)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

highest_revenue_customer = customer_summary.sort_values("Revenue", ascending=False).iloc[0] if not customer_summary.empty else None
highest_orders_customer = customer_summary.sort_values("Orders", ascending=False).iloc[0] if not customer_summary.empty else None
active_countries = customer_summary["Country"].nunique()

with st.expander("💡 Business Insights", expanded=True):
    left_info, right_info = st.columns(2)
    
    with left_info:
        if highest_revenue_customer is not None:
            render_insight_card(
                "💰 Revenue Insights",
                f"""
                Highest Revenue Customer: **{highest_revenue_customer['CustomerID']}**  
                Revenue: **{format_currency(highest_revenue_customer['Revenue'])}**  
                Average Customer Revenue: **{format_currency(average_customer_revenue)}**
                """
            )
            
    with right_info:
        if highest_orders_customer is not None:
            render_insight_card(
                "👥 Customer Insights",
                f"""
                Highest Order Customer: **{highest_orders_customer['CustomerID']}**  
                Orders: **{format_number(highest_orders_customer['Orders'])}**  
                Active Countries: **{format_number(active_countries)}**  
                Average Orders: **{average_orders:.2f}**
                """
            )

    render_insight_card(
        "📊 Executive Summary",
        f"""
        • Customers Analysed: **{format_number(total_customers)}**  
        • Revenue Generated: **{format_currency(total_revenue)}**  
        • Average Basket Value: **{format_currency(average_basket)}**  
        • Top Customer: **{highest_revenue_customer['CustomerID'] if highest_revenue_customer is not None else 'N/A'}**
        """
    )

dashboard_footer()