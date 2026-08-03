import streamlit as st
import plotly.express as px
import pandas as pd

from utils.chart_utils import create_monthly_sales_chart
from utils.theme import load_css
from utils.data_loader import load_retail_data
from utils.metrics import get_basic_kpis

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Sales Analytics",
    page_icon="📈",
    layout="wide",
)

load_css()

st.title("📈 Sales Analytics")
st.caption("RetailPulse • Sales Performance Dashboard")

st.markdown("---")

# --------------------------------------------------
# Load Data
# --------------------------------------------------
df = load_retail_data()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------
st.sidebar.header("Filters")

selected_country = st.sidebar.selectbox(
    "Country",
    ["All"] + sorted(df["Country"].dropna().unique().tolist())
)

if selected_country != "All":
    df = df[df["Country"] == selected_country]

# --------------------------------------------------
# KPIs
# --------------------------------------------------
kpis = get_basic_kpis(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Revenue", f"£{kpis['Total Revenue']:,.2f}")
col2.metric("Orders", f"{kpis['Orders']:,}")
col3.metric("Customers", f"{kpis['Customers']:,}")
col4.metric("Products", f"{kpis['Products']:,}")

st.markdown("---")

st.subheader("Monthly Revenue Trend")

st.plotly_chart(
    create_monthly_sales_chart(df),
    use_container_width=True,
)

monthly_orders = (
    df.groupby("InvoiceMonthYear", as_index=False)["InvoiceID"]
      .nunique()
      .sort_values("InvoiceMonthYear")
)

fig = px.line(
    monthly_orders,
    x="InvoiceMonthYear",
    y="InvoiceID",
    markers=True,
    title="Monthly Orders"
)

fig.update_layout(
    template="plotly_white",
    height=450,
    title_x=0.5,
)

st.markdown("---")
st.subheader("🌍 Revenue by Country")

country_sales = (
    df.groupby("Country", as_index=False)["TotalAmount"]
      .sum()
      .sort_values("TotalAmount", ascending=False)
      .head(10)
)

fig_country = px.bar(
    country_sales,
    x="TotalAmount",
    y="Country",
    orientation="h",
    title="Top 10 Countries by Revenue",
    labels={
        "TotalAmount": "Revenue (£)",
        "Country": "Country"
    }
)

fig_country.update_layout(
    template="plotly_white",
    height=450,
    title_x=0.5
)

st.plotly_chart(
    fig_country,
    use_container_width=True
)

st.subheader("📅 Revenue by Weekday")

weekday_order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]

weekday_sales = (
    df.groupby("DayName", as_index=False)["TotalAmount"]
      .sum()
)

weekday_sales["DayName"] = pd.Categorical(
    weekday_sales["DayName"],
    categories=weekday_order,
    ordered=True
)

weekday_sales = weekday_sales.sort_values("DayName")

fig_weekday = px.bar(
    weekday_sales,
    x="DayName",
    y="TotalAmount",
    title="Revenue by Weekday"
)

fig_weekday.update_layout(
    template="plotly_white",
    height=450,
    title_x=0.5
)

st.plotly_chart(
    fig_weekday,
    use_container_width=True
)

st.subheader("🕒 Hourly Revenue")

hourly_sales = (
    df.groupby("InvoiceHour", as_index=False)["TotalAmount"]
      .sum()
)

fig_hour = px.line(
    hourly_sales,
    x="InvoiceHour",
    y="TotalAmount",
    markers=True,
    title="Revenue by Hour"
)

fig_hour.update_layout(
    template="plotly_white",
    height=450,
    title_x=0.5
)

st.plotly_chart(
    fig_hour,
    use_container_width=True
)

st.subheader("🏆 Top Selling Products")

top_products = (
    df.groupby("ProductDescription", as_index=False)
      .agg(
          Revenue=("TotalAmount", "sum"),
          Quantity=("Quantity", "sum")
      )
      .sort_values("Revenue", ascending=False)
      .head(10)
)

fig_products = px.bar(
    top_products,
    x="Revenue",
    y="ProductDescription",
    orientation="h",
    title="Top 10 Products by Revenue"
)

fig_products.update_layout(
    template="plotly_white",
    height=500,
    title_x=0.5
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.subheader("📋 Sales Transactions")

display_columns = [
    "InvoiceID",
    "InvoiceDate",
    "CustomerID",
    "Country",
    "ProductDescription",
    "Quantity",
    "UnitPrice",
    "TotalAmount",
]

st.dataframe(
    df[display_columns],
    use_container_width=True,
    hide_index=True,
)

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Sales Data",
    data=csv,
    file_name="sales_analytics.csv",
    mime="text/csv",
)

st.markdown("---")
st.subheader("📌 Business Summary")

highest_country = (
    df.groupby("Country")["TotalAmount"]
    .sum()
    .idxmax()
)

highest_product = (
    df.groupby("ProductDescription")["TotalAmount"]
    .sum()
    .idxmax()
)

highest_month = (
    df.groupby("MonthName")["TotalAmount"]
    .sum()
    .idxmax()
)

avg_order = (
    df["TotalAmount"].sum()
    / df["InvoiceID"].nunique()
)

avg_basket = df["BasketSize"].mean()

weekend_sales = (
    df[df["IsWeekend"]]["TotalAmount"].sum()
)

total_sales = df["TotalAmount"].sum()

weekend_percentage = (
    weekend_sales / total_sales * 100
)

col1, col2 = st.columns(2)

with col1:
    st.info(f"""
### 📊 Revenue Insights

• Highest Revenue Country: **{highest_country}**

• Highest Revenue Month: **{highest_month}**

• Average Order Value: **£{avg_order:,.2f}**
""")

with col2:
    st.info(f"""
### 🛒 Product Insights

• Top Product: **{highest_product}**

• Average Basket Size: **{avg_basket:.2f}**

• Weekend Sales: **{weekend_percentage:.2f}%**
""")

    st.markdown("---")

st.caption(
    """
RetailPulse • Sales Analytics Dashboard

Data Source:
Processed Retail Dataset

Notebook Outputs:
Read-only

Models:
Not Used On This Page
"""
)