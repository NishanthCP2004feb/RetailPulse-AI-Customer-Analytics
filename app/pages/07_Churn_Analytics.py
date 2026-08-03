# ==========================================================
# Imports
# ==========================================================

import streamlit as st
import pandas as pd
import plotly.express as px

from utils.theme import load_css

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Customer Churn Analytics",
    page_icon="⚠️",
    layout="wide",
)

load_css()

# ==========================================================
# Header
# ==========================================================

st.title("⚠️ Customer Churn Analytics")

st.caption(
    "RetailPulse • Customer Retention Dashboard"
)

st.markdown("---")

# ==========================================================
# Load Report
# ==========================================================

@st.cache_data
def load_churn_data():

    df = pd.read_csv(
        "reports/high_risk_customers.csv"
    )

    df["FirstPurchase"] = pd.to_datetime(df["FirstPurchase"])
    df["LastPurchase"] = pd.to_datetime(df["LastPurchase"])

    return df

df = load_churn_data()

if df.empty:
    st.error("No churn data available.")
    st.stop()

# ==========================================================
# Sidebar Filters
# ==========================================================

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

status_options = sorted(
    df["PredictedChurn"].astype(str).unique()
)

selected_status = st.sidebar.multiselect(
    "Predicted Churn",
    status_options,
    default=status_options,
)

filtered_df = df[
    (df["ChurnProbability"] >= selected_probability)
    &
    (
        df["PredictedChurn"]
        .astype(str)
        .isin(selected_status)
    )
]

if filtered_df.empty:
    st.warning(
        "No customers found for selected filters."
    )
    st.stop()

# ==========================================================
# KPI Calculations
# ==========================================================

total_customers = len(filtered_df)

high_risk_customers = (
    filtered_df["PredictedChurn"]
    .astype(str)
    .str.lower()
    .isin(["1", "true", "yes"])
    .sum()
)

average_probability = (
    filtered_df["ChurnProbability"]
    .mean()
)

average_lifetime = (
    filtered_df["CustomerLifetimeDays"]
    .mean()
)

revenue_at_risk = (
    filtered_df.loc[
        filtered_df["PredictedChurn"]
        .astype(str)
        .str.lower()
        .isin(["1", "true", "yes"]),
        "Monetary",
    ].sum()
)

average_revenue = (
    filtered_df["Monetary"]
    .mean()
)

# ==========================================================
# KPI Cards
# ==========================================================

st.subheader("📊 Churn Overview")

k1, k2, k3 = st.columns(3)

k1.metric(
    "Customers",
    f"{total_customers:,}"
)

k2.metric(
    "High Risk",
    f"{high_risk_customers:,}"
)

k3.metric(
    "Avg Churn Probability",
    f"{average_probability:.2%}"
)

k4, k5, k6 = st.columns(3)

k4.metric(
    "Revenue At Risk",
    f"£{revenue_at_risk:,.2f}"
)

k5.metric(
    "Avg Lifetime",
    f"{average_lifetime:.0f} Days"
)

k6.metric(
    "Avg Customer Revenue",
    f"£{average_revenue:,.2f}"
)

st.markdown("---")

# ==========================================================
# Churn Distribution
# ==========================================================

left_chart, right_chart = st.columns(2)

with left_chart:

    st.subheader("📊 Predicted Churn Distribution")

    churn_distribution = (
        filtered_df["PredictedChurn"]
        .astype(str)
        .value_counts()
        .reset_index()
    )

    churn_distribution.columns = [
        "PredictedChurn",
        "Customers",
    ]

    fig_churn_distribution = px.pie(
        churn_distribution,
        names="PredictedChurn",
        values="Customers",
        hole=0.45,
        title="Customer Churn Distribution",
    )

    fig_churn_distribution.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
    )

    st.plotly_chart(
        fig_churn_distribution,
        use_container_width=True,
        key="churn_distribution_chart",
    )

# ==========================================================
# Churn Probability Distribution
# ==========================================================

with right_chart:

    st.subheader("📈 Churn Probability Distribution")

    fig_probability = px.histogram(
        filtered_df,
        x="ChurnProbability",
        nbins=30,
        title="Probability Distribution",
    )

    fig_probability.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
    )

    st.plotly_chart(
        fig_probability,
        use_container_width=True,
        key="probability_distribution_chart",
    )

