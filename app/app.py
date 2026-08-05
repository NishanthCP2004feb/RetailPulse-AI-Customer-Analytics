import streamlit as st

from utils.theme import (
    load_css,
    page_header,
    section_header,
    dashboard_divider,
    dashboard_footer,
    render_kpi_row,
    info_banner,
    success_banner,
    render_insight_card,
    PRIMARY,
    SECONDARY,
    SUCCESS,
    WARNING,
    INFO,
)

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="RetailPulse - AI Customer Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.markdown(
    '<h3 class="rp-section-header">📂 Navigation</h3>',
    unsafe_allow_html=True,
)
st.sidebar.info(
    "Use the sidebar to navigate through the RetailPulse dashboard pages."
)

# --------------------------------------------------
# Page Header
# --------------------------------------------------
page_header(
    title="🛍️ RetailPulse",
    subtitle="AI-Powered Customer Analytics & Demand Forecasting",
)

dashboard_divider()

# --------------------------------------------------
# Welcome Section
# --------------------------------------------------
st.markdown('<div class="rp-card">', unsafe_allow_html=True)

section_header("Welcome")

st.markdown(
    """
Welcome to the **RetailPulse** production dashboard.

This application is built on the outputs generated from the completed
RetailPulse notebook pipeline. The dashboard **does not retrain models
or modify datasets**. It consumes the existing processed datasets,
reports, and trained models as read-only resources.
"""
)

st.markdown("</div>", unsafe_allow_html=True)

dashboard_divider()

# --------------------------------------------------
# Platform Highlights
# --------------------------------------------------
section_header("Platform Highlights")

render_kpi_row(
    [
        {
            "title": "Dashboard Modules",
            "value": "11",
            "icon": "📊",
            "color": PRIMARY,
        },
        {
            "title": "Analytics Engine",
            "value": "AI-Powered",
            "icon": "🤖",
            "color": SECONDARY,
        },
        {
            "title": "Data Pipeline",
            "value": "Read-Only",
            "icon": "🔒",
            "color": SUCCESS,
        },
        {
            "title": "Tech Stack",
            "value": "Python",
            "icon": "⚙️",
            "color": WARNING,
        },
    ]
)

dashboard_divider()

# --------------------------------------------------
# Dashboard Modules
# --------------------------------------------------
section_header("Available Dashboard Modules")

st.markdown('<div class="rp-card">', unsafe_allow_html=True)

left_col, right_col = st.columns(2)

with left_col:
    render_insight_card(
        "📊 Executive Dashboard",
        [
            "High-level KPIs and business overview",
            "Revenue, orders, and customer metrics",
            "Monthly sales trends and top products",
        ],
        card_type="info",
    )
    render_insight_card(
        "📈 Sales Analytics",
        [
            "Detailed sales performance analysis",
            "Country-wise and product-wise breakdowns",
            "Revenue trends and distribution insights",
        ],
        card_type="success",
    )
    render_insight_card(
        "📦 Product Performance",
        [
            "Product-level revenue and quantity analysis",
            "Top and bottom performing products",
            "Executive summary with key product metrics",
        ],
        card_type="info",
    )
    render_insight_card(
        "👥 Customer Analytics",
        [
            "Customer segmentation and behavior patterns",
            "RFM analysis and customer value scores",
            "Segment-wise revenue contribution",
        ],
        card_type="success",
    )
    render_insight_card(
        "🌍 Country Analytics",
        [
            "Geographic performance analysis",
            "Country-wise revenue, orders, and customers",
            "Top contributing regions identification",
        ],
        card_type="info",
    )
    render_insight_card(
        "📉 Forecasting",
        [
            "Sales forecasting with ML models",
            "Forecast accuracy and error analysis",
            "Future demand predictions",
        ],
        card_type="success",
    )

with right_col:
    render_insight_card(
        "⚠️ Churn Analytics",
        [
            "Customer churn prediction and analysis",
            "Risk scoring and retention recommendations",
            "Revenue at risk estimation",
        ],
        card_type="warning",
    )
    render_insight_card(
        "📦 Inventory Optimization",
        [
            "Inventory status and demand tracking",
            "Restock and reduction recommendations",
            "Inventory health monitoring",
        ],
        card_type="info",
    )
    render_insight_card(
        "🎯 Recommendation System",
        [
            "AI-powered product recommendations",
            "Cross-selling and upselling insights",
            "Customer segment-based suggestions",
        ],
        card_type="success",
    )
    render_insight_card(
        "💡 Business Insights",
        [
            "Comprehensive business intelligence",
            "Actionable insights and recommendations",
            "Strategic decision support data",
        ],
        card_type="info",
    )
    render_insight_card(
        "📊 Interactive Analytics",
        [
            "Custom data exploration tools",
            "Dynamic filtering and visualization",
            "Ad-hoc analysis capabilities",
        ],
        card_type="success",
    )

st.markdown("</div>", unsafe_allow_html=True)

dashboard_divider()

# --------------------------------------------------
# Technology Stack
# --------------------------------------------------
section_header("Technology Stack")

render_kpi_row(
    [
        {
            "title": "Frontend",
            "value": "Streamlit",
            "icon": "🖥️",
            "color": PRIMARY,
        },
        {
            "title": "Visualization",
            "value": "Plotly",
            "icon": "📊",
            "color": SECONDARY,
        },
        {
            "title": "ML Framework",
            "value": "Scikit-learn",
            "icon": "🧠",
            "color": INFO,
        },
        {
            "title": "Language",
            "value": "Python",
            "icon": "🐍",
            "color": SUCCESS,
        },
    ]
)

dashboard_divider()

# --------------------------------------------------
# Status
# --------------------------------------------------
success_banner("Production dashboard initialized successfully.")
info_banner(
    "Select a module from the sidebar to begin exploring your data."
)

# --------------------------------------------------
# Footer
# --------------------------------------------------
dashboard_footer()