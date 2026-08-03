import streamlit as st
from utils.theme import load_css
# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="RetailPulse - AI Customer Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
st.sidebar.title("📂 Navigation")
st.sidebar.info(
    "Use the sidebar to navigate through the RetailPulse dashboard pages."
)

# --------------------------------------------------
# Main Page
# --------------------------------------------------
st.title("🛍️ RetailPulse")
st.subheader("AI-Powered Customer Analytics & Demand Forecasting")

st.markdown("---")

st.markdown("""
Welcome to the **RetailPulse** production dashboard.

This application is built on the outputs generated from the completed
RetailPulse notebook pipeline.

The dashboard **does not retrain models or modify datasets**.
It consumes the existing processed datasets, reports, and trained models
as read-only resources.

### Available Dashboard Modules

- 📊 Executive Dashboard
- 📈 Sales Analytics
- 📦 Product Performance
- 👥 Customer Analytics
- 🌍 Country Analytics
- 📉 Sales Forecasting
- ⚠️ Churn Analytics
- 📦 Inventory Optimization
- 🎯 Recommendation System
- 💡 Business Insights
- 📊 Interactive Analytics

Select a module from the **left sidebar** to begin.
""")

st.success("✅ Production Streamlit application initialized successfully.")