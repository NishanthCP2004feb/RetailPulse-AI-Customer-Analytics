import streamlit as st
from utils.metrics import get_basic_kpis
from utils.data_loader import load_retail_data

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Executive Dashboard",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Executive Dashboard")
st.caption("RetailPulse • AI-Powered Customer Analytics & Demand Forecasting")

st.markdown("---")

# --------------------------------------------------
# Load Dataset
# --------------------------------------------------
df = load_retail_data()

# --------------------------------------------------
# KPI Calculations
# --------------------------------------------------
kpis = get_basic_kpis(df)

from utils.chart_utils import (
    create_monthly_sales_chart,
    create_top_products_chart,
)
# --------------------------------------------------
# KPI Cards
# --------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"£{kpis['Total Revenue']:,.2f}")
col2.metric("Orders", f"{kpis['Orders']:,}")
col3.metric("Customers", f"{kpis['Customers']:,}")
col4.metric("Products", f"{kpis['Products']:,}")

st.markdown("---")

st.markdown("---")
st.subheader("Sales Overview")

left, right = st.columns(2)

with left:
    st.plotly_chart(
        create_monthly_sales_chart(df),
        use_container_width=True,
    )

with right:
    st.plotly_chart(
        create_top_products_chart(df),
        use_container_width=True,
    )
# --------------------------------------------------
# Dataset Overview
# --------------------------------------------------
st.subheader("Dataset Overview")

left, right = st.columns([2, 1])

with left:
    st.dataframe(df.head(), use_container_width=True)

with right:
    st.write("**Rows**", len(df))
    st.write("**Columns**", len(df.columns))
    st.write(
        "**Date Range**",
        f"{df['InvoiceDate'].min().date()} → {df['InvoiceDate'].max().date()}",
    )

st.success("Executive Dashboard loaded successfully.")