st.markdown("---")

# ==========================================================
# Revenue at Risk
# ==========================================================

left_revenue, right_revenue = st.columns(2)

with left_revenue:

    st.subheader("💰 Revenue at Risk")

    revenue_risk = (
        filtered_df
        .sort_values(
            "Monetary",
            ascending=False,
        )
        .head(10)
    )

    fig_revenue_risk = px.bar(
        revenue_risk,
        x="CustomerID",
        y="Monetary",
        color="ChurnProbability",
        text_auto=".2s",
        title="Top Revenue at Risk",
    )

    fig_revenue_risk.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
        xaxis_title="Customer",
        yaxis_title="Revenue (£)",
    )

    st.plotly_chart(
        fig_revenue_risk,
        use_container_width=True,
        key="revenue_at_risk_chart",
    )

# ==========================================================
# Recency vs Churn Probability
# ==========================================================

with right_revenue:

    st.subheader("🔄 Recency vs Churn Probability")

    fig_recency = px.scatter(
        filtered_df,
        x="Recency",
        y="ChurnProbability",
        color="Monetary",
        size="Monetary",
        hover_name="CustomerID",
        title="Recency vs Churn Probability",
    )

    fig_recency.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
    )

    st.plotly_chart(
        fig_recency,
        use_container_width=True,
        key="recency_probability_chart",
    )

st.markdown("---")

# ==========================================================
# Customer Lifetime Distribution
# ==========================================================

st.subheader("📅 Customer Lifetime Distribution")

fig_lifetime = px.histogram(
    filtered_df,
    x="CustomerLifetimeDays",
    nbins=35,
    color="PredictedChurn",
    title="Customer Lifetime",
)

fig_lifetime.update_layout(
    template="plotly_white",
    height=500,
    title_x=0.5,
)

st.plotly_chart(
    fig_lifetime,
    use_container_width=True,
    key="customer_lifetime_chart",
)

st.markdown("---")

# ==========================================================
# Customer Search
# ==========================================================

st.subheader("🔍 Customer Search")

search_customer = st.text_input(
    "Search Customer ID",
    placeholder="Enter Customer ID..."
)

display_df = filtered_df.copy()

if search_customer:

    display_df = display_df[
        display_df["CustomerID"]
        .astype(str)
        .str.contains(
            search_customer,
            case=False,
            na=False,
        )
    ]

# ==========================================================
# Revenue vs Lifetime Analysis
# ==========================================================

left_scatter, right_scatter = st.columns(2)

with left_scatter:

    st.subheader("💰 Revenue vs Customer Lifetime")

    fig_revenue_lifetime = px.scatter(
        filtered_df,
        x="CustomerLifetimeDays",
        y="Monetary",
        size="ChurnProbability",
        color="ChurnProbability",
        hover_name="CustomerID",
        title="Revenue vs Customer Lifetime"
    )

    fig_revenue_lifetime.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
        xaxis_title="Lifetime (Days)",
        yaxis_title="Revenue (£)"
    )

    st.plotly_chart(
        fig_revenue_lifetime,
        use_container_width=True,
        key="revenue_lifetime_chart"
    )

with right_scatter:

    st.subheader("📦 Frequency vs Monetary")

    fig_frequency = px.scatter(
        filtered_df,
        x="Frequency",
        y="Monetary",
        size="Frequency",
        color="ChurnProbability",
        hover_name="CustomerID",
        title="Frequency vs Monetary Value"
    )

    fig_frequency.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5
    )

    st.plotly_chart(
        fig_frequency,
        use_container_width=True,
        key="frequency_monetary_chart"
    )

st.markdown("---")

# ==========================================================
# High Risk Customer Table
# ==========================================================

st.subheader("📋 High Risk Customer Details")

display_columns = [
    "CustomerID",
    "Recency",
    "Frequency",
    "Monetary",
    "CustomerLifetimeDays",
    "RevenuePerMonth",
    "ChurnProbability",
    "PredictedChurn",
]

