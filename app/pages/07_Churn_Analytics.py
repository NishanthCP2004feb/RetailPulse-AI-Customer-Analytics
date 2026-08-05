import streamlit as st
import pandas as pd
import plotly.express as px

from utils.theme import (
    load_css, page_header, section_header, dashboard_divider, 
    dashboard_footer, render_kpi_row, render_insight_card, 
    success_banner, warning_banner, error_banner
)
from utils.data_loader import load_churn_data
from utils.helpers import format_currency, format_number, format_percentage
from utils.chart_utils import (
    create_bar_chart, create_pie_chart, 
    create_scatter_chart, create_histogram, apply_chart_layout
)

st.set_page_config(page_title="Churn Analytics", page_icon="⚠️", layout="wide")

load_css()

page_header('⚠️ Churn Analytics', 'RetailPulse • Customer Churn Prediction & Risk Analysis')

df = load_churn_data()

if df.empty:
    error_banner("No churn data available.")
    st.stop()

st.sidebar.header("⚙️ Churn Filters")

min_probability = float(df["ChurnProbability"].min())
max_probability = float(df["ChurnProbability"].max())

selected_probability = st.sidebar.slider(
    "Minimum Churn Probability",
    min_value=round(min_probability, 2),
    max_value=round(max_probability, 2),
    value=round(min_probability, 2),
    step=0.01,
)

status_options = sorted(df["PredictedChurn"].astype(str).unique())

selected_status = st.sidebar.multiselect(
    "Predicted Churn",
    status_options,
    default=status_options,
)

filtered_df = df[
    (df["ChurnProbability"] >= selected_probability)
    & (df["PredictedChurn"].astype(str).isin(selected_status))
]

if filtered_df.empty:
    warning_banner("No customers found for selected filters.")
    st.stop()

total_customers = len(filtered_df)
high_risk_customers = filtered_df["PredictedChurn"].astype(str).str.lower().isin(["1", "true", "yes"]).sum()
average_probability = filtered_df["ChurnProbability"].mean()
average_lifetime = filtered_df["CustomerLifetimeDays"].mean()
revenue_at_risk = filtered_df.loc[filtered_df["PredictedChurn"].astype(str).str.lower().isin(["1", "true", "yes"]), "Monetary"].sum()
average_revenue = filtered_df["Monetary"].mean()

section_header("📊 Churn Overview")

kpi_data1 = [
    {"title": "Customers", "value": format_number(total_customers), "icon": "👥"},
    {"title": "High Risk", "value": format_number(high_risk_customers), "icon": "⚠️"},
    {"title": "Avg Churn Probability", "value": format_percentage(average_probability * 100), "icon": "📉"}
]
render_kpi_row(kpi_data1)

kpi_data2 = [
    {"title": "Revenue At Risk", "value": format_currency(revenue_at_risk), "icon": "💰"},
    {"title": "Avg Lifetime", "value": f"{average_lifetime:.0f} Days", "icon": "📅"},
    {"title": "Avg Customer Revenue", "value": format_currency(average_revenue), "icon": "💳"}
]
render_kpi_row(kpi_data2)

dashboard_divider()

left_chart, right_chart = st.columns(2)

with left_chart:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("📊 Predicted Churn Distribution")
    churn_distribution = filtered_df["PredictedChurn"].astype(str).value_counts().reset_index()
    churn_distribution.columns = ["PredictedChurn", "Customers"]
    
    fig_churn = create_pie_chart(
        churn_distribution, 
        names="PredictedChurn", 
        values="Customers", 
        title="Customer Churn Distribution",
        hole=0.45
    )
    apply_chart_layout(fig_churn)
    st.plotly_chart(fig_churn, use_container_width=True, key="churn_distribution_chart")
    st.markdown('</div>', unsafe_allow_html=True)

with right_chart:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("📈 Churn Probability Distribution")
    fig_prob = create_histogram(
        filtered_df,
        x="ChurnProbability",
        nbins=30,
        title="Probability Distribution"
    )
    apply_chart_layout(fig_prob)
    st.plotly_chart(fig_prob, use_container_width=True, key="probability_distribution_chart")
    st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

left_revenue, right_revenue = st.columns(2)

with left_revenue:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("💰 Revenue at Risk")
    revenue_risk = filtered_df.sort_values("Monetary", ascending=False).head(10)
    fig_rev = create_bar_chart(
        revenue_risk,
        x="CustomerID",
        y="Monetary",
        color="ChurnProbability",
        title="Top Revenue at Risk",
        text_auto=".2s"
    )
    fig_rev.update_xaxes(type="category")
    apply_chart_layout(fig_rev)
    st.plotly_chart(fig_rev, use_container_width=True, key="revenue_at_risk_chart")
    st.markdown('</div>', unsafe_allow_html=True)

with right_revenue:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("🔄 Recency vs Churn Probability")
    fig_recency = create_scatter_chart(
        filtered_df,
        x="Recency",
        y="ChurnProbability",
        color="Monetary",
        size="Monetary",
        hover_name="CustomerID",
        title="Recency vs Churn Probability"
    )
    apply_chart_layout(fig_recency)
    st.plotly_chart(fig_recency, use_container_width=True, key="recency_probability_chart")
    st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("📅 Customer Lifetime Distribution")
