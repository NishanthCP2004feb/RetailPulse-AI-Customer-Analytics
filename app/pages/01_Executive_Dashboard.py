import streamlit as st

from utils.data_loader import load_retail_data
from utils.metrics import get_sales_kpis, get_customer_kpis, get_product_kpis, get_basic_kpis
from utils.helpers import format_currency, format_number, format_percentage, format_compact_currency
from utils.chart_utils import (
    create_monthly_sales_chart,
    create_top_products_chart,
    create_country_sales_chart,
    create_pie_chart,
    create_bar_chart,
    create_line_chart,
    apply_chart_layout
)
from utils.theme import (
    load_css,
    page_header,
    section_header,
    dashboard_divider,
    dashboard_footer,
    kpi_card,
    render_kpi_row,
    success_banner,
    info_banner,
    render_insight_card,
    apply_plotly_theme
)

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide",
)

load_css()

# =====================================================
# Header
# =====================================================

page_header(
    title="📊 Executive Dashboard",
    subtitle="RetailPulse • AI-Powered Customer Analytics & Demand Forecasting",
)

dashboard_divider()

# =====================================================
# Load Dataset
# =====================================================

df = load_retail_data()

# =====================================================
# KPI Calculations
# =====================================================

kpis = get_basic_kpis(df)

# =====================================================
# KPI Cards
# =====================================================

st.markdown('<div class="rp-card">', unsafe_allow_html=True)

render_kpi_row([
    {"title": "Total Revenue", "value": format_currency(kpis["Revenue"]), "icon": "💰", "color": "#2563EB"},
    {"title": "Orders", "value": format_number(kpis["Orders"]), "icon": "🧾", "color": "#0EA5E9"},
    {"title": "Customers", "value": format_number(kpis["Customers"]), "icon": "👥", "color": "#22C55E"},
    {"title": "Products", "value": format_number(kpis["Products"]), "icon": "📦", "color": "#F59E0B"}
])

st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# =====================================================
# Sales Overview
# =====================================================

section_header("Sales Overview")

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
left, right = st.columns(2)

with left:
    monthly_sales_chart = create_monthly_sales_chart(df)
    st.plotly_chart(
        monthly_sales_chart,
        width="stretch",
        key="exec_monthly_sales"
    )

with right:
    top_products_chart = create_top_products_chart(df)
    st.plotly_chart(
        top_products_chart,
        width="stretch",
        key="exec_top_products"
    )
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# =====================================================
# Dataset Overview
# =====================================================

section_header("Dataset Overview")

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
left, right = st.columns([2, 1])

with left:
    st.dataframe(
        df.head(10),
        width="stretch",
        hide_index=True,
    )

with right:
    render_kpi_row([
        {"title": "Rows", "value": format_number(len(df)), "icon": "📑", "color": "#2563EB"},
        {"title": "Columns", "value": format_number(len(df.columns)), "icon": "📊", "color": "#0EA5E9"}
    ])
    
    render_kpi_row([
        {"title": "Countries", "value": format_number(df["Country"].nunique()), "icon": "🌍", "color": "#8B5CF6"},
        {"title": "Date Range", "value": f"{df['InvoiceDate'].min().strftime('%d %b %Y')} → {df['InvoiceDate'].max().strftime('%d %b %Y')}", "icon": "📅", "color": "#14B8A6"}
    ])
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# =====================================================
# Footer
# =====================================================

success_banner("Executive Dashboard loaded successfully.")

dashboard_footer()
