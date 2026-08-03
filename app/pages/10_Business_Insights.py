# ==========================================================
# Imports
# ==========================================================

import streamlit as st
import pandas as pd

from utils.theme import load_css

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Business Insights",
    page_icon="📊",
    layout="wide",
)

load_css()

# ==========================================================
# Header
# ==========================================================

st.title("📊 Business Insights")

st.caption(
    "RetailPulse • Executive Business Intelligence Dashboard"
)

st.markdown("---")

# ==========================================================
# Load Reports
# ==========================================================

@st.cache_data
def load_reports():

    forecast = pd.read_csv(
        "reports/forecast_results.csv"
    )

    model = pd.read_csv(
        "reports/forecasting_model_comparison.csv"
    )

    churn = pd.read_csv(
        "reports/high_risk_customers.csv"
    )

    inventory = pd.read_csv(
        "reports/inventory_summary.csv"
    )

    recommendations = pd.read_csv(
        "reports/customer_product_recommendations.csv"
    )

    business = pd.read_csv(
        "reports/business_recommendations.csv"
    )

    return (
        forecast,
        model,
        churn,
        inventory,
        recommendations,
        business,
    )


(
    forecast_df,
    model_df,
    churn_df,
    inventory_df,
    recommendation_df,
    business_df,
) = load_reports()

# ==========================================================
# Executive KPIs
# ==========================================================

best_model = (
    model_df
    .sort_values("RMSE")
    .iloc[0]["Model"]
)

forecast_days = len(forecast_df)

customers = len(churn_df)

high_risk = (
    churn_df["PredictedChurn"]
    .astype(str)
    .isin(["1", "True", "true"])
    .sum()
)

inventory_products = len(inventory_df)

recommended_customers = len(recommendation_df)

business_rules = len(business_df)

# ==========================================================
# KPI Cards
# ==========================================================

st.subheader("📈 Executive Overview")

k1, k2, k3 = st.columns(3)

k1.metric(
    "Forecast Model",
    best_model,
)

k2.metric(
    "Forecast Days",
    forecast_days,
)

k3.metric(
    "Business Rules",
    business_rules,
)

k4, k5, k6 = st.columns(3)

k4.metric(
    "Customers",
    f"{customers:,}",
)

k5.metric(
    "High Risk Customers",
    f"{high_risk:,}",
)

k6.metric(
    "Inventory Products",
    f"{inventory_products:,}",
)

st.markdown("---")

# ==========================================================
# Executive Business Health
# ==========================================================

import plotly.express as px

left_health, right_health = st.columns(2)

with left_health:

    st.subheader("📊 Business Module Coverage")

    coverage_df = pd.DataFrame(
        {
            "Module": [
                "Forecasting",
                "Churn",
                "Inventory",
                "Recommendations",
            ],
            "Records": [
                len(forecast_df),
                len(churn_df),
                len(inventory_df),
                len(recommendation_df),
            ],
        }
    )

    fig_modules = px.bar(
        coverage_df,
        x="Module",
        y="Records",
        color="Records",
        text_auto=True,
        title="Business Data Coverage"
    )

    fig_modules.update_layout(
        template="plotly_white",
        height=450,
        title_x=0.5,
    )

    st.plotly_chart(
        fig_modules,
        use_container_width=True,
        key="business_module_coverage"
    )

with right_health:

    st.subheader("📈 Forecast Model Performance")

    fig_model = px.bar(
        model_df,
        x="Model",
        y="RMSE",
        color="RMSE",
        text_auto=".2f",
        title="Forecast Model RMSE"
    )

    fig_model.update_layout(
        template="plotly_white",
        height=450,
        title_x=0.5,
    )

    st.plotly_chart(
        fig_model,
        use_container_width=True,
        key="business_forecast_model"
    )

st.markdown("---")

# ==========================================================
# Churn & Recommendation Summary
# ==========================================================

left_churn, right_recommendation = st.columns(2)

with left_churn:

    st.subheader("⚠️ Churn Summary")

    churn_counts = (
        churn_df["PredictedChurn"]
        .astype(str)
        .value_counts()
        .reset_index()
    )

    churn_counts.columns = [
        "Status",
        "Customers",
    ]

    fig_churn = px.pie(
        churn_counts,
        names="Status",
        values="Customers",
        hole=0.45,
        title="Predicted Customer Churn"
    )

    fig_churn.update_layout(
        template="plotly_white",
        height=450,
        title_x=0.5,
    )

    st.plotly_chart(
        fig_churn,
        use_container_width=True,
        key="business_churn_summary"
    )

with right_recommendation:

    st.subheader("🎯 Customer Segments")

    segment_summary = (
        recommendation_df["Segment"]
        .value_counts()
        .reset_index()
    )

    segment_summary.columns = [
        "Segment",
        "Customers",
    ]

    fig_segments = px.bar(
        segment_summary,
        x="Segment",
        y="Customers",
        color="Customers",
        text_auto=True,
        title="Customer Segments"
    )

    fig_segments.update_layout(
        template="plotly_white",
        height=450,
        title_x=0.5,
    )

    st.plotly_chart(
        fig_segments,
        use_container_width=True,
        key="business_segment_summary"
    )

