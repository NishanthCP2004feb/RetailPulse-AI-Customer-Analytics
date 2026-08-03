import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from utils.theme import (
    load_css, page_header, section_header, dashboard_divider, 
    dashboard_footer, kpi_card, success_banner, info_banner, warning_banner
)
from utils.data_loader import load_retail_data
from utils.helpers import (
    format_currency, format_number, format_percentage, 
    format_compact_currency, safe_divide
)
from utils.metrics import get_country_kpis, get_total_revenue, get_total_orders, get_total_customers
from utils.chart_utils import (
    create_horizontal_bar_chart, create_pie_chart, create_scatter_chart, 
    create_histogram, apply_chart_layout
)

# Initialize Page
load_css()
page_header('🌍 Country Analytics', 'RetailPulse • Geographic Revenue & Market Analysis')
dashboard_divider()

# Load Data
df = load_retail_data()

if df.empty:
    st.error("No data available.")
    st.stop()

# Sidebar Filters
st.sidebar.header("🌍 Country Filters")
years = sorted(df["InvoiceYear"].dropna().unique())
selected_years = st.sidebar.multiselect("Invoice Year", years, default=years, key="country_years")

months = sorted(df["MonthName"].dropna().unique())
selected_months = st.sidebar.multiselect("Month", months, default=months, key="country_months")

filtered_df = df[
    (df["InvoiceYear"].isin(selected_years)) &
    (df["MonthName"].isin(selected_months))
]

if filtered_df.empty:
    warning_banner("No records found for selected filters.")
    st.stop()

# Country Summary logic
country_summary = (
    filtered_df
    .groupby("Country", as_index=False)
    .agg(
        Revenue=("TotalAmount", "sum"),
        Orders=("InvoiceID", "nunique"),
        Customers=("CustomerID", "nunique"),
        Quantity=("Quantity", "sum"),
        AvgBasket=("BasketValue", "mean"),
    )
)
country_summary["AverageOrderValue"] = safe_divide(country_summary["Revenue"], country_summary["Orders"])
country_summary = country_summary.sort_values("Revenue", ascending=False).reset_index(drop=True)

# KPIs
total_countries = len(country_summary)
total_revenue = country_summary["Revenue"].sum()
total_orders = country_summary["Orders"].sum()
total_customers = country_summary["Customers"].sum()
average_country_revenue = safe_divide(total_revenue, total_countries)
top_country = country_summary.iloc[0]["Country"] if total_countries > 0 else "-"