st.dataframe(
    display_df[display_columns]
    .sort_values(
        "ChurnProbability",
        ascending=False
    ),
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")

# ==========================================================
# Download Report
# ==========================================================

download_csv = (
    display_df
    .to_csv(index=False)
    .encode("utf-8")
)

st.download_button(
    label="📥 Download High Risk Customers",
    data=download_csv,
    file_name="high_risk_customers.csv",
    mime="text/csv",
)

st.markdown("---")

# ==========================================================
# Business Insights
# ==========================================================

highest_probability = (
    filtered_df
    .sort_values(
        "ChurnProbability",
        ascending=False
    )
    .iloc[0]
)

highest_revenue = (
    filtered_df
    .sort_values(
        "Monetary",
        ascending=False
    )
    .iloc[0]
)

highest_recency = (
    filtered_df
    .sort_values(
        "Recency",
        ascending=False
    )
    .iloc[0]
)

left_info, right_info = st.columns(2)

with left_info:

    st.success(
        f"""
### ⚠️ Highest Risk Customer

Customer ID

**{highest_probability['CustomerID']}**

Probability

**{highest_probability['ChurnProbability']:.2%}**

Revenue

**£{highest_probability['Monetary']:,.2f}**
"""
    )

with right_info:

    st.success(
        f"""
### 💰 Revenue Risk

Highest Revenue Customer

**{highest_revenue['CustomerID']}**

Revenue

**£{highest_revenue['Monetary']:,.2f}**

Longest Inactive Customer

**{highest_recency['CustomerID']}**
"""
    )

st.markdown("---")

# ==========================================================
# Executive Churn Summary
# ==========================================================

st.subheader("📊 Executive Churn Summary")

churn_rate = (
    high_risk_customers / total_customers * 100
    if total_customers > 0 else 0
)

average_revenue_per_month = (
    filtered_df["RevenuePerMonth"].mean()
)

summary_left, summary_right = st.columns(2)

with summary_left:

    st.info(
        f"""
### 📈 Customer Portfolio

Customers Analysed

**{total_customers:,}**

High Risk Customers

**{high_risk_customers:,}**

Estimated Churn Rate

**{churn_rate:.2f}%**
"""
    )

with summary_right:

    st.info(
        f"""
### 💰 Financial Impact

Revenue At Risk

**£{revenue_at_risk:,.2f}**

Average Revenue / Month

**£{average_revenue_per_month:,.2f}**

Average Customer Lifetime

**{average_lifetime:.0f} Days**
"""
    )

st.markdown("---")

# ==========================================================
# Customer Retention Recommendations
# ==========================================================

st.subheader("💡 Retention Recommendations")

recommendations = []

if churn_rate >= 40:
    recommendations.append(
        "Customer churn is high. Prioritize immediate retention campaigns for high-risk customers."
    )
elif churn_rate >= 20:
    recommendations.append(
        "Customer churn is moderate. Focus on proactive engagement and personalized offers."
    )
else:
    recommendations.append(
        "Customer churn is under control. Continue monitoring customer behavior regularly."
    )

if average_probability >= 0.75:
    recommendations.append(
        "Many customers show a high probability of churn. Review inactive customer segments."
    )

if revenue_at_risk > 0:
    recommendations.append(
        "Protect high-value customers by offering loyalty rewards and targeted promotions."
    )

recommendations.append(
    "Use churn predictions as a decision-support tool. Retraining should only be performed through the notebook workflow."
)

for index, recommendation in enumerate(recommendations, start=1):
    st.write(f"{index}. {recommendation}")

st.markdown("---")

# ==========================================================
# Churn Health Status
# ==========================================================

st.subheader("🚦 Churn Health")

if churn_rate < 10:
    st.success("Churn Health: Excellent")

elif churn_rate < 20:
    st.success("Churn Health: Good")

elif churn_rate < 35:
    st.warning("Churn Health: Moderate Risk")

else:
    st.error("Churn Health: High Risk")

st.markdown("---")

# ==========================================================
# Footer
# ==========================================================

st.caption(
    """
RetailPulse

Customer Churn Analytics Dashboard

Notebook Outputs : Read Only

Report :
high_risk_customers.csv

Version : 1.0
"""
)