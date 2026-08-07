import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# Utilities
# ==========================================================
from utils.theme import (
    load_css, 
    page_header, 
    section_header, 
    dashboard_divider, 
    dashboard_footer, 
    render_kpi_row, 
    render_insight_card
)
from utils.data_loader import load_retail_data
from utils.helpers import (
    format_currency, 
    format_number, 
    format_percentage, 
    format_compact_currency
)
from utils.metrics import (
    get_total_revenue, 
    get_total_orders, 
    get_total_customers, 
    get_total_products, 
    get_total_quantity, 
    get_average_order_value
)
from utils.chart_utils import (
    create_monthly_sales_chart, 
    create_top_products_chart, 
    create_country_sales_chart, 
    create_bar_chart, 
    create_line_chart, 
    create_scatter_chart, 
    create_histogram, 
    create_pie_chart, 
    apply_chart_layout
)

@st.cache_data(show_spinner=False)
def _get_filter_options(_df):
    """Return cached unique sorted filter values."""
    countries = sorted(_df["Country"].dropna().unique())
    years = sorted(_df["InvoiceYear"].dropna().unique())
    months = sorted(_df["MonthName"].dropna().unique())
    return countries, years, months

@st.cache_data(show_spinner=False)
def _convert_df_to_csv(_df):
    """Cache CSV conversion to avoid recomputing on every rerun."""
    return _df.to_csv(index=False).encode('utf-8')

# ==========================================================
# Page Config
# ==========================================================
st.set_page_config(
    page_title="Sales Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()

# ==========================================================
# Header
# ==========================================================
page_header(
    '📈 Sales Analytics', 
    'RetailPulse • Sales Performance & Revenue Analysis'
)

# ==========================================================
# Load Dataset
# ==========================================================
df = load_retail_data()

if df.empty:
    st.error("Retail dataset not found.")
    st.stop()

# ==========================================================
# Sidebar Filters
# ==========================================================
st.sidebar.header("🎛 Sales Filters")

countries, years, months = _get_filter_options(df)

# Handle missing or empty lists for filters
selected_country = st.sidebar.multiselect(
    "Country",
    countries,
    default=countries,
)

selected_year = st.sidebar.multiselect(
    "Invoice Year",
    years,
    default=years,
)

selected_month = st.sidebar.multiselect(
    "Month",
    months,
    default=months,
)

filtered_df = df[
    (df["Country"].isin(selected_country)) &
    (df["InvoiceYear"].isin(selected_year)) &
    (df["MonthName"].isin(selected_month))
]

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# ==========================================================
# KPI Row
# ==========================================================


revenue = get_total_revenue(filtered_df)
orders = get_total_orders(filtered_df)
aov = get_average_order_value(filtered_df)
quantity = get_total_quantity(filtered_df)
products = get_total_products(filtered_df)
customers = get_total_customers(filtered_df)

kpi_data = [
    {"title": "Total Revenue", "value": format_currency(revenue), "icon": "💰", "color": "#2563EB"},
    {"title": "Total Orders", "value": format_number(orders), "icon": "🛒", "color": "#0EA5E9"},
    {"title": "Average Order Value", "value": format_currency(aov), "icon": "💳", "color": "#22C55E"},
    {"title": "Total Quantity", "value": format_number(quantity), "icon": "📦", "color": "#F59E0B"},
    {"title": "Unique Products", "value": format_number(products), "icon": "🏷️", "color": "#EF4444"},
    {"title": "Unique Customers", "value": format_number(customers), "icon": "👥", "color": "#06B6D4"}
]

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
render_kpi_row(kpi_data)
st.markdown('</div>', unsafe_allow_html=True)
dashboard_divider()

# ==========================================================
# Charts - Row 1
# ==========================================================
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("Monthly Revenue Trend")
    monthly_sales_fig = create_monthly_sales_chart(filtered_df)
    st.plotly_chart(monthly_sales_fig, use_container_width=True, key="monthly_revenue")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("Revenue by Country (Top 10)")
    country_sales_fig = create_country_sales_chart(filtered_df, top_n=10)
    st.plotly_chart(country_sales_fig, use_container_width=True, key="country_sales")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Charts - Row 2
# ==========================================================
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("Top 10 Products by Revenue")
    top_products_fig = create_top_products_chart(filtered_df, top_n=10)
    st.plotly_chart(top_products_fig, use_container_width=True, key="top_products")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("Revenue by Day of Week")
    dow_revenue = filtered_df.groupby("DayName", as_index=False)["TotalAmount"].sum()
    dow_revenue = dow_revenue.sort_values("TotalAmount", ascending=False)
    dow_fig = create_bar_chart(dow_revenue, x="DayName", y="TotalAmount", title="Revenue by Day of Week")
    st.plotly_chart(dow_fig, use_container_width=True, key="dow_revenue")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Charts - Row 3
# ==========================================================
col5, col6 = st.columns(2)

with col5:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("Revenue Distribution")
    dist_fig = create_histogram(filtered_df, x="TotalAmount", title="Revenue Distribution", nbins=50)
    st.plotly_chart(dist_fig, use_container_width=True, key="revenue_dist")
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("Monthly Orders Trend")
    monthly_orders = filtered_df.groupby("InvoiceMonthYear", as_index=False)["InvoiceID"].nunique()
    # To maintain temporal order, sort by the actual date proxy if possible, or just plot as is assuming it's pre-sorted
    monthly_orders_fig = create_line_chart(monthly_orders, x="InvoiceMonthYear", y="InvoiceID", title="Monthly Orders Trend", markers=True)
    st.plotly_chart(monthly_orders_fig, use_container_width=True, key="monthly_orders")
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Charts - Row 4
# ==========================================================
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("Revenue vs Quantity Scatter")
scatter_sample = filtered_df.sample(n=min(5000, len(filtered_df)), random_state=42) if len(filtered_df) > 5000 else filtered_df
scatter_fig = create_scatter_chart(scatter_sample, x="Quantity", y="TotalAmount", title="Revenue vs Quantity", color="Country", hover_name="ProductDescription")
st.plotly_chart(scatter_fig, use_container_width=True, key="rev_vs_qty")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Sales Data Table & Download
# ==========================================================
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("Sales Data")
st.dataframe(filtered_df.head(100), use_container_width=True)

st.markdown('<div class="rp-download-btn">', unsafe_allow_html=True)
csv_data = _convert_df_to_csv(filtered_df)
st.download_button(
    label="⬇️ Download Filtered Sales Data (CSV)",
    data=csv_data,
    file_name="retailpulse_sales_filtered.csv",
    mime="text/csv",
    key="download_sales_data"
)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Business Insights
# ==========================================================
with st.expander("💡 Business Insights & Recommendations"):
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    
    insight_1 = {
        "title": "Revenue Concentration",
        "description": "Analyze the top products chart to see if your revenue is overly dependent on a few key items. High concentration increases risk.",
        "icon": "⚠️",
        "color": "#F59E0B"
    }
    
    insight_2 = {
        "title": "Seasonal Trends",
        "description": "Observe the monthly revenue trend to identify peak seasons. Use these patterns to optimize inventory and marketing campaigns.",
        "icon": "📅",
        "color": "#2563EB"
    }
    
    insight_3 = {
        "title": "Geographic Performance",
        "description": "Evaluate the country revenue chart. Identify high-performing regions for expansion and underperforming regions for targeted promotions.",
        "icon": "🌍",
        "color": "#0EA5E9"
    }
    
    render_insight_card(insight_1)
    render_insight_card(insight_2)
    render_insight_card(insight_3)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ==========================================================
# Footer
# ==========================================================
dashboard_footer()