section_header("📊 Country Overview")
st.markdown('<div class="rp-kpi-grid">', unsafe_allow_html=True)
kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
with kpi1: st.markdown(kpi_card("Countries", format_number(total_countries), "🌍"), unsafe_allow_html=True)
with kpi2: st.markdown(kpi_card("Total Revenue", format_compact_currency(total_revenue), "💰"), unsafe_allow_html=True)
with kpi3: st.markdown(kpi_card("Total Orders", format_number(total_orders), "📦"), unsafe_allow_html=True)
with kpi4: st.markdown(kpi_card("Customers", format_number(total_customers), "👥"), unsafe_allow_html=True)
with kpi5: st.markdown(kpi_card("Avg Rev/Country", format_compact_currency(average_country_revenue), "🧮"), unsafe_allow_html=True)
with kpi6: st.markdown(kpi_card("Top Country", top_country, "🏆"), unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# Charts row 1: Revenue & Orders
left_chart, right_chart = st.columns(2)
with left_chart:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("💰 Top Countries by Revenue")
    top_revenue = country_summary.head(10)
    fig_rev = create_horizontal_bar_chart(top_revenue, "Revenue", "Country", color="Revenue")
    st.plotly_chart(fig_rev, width="stretch", key="chart_rev")
    st.markdown('</div>', unsafe_allow_html=True)

with right_chart:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("📦 Top Countries by Orders")
    top_orders = country_summary.sort_values("Orders", ascending=False).head(10)
    fig_ord = create_horizontal_bar_chart(top_orders, "Orders", "Country", color="Orders", text_auto=".3s")
    st.plotly_chart(fig_ord, width="stretch", key="chart_ord")
    st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# Charts row 2: Customers & AOV
left_cust, right_cust = st.columns(2)
with left_cust:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("👥 Customers by Country")
    top_customers = country_summary.sort_values("Customers", ascending=False).head(10)
    fig_cust = create_horizontal_bar_chart(top_customers, "Customers", "Country", color="Customers", text_auto=".3s")
    st.plotly_chart(fig_cust, width="stretch", key="chart_cust")
    st.markdown('</div>', unsafe_allow_html=True)

with right_cust:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("💳 Average Order Value")
    top_aov = country_summary.sort_values("AverageOrderValue", ascending=False).head(10)
    fig_aov = create_horizontal_bar_chart(top_aov, "AverageOrderValue", "Country", color="AverageOrderValue")
    st.plotly_chart(fig_aov, width="stretch", key="chart_aov")
    st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# Charts row 3: Scatter & Pie
left_scatter, right_pie = st.columns(2)
with left_scatter:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("📈 Revenue vs Customers")
    fig_scatter = create_scatter_chart(country_summary, "Customers", "Revenue", color="Revenue", size="Orders", hover_name="Country")
    st.plotly_chart(fig_scatter, width="stretch", key="chart_scatter")
    st.markdown('</div>', unsafe_allow_html=True)

with right_pie:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("🥧 Revenue Contribution")
    top_pie = country_summary.head(10).copy()
    remaining = country_summary.iloc[10:]["Revenue"].sum()
    if remaining > 0:
        top_pie.loc[len(top_pie)] = {"Country": "Others", "Revenue": remaining, "Orders": 0, "Customers": 0, "Quantity": 0, "AvgBasket": 0, "AverageOrderValue": 0}
    fig_pie = create_pie_chart(top_pie, "Country", "Revenue", hole=0.45)
    st.plotly_chart(fig_pie, width="stretch", key="chart_pie")
    st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# Charts row 4: Hist & Pareto
left_hist, right_pareto = st.columns(2)
with left_hist:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("📊 Revenue Distribution")
    fig_hist = create_histogram(country_summary, "Revenue", nbins=25)
    st.plotly_chart(fig_hist, width="stretch", key="chart_hist")
    st.markdown('</div>', unsafe_allow_html=True)

with right_pareto:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("📉 Pareto Analysis (80/20 Rule)")
    pareto = country_summary.copy()
    pareto["CumulativeRevenue"] = pareto["Revenue"].cumsum()
    pareto["CumulativePercent"] = safe_divide(pareto["CumulativeRevenue"], pareto["Revenue"].sum()) * 100
    
    fig_pareto = go.Figure()
    fig_pareto.add_trace(go.Bar(x=pareto["Country"], y=pareto["Revenue"], name="Revenue", marker_color="#2563EB"))
    fig_pareto.add_trace(go.Scatter(x=pareto["Country"], y=pareto["CumulativePercent"], mode="lines+markers", name="Cumulative %", yaxis="y2", line=dict(color="#0EA5E9", width=3)))
    
    fig_pareto.update_layout(
        xaxis=dict(showticklabels=False),
        yaxis=dict(title="Revenue (£)"),
        yaxis2=dict(overlaying="y", side="right", range=[0, 100], title="Cumulative %"),
        showlegend=False,
        hovermode="x unified",
        margin=dict(l=40, r=40, t=40, b=40)
    )
    apply_chart_layout(fig_pareto, height=450)
    st.plotly_chart(fig_pareto, width="stretch", key="chart_pareto")
    st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# Search & Table
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("📋 Country Search & Summary")
search_country = st.text_input("Search Country", placeholder="Enter country name...", key="search_country")
display_table = country_summary.copy()
if search_country:
    display_table = display_table[display_table["Country"].str.contains(search_country, case=False, na=False)]

display_table = display_table.sort_values("Revenue", ascending=False)
st.dataframe(display_table, width="stretch", hide_index=True)

st.markdown('<div class="rp-download-btn">', unsafe_allow_html=True)
csv = display_table.to_csv(index=False).encode("utf-8")
st.download_button(label="📥 Download Country Report", data=csv, file_name="country_analytics.csv", mime="text/csv", key="download_country")
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# Business Insights
with st.expander("💡 Detailed Business Insights", expanded=True):
    highest_revenue_country = country_summary.sort_values("Revenue", ascending=False).iloc[0] if total_countries > 0 else None
    highest_orders_country = country_summary.sort_values("Orders", ascending=False).iloc[0] if total_countries > 0 else None
    highest_customer_country = country_summary.sort_values("Customers", ascending=False).iloc[0] if total_countries > 0 else None
    average_order_value_all = country_summary["AverageOrderValue"].mean() if total_countries > 0 else 0
    top5_revenue = country_summary.head(5)["Revenue"].sum()
    top5_percentage = safe_divide(top5_revenue, total_revenue) * 100

    if highest_revenue_country is not None:
        col1, col2 = st.columns(2)
        with col1:
            success_banner(f"**Highest Revenue Country:** {highest_revenue_country['Country']} ({format_currency(highest_revenue_country['Revenue'])})  \n**Average Order Value:** {format_currency(average_order_value_all)}")
        with col2:
            info_banner(f"**Most Orders:** {highest_orders_country['Country']} | **Most Customers:** {highest_customer_country['Country']}  \n**Top 5 Countries** contribute {format_percentage(top5_percentage)} of total revenue.")
        
        info_banner(f"**Executive Summary:** Analyzed {total_countries} active countries driving {format_currency(total_revenue)} in total revenue from {format_number(total_orders)} orders and {format_number(total_customers)} customers.")

dashboard_footer()