st.markdown("---")

# ==========================================================
# Inventory Status Summary
# ==========================================================

st.subheader("📦 Inventory Status")

inventory_status = (
    inventory_df["InventoryStatus"]
    .value_counts()
    .reset_index()
)

inventory_status.columns = [
    "InventoryStatus",
    "Products",
]

fig_inventory = px.bar(
    inventory_status,
    x="InventoryStatus",
    y="Products",
    color="Products",
    text_auto=True,
    title="Inventory Status Distribution"
)

fig_inventory.update_layout(
    template="plotly_white",
    height=500,
    title_x=0.5,
)

st.plotly_chart(
    fig_inventory,
    use_container_width=True,
    key="business_inventory_summary"
)

st.markdown("---")

# ==========================================================
# Notebook Business Recommendations
# ==========================================================

st.subheader("💡 Notebook Generated Business Recommendations")

st.dataframe(
    business_df,
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")

# ==========================================================
# Forecast Executive Summary
# ==========================================================

st.subheader("📈 Forecast Executive Summary")

forecast_summary = forecast_df.copy()

forecast_summary["ForecastError"] = (
    forecast_summary["PredictedSales"]
    - forecast_summary["ActualSales"]
)

forecast_summary["AbsoluteError"] = (
    forecast_summary["ForecastError"].abs()
)

total_actual_sales = (
    forecast_summary["ActualSales"].sum()
)

total_predicted_sales = (
    forecast_summary["PredictedSales"].sum()
)

average_error = (
    forecast_summary["AbsoluteError"].mean()
)

forecast_left, forecast_right = st.columns(2)

with forecast_left:

    st.info(
        f"""
### Forecast Overview

Total Actual Sales

**{total_actual_sales:,.2f}**

Total Predicted Sales

**{total_predicted_sales:,.2f}**

Average Forecast Error

**{average_error:.2f}**
"""
    )

with forecast_right:

    best_rmse = (
        model_df["RMSE"].min()
    )

    best_mae = (
        model_df["MAE"].min()
    )

    st.info(
        f"""
### Forecast Model

Best Model

**{best_model}**

Lowest RMSE

**{best_rmse:.2f}**

Lowest MAE

**{best_mae:.2f}**
"""
    )

st.markdown("---")

# ==========================================================
# Cross Module Executive Summary
# ==========================================================

st.subheader("📊 Cross Module Summary")

summary_df = pd.DataFrame(
    {
        "Business Area": [
            "Forecasting",
            "Churn",
            "Inventory",
            "Recommendations",
        ],
        "Records": [
            len(forecast_df),
            len(churn_df),
            len(inventory_df),
            len(recommendation_df),
        ],
    }
)

st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")

# ==========================================================
# Executive Downloads
# ==========================================================

left_download, right_download = st.columns(2)

with left_download:

    executive_csv = (
        summary_df
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        label="📥 Download Executive Summary",
        data=executive_csv,
        file_name="executive_summary.csv",
        mime="text/csv",
    )

with right_download:

    recommendation_csv = (
        business_df
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        label="📥 Download Business Recommendations",
        data=recommendation_csv,
        file_name="business_recommendations.csv",
        mime="text/csv",
    )

st.markdown("---")

# ==========================================================
# Executive Performance Scorecard
# ==========================================================

st.subheader("📈 Executive Performance Scorecard")

scorecard = pd.DataFrame(
    {
        "Business Area": [
            "Forecasting",
            "Customer Churn",
            "Inventory",
            "Recommendations",
        ],
        "Key Metric": [
            best_model,
            f"{high_risk:,} High Risk Customers",
            f"{inventory_products:,} Products",
            f"{recommended_customers:,} Customers",
        ],
        "Status": [
            "Operational",
            "Monitoring",
            "Operational",
            "Operational",
        ],
    }
)

st.dataframe(
    scorecard,
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")

# ==========================================================
# Business Health Indicators
# ==========================================================

st.subheader("📊 Business Health Indicators")

indicator1, indicator2, indicator3, indicator4 = st.columns(4)

forecast_accuracy = (
    100
    - (
        (
            (forecast_df["PredictedSales"] - forecast_df["ActualSales"])
            .abs()
            .mean()
        )
        / forecast_df["ActualSales"].mean()
        * 100
    )
)

forecast_accuracy = max(0, min(forecast_accuracy, 100))

churn_rate = (
    (high_risk / customers) * 100
    if customers > 0 else 0
)

inventory_health = (
    (
        inventory_df["InventoryStatus"]
        .astype(str)
        .str.contains(
            "high",
            case=False,
            na=False,
        )
    ).sum()
    / inventory_products
    * 100
)

recommendation_coverage = (
    recommended_customers
    / customers
    * 100
    if customers > 0 else 0
)

indicator1.metric(
    "Forecast Accuracy",
    f"{forecast_accuracy:.1f}%"
)

indicator2.metric(
    "Churn Rate",
    f"{churn_rate:.1f}%"
)

indicator3.metric(
    "Inventory Health",
    f"{inventory_health:.1f}%"
)

indicator4.metric(
    "Recommendation Coverage",
    f"{recommendation_coverage:.1f}%"
)

st.markdown("---")

# ==========================================================
# Executive Risk Dashboard
# ==========================================================

st.subheader("🚨 Executive Risk Dashboard")

risk_left, risk_right = st.columns(2)

with risk_left:

    st.warning(
        f"""
### Business Risks

• High Risk Customers

**{high_risk:,}**

• Forecast Days

**{forecast_days}**

• Inventory Products

**{inventory_products:,}**
"""
    )

with risk_right:

    st.success(
        f"""
### Business Strengths

• Best Forecast Model

**{best_model}**

• Recommendation Records

**{recommended_customers:,}**

• Business Recommendations

**{business_rules}**
"""
    )

st.markdown("---")

# ==========================================================
# Management Summary
# ==========================================================

st.subheader("📋 Management Summary")

management_summary = pd.DataFrame(
    {
        "Area": [
            "Forecasting",
            "Customer Analytics",
            "Inventory",
            "Recommendation Engine",
        ],
        "Current Status": [
            "Operational",
            "Monitoring",
            "Operational",
            "Operational",
        ],
        "Primary Focus": [
            "Demand Planning",
            "Customer Retention",
            "Stock Optimization",
            "Cross-selling",
        ],
    }
)

st.dataframe(
    management_summary,
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")

# ==========================================================
# Executive Action Plan
# ==========================================================

st.subheader("🎯 Executive Action Plan")

action_plan = [
    "Continue using the best-performing forecasting model for demand planning.",
    "Prioritize retention campaigns for high-risk customers identified by the churn model.",
    "Follow notebook-generated inventory recommendations to optimize stock levels.",
    "Use personalized product recommendations to improve cross-selling opportunities.",
    "Monitor business KPIs regularly through the RetailPulse dashboard.",
]

for i, action in enumerate(action_plan, start=1):
    st.write(f"{i}. {action}")

st.markdown("---")

# ==========================================================
# CEO Executive Summary
# ==========================================================

st.subheader("📊 CEO Executive Summary")

st.info(
    f"""
### RetailPulse Executive Report

Forecasting Model
**{best_model}**

Forecast Period
**{forecast_days} Days**

Customers Analysed
**{customers:,}**

Inventory Products
**{inventory_products:,}**

Recommendation Records
**{recommended_customers:,}**

Business Recommendations
**{business_rules}**
"""
)

st.markdown("---")

# ==========================================================
# Overall Business Health
# ==========================================================

st.subheader("🚦 Overall Business Health")

health_score = 0

if forecast_accuracy >= 90:
    health_score += 25
elif forecast_accuracy >= 80:
    health_score += 20
else:
    health_score += 10

if churn_rate < 20:
    health_score += 25
elif churn_rate < 35:
    health_score += 20
else:
    health_score += 10

if inventory_health >= 50:
    health_score += 25
elif inventory_health >= 30:
    health_score += 20
else:
    health_score += 10

if recommendation_coverage >= 70:
    health_score += 25
elif recommendation_coverage >= 40:
    health_score += 20
else:
    health_score += 10

if health_score >= 90:
    st.success(f"Overall Business Health: Excellent ({health_score}/100)")
elif health_score >= 75:
    st.success(f"Overall Business Health: Good ({health_score}/100)")
elif health_score >= 60:
    st.warning(f"Overall Business Health: Moderate ({health_score}/100)")
else:
    st.error(f"Overall Business Health: Needs Attention ({health_score}/100)")

st.progress(health_score / 100)

st.markdown("---")

# ==========================================================
# Executive Notes
# ==========================================================

st.subheader("📝 Executive Notes")

st.markdown(
    """
- This dashboard is generated from notebook-produced reports.
- All analytics displayed are read-only visualizations.
- Forecasting, churn prediction, inventory optimization, and recommendation logic remain in the notebook pipeline.
- Streamlit serves as the presentation and decision-support layer.
"""
)

st.markdown("---")

# ==========================================================
# Footer
# ==========================================================

st.caption(
    """
RetailPulse

Executive Business Intelligence Dashboard

Notebook Outputs : Read Only

Integrated Reports:
• forecast_results.csv
• forecasting_model_comparison.csv
• high_risk_customers.csv
• inventory_summary.csv
• inventory_recommendations.csv
• customer_product_recommendations.csv
• business_recommendations.csv

Version : 1.0
"""
)