fig_lifetime = px.histogram(
    filtered_df,
    x="CustomerLifetimeDays",
    nbins=35,
    color="PredictedChurn",
    title="Customer Lifetime"
)
apply_chart_layout(fig_lifetime)
st.plotly_chart(fig_lifetime, use_container_width=True, key="customer_lifetime_chart")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("🔍 Customer Search")
search_customer = st.text_input("Search Customer ID", placeholder="Enter Customer ID...", key="customer_search")
display_df = filtered_df.copy()
if search_customer:
    display_df = display_df[display_df["CustomerID"].astype(str).str.contains(search_customer, case=False, na=False)]
st.markdown('</div>', unsafe_allow_html=True)

left_scatter, right_scatter = st.columns(2)

with left_scatter:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("💰 Revenue vs Customer Lifetime")
    fig_rev_life = create_scatter_chart(
        filtered_df,
        x="CustomerLifetimeDays",
        y="Monetary",
        color="ChurnProbability",
        size="ChurnProbability",
        hover_name="CustomerID",
        title="Revenue vs Customer Lifetime"
    )
    apply_chart_layout(fig_rev_life)
    st.plotly_chart(fig_rev_life, use_container_width=True, key="revenue_lifetime_chart")
    st.markdown('</div>', unsafe_allow_html=True)

with right_scatter:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("📦 Frequency vs Monetary")
    fig_freq = create_scatter_chart(
        filtered_df,
        x="Frequency",
        y="Monetary",
        color="ChurnProbability",
        size="Frequency",
        hover_name="CustomerID",
        title="Frequency vs Monetary Value"
    )
    apply_chart_layout(fig_freq)
    st.plotly_chart(fig_freq, use_container_width=True, key="frequency_monetary_chart")
    st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("📋 High Risk Customer Details")
display_columns = ["CustomerID", "Recency", "Frequency", "Monetary", "CustomerLifetimeDays", "RevenuePerMonth", "ChurnProbability", "PredictedChurn"]
st.dataframe(display_df[display_columns].sort_values("ChurnProbability", ascending=False), use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

st.markdown('<div class="rp-download-btn">', unsafe_allow_html=True)
download_csv = display_df.to_csv(index=False).encode("utf-8")
st.download_button(label="📥 Download High Risk Customers", data=download_csv, file_name="high_risk_customers.csv", mime="text/csv", key="download_high_risk_csv")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

highest_probability = filtered_df.sort_values("ChurnProbability", ascending=False).iloc[0]
highest_revenue = filtered_df.sort_values("Monetary", ascending=False).iloc[0]
highest_recency = filtered_df.sort_values("Recency", ascending=False).iloc[0]

left_info, right_info = st.columns(2)
with left_info:
    render_insight_card(
        "⚠️ Highest Risk Customer",
        f"**Customer ID:** {highest_probability['CustomerID']}\n\n**Probability:** {format_percentage(highest_probability['ChurnProbability'] * 100)}\n\n**Revenue:** {format_currency(highest_probability['Monetary'])}"
    )

with right_info:
    render_insight_card(
        "💰 Revenue Risk",
        f"**Highest Revenue Customer:** {highest_revenue['CustomerID']}\n\n**Revenue:** {format_currency(highest_revenue['Monetary'])}\n\n**Longest Inactive Customer:** {highest_recency['CustomerID']}"
    )

dashboard_divider()

section_header("📊 Executive Churn Summary")
churn_rate = (high_risk_customers / total_customers * 100) if total_customers > 0 else 0
average_revenue_per_month = filtered_df["RevenuePerMonth"].mean()

summary_left, summary_right = st.columns(2)
with summary_left:
    render_insight_card(
        "📈 Customer Portfolio",
        f"**Customers Analysed:** {format_number(total_customers)}\n\n**High Risk Customers:** {format_number(high_risk_customers)}\n\n**Estimated Churn Rate:** {format_percentage(churn_rate)}"
    )

with summary_right:
    render_insight_card(
        "💰 Financial Impact",
        f"**Revenue At Risk:** {format_currency(revenue_at_risk)}\n\n**Average Revenue / Month:** {format_currency(average_revenue_per_month)}\n\n**Average Customer Lifetime:** {average_lifetime:.0f} Days"
    )

dashboard_divider()

section_header("💡 Retention Recommendations")
with st.expander("View Retention Recommendations", expanded=True):
    recommendations = []
    if churn_rate >= 40:
        recommendations.append("Customer churn is high. Prioritize immediate retention campaigns for high-risk customers.")
    elif churn_rate >= 20:
        recommendations.append("Customer churn is moderate. Focus on proactive engagement and personalized offers.")
    else:
        recommendations.append("Customer churn is under control. Continue monitoring customer behavior regularly.")
    if average_probability >= 0.75:
        recommendations.append("Many customers show a high probability of churn. Review inactive customer segments.")
    if revenue_at_risk > 0:
        recommendations.append("Protect high-value customers by offering loyalty rewards and targeted promotions.")
    recommendations.append("Use churn predictions as a decision-support tool. Retraining should only be performed through the notebook workflow.")
    for index, recommendation in enumerate(recommendations, start=1):
        st.write(f"{index}. {recommendation}")

dashboard_divider()

section_header("🚦 Churn Health")
if churn_rate < 10:
    success_banner("Churn Health: Excellent")
elif churn_rate < 20:
    success_banner("Churn Health: Good")
elif churn_rate < 35:
    warning_banner("Churn Health: Moderate Risk")
else:
    error_banner("Churn Health: High Risk")

dashboard_footer()