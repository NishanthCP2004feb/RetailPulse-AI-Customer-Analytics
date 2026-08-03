import streamlit as st
import pandas as pd
import plotly.express as px

from utils.theme import (
    load_css,
    page_header,
    section_header,
    dashboard_divider,
    dashboard_footer,
    render_kpi_row,
    render_insight_card,
    success_banner,
    warning_banner,
    info_banner
)

from utils.data_loader import (
    load_business_reports,
    load_forecast_results,
    load_forecast_model_comparison,
    load_churn_data,
    load_inventory_summary,
    load_recommendations,
    load_business_recommendations
)

from utils.helpers import (
    format_currency,
    format_number,
    format_percentage
)

from utils.chart_utils import (
    create_bar_chart,
    create_pie_chart,
    apply_chart_layout
)

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
page_header("📊 Business Insights", "RetailPulse • Executive Business Intelligence Dashboard")

# ==========================================================
# Load Reports
# ==========================================================
try:
    (
        forecast_df,
        model_df,
        churn_df,
        inventory_df,
        recommendation_df,
        business_df,
    ) = load_business_reports()
except Exception as e:
    st.error(f"Error loading business reports: {e}")
    st.stop()

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
section_header("📈 Executive Overview")

kpis1 = [
    {"title": "Forecast Model", "value": best_model, "icon": "📈"},
    {"title": "Forecast Days", "value": format_number(forecast_days), "icon": "📅"},
    {"title": "Business Rules", "value": format_number(business_rules), "icon": "💡"},
]
render_kpi_row(kpis1)

kpis2 = [
    {"title": "Customers", "value": format_number(customers), "icon": "👥"},
    {"title": "High Risk Customers", "value": format_number(high_risk), "icon": "⚠️"},
    {"title": "Inventory Products", "value": format_number(inventory_products), "icon": "📦"},
]
render_kpi_row(kpis2)

dashboard_divider()

# ==========================================================
# Executive Business Health
# ==========================================================
left_health, right_health = st.columns(2)

with left_health:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("📊 Business Module Coverage")

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

    fig_modules = create_bar_chart(
        coverage_df,
        x="Module",
        y="Records",
        title="Business Data Coverage",
        text_auto=True
    )

    st.plotly_chart(
        fig_modules,
        width="stretch",
        key="business_module_coverage"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with right_health:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("📈 Forecast Model Performance")

    fig_model = create_bar_chart(
        model_df,
        x="Model",
        y="RMSE",
        title="Forecast Model RMSE",
        text_auto=".2f"
    )

    st.plotly_chart(
        fig_model,
        width="stretch",
        key="business_forecast_model"
    )
    st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Churn & Recommendation Summary
# ==========================================================
left_churn, right_recommendation = st.columns(2)

with left_churn:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("⚠️ Churn Summary")

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

    fig_churn = create_pie_chart(
        churn_counts,
        names="Status",
        values="Customers",
        title="Predicted Customer Churn",
        hole=0.45
    )

    st.plotly_chart(
        fig_churn,
        width="stretch",
        key="business_churn_summary"
    )
    st.markdown('</div>', unsafe_allow_html=True)

with right_recommendation:
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    section_header("🎯 Customer Segments")

    segment_summary = (
        recommendation_df["Segment"]
        .value_counts()
        .reset_index()
    )

    segment_summary.columns = [
        "Segment",
        "Customers",
    ]

    fig_segments = create_bar_chart(
        segment_summary,
        x="Segment",
        y="Customers",
        title="Customer Segments",
        text_auto=True
    )

    st.plotly_chart(
        fig_segments,
        width="stretch",
        key="business_segment_summary"
    )
    st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Inventory Status Summary
# ==========================================================
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("📦 Inventory Status")

inventory_status = (
    inventory_df["InventoryStatus"]
    .value_counts()
    .reset_index()
)

inventory_status.columns = [
    "InventoryStatus",
    "Products",
]

fig_inventory = create_bar_chart(
    inventory_status,
    x="InventoryStatus",
    y="Products",
    title="Inventory Status Distribution",
    text_auto=True
)

st.plotly_chart(
    fig_inventory,
    width="stretch",
    key="business_inventory_summary"
)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Notebook Business Recommendations
# ==========================================================
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("💡 Notebook Generated Business Recommendations")

st.dataframe(
    business_df,
    width="stretch",
    hide_index=True,
)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Forecast Executive Summary
# ==========================================================
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("📈 Forecast Executive Summary")

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
    info_banner(
        f"""
### Forecast Overview

Total Actual Sales
**{format_currency(total_actual_sales)}**

Total Predicted Sales
**{format_currency(total_predicted_sales)}**

Average Forecast Error
**{format_number(average_error)}**
"""
    )

with forecast_right:
    best_rmse = (
        model_df["RMSE"].min()
    )

    best_mae = (
        model_df["MAE"].min()
    )

    info_banner(
        f"""
### Forecast Model

Best Model
**{best_model}**

Lowest RMSE
**{format_number(best_rmse)}**

Lowest MAE
**{format_number(best_mae)}**
"""
    )
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Cross Module Executive Summary
# ==========================================================
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("📊 Cross Module Summary")

summary_df = pd.DataFrame(
    {
        "Business Area": [
            "Forecasting",
            "Churn",
            "Inventory",
            "Recommendations",
        ],
        "Records": [
            format_number(len(forecast_df)),
            format_number(len(churn_df)),
            format_number(len(inventory_df)),
            format_number(len(recommendation_df)),
        ],
    }
)

st.dataframe(
    summary_df,
    width="stretch",
    hide_index=True,
)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Executive Downloads
# ==========================================================
st.markdown('<div class="rp-card rp-download-btn">', unsafe_allow_html=True)
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
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Executive Performance Scorecard
# ==========================================================
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("📈 Executive Performance Scorecard")

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
            f"{format_number(high_risk)} High Risk Customers",
            f"{format_number(inventory_products)} Products",
            f"{format_number(recommended_customers)} Customers",
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
    width="stretch",
    hide_index=True,
)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Business Health Indicators
# ==========================================================
section_header("📊 Business Health Indicators")

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

kpis_health = [
    {"title": "Forecast Accuracy", "value": format_percentage(forecast_accuracy), "icon": "🎯"},
    {"title": "Churn Rate", "value": format_percentage(churn_rate), "icon": "⚠️"},
    {"title": "Inventory Health", "value": format_percentage(inventory_health), "icon": "✅"},
    {"title": "Recommendation Coverage", "value": format_percentage(recommendation_coverage), "icon": "👥"},
]
render_kpi_row(kpis_health)

dashboard_divider()

# ==========================================================
# Executive Risk Dashboard
# ==========================================================
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("🚨 Executive Risk Dashboard")

risk_left, risk_right = st.columns(2)

with risk_left:
    warning_banner(
        f"""
### Business Risks

• High Risk Customers
**{format_number(high_risk)}**

• Forecast Days
**{format_number(forecast_days)}**

• Inventory Products
**{format_number(inventory_products)}**
"""
    )

with risk_right:
    success_banner(
        f"""
### Business Strengths

• Best Forecast Model
**{best_model}**

• Recommendation Records
**{format_number(recommended_customers)}**

• Business Recommendations
**{format_number(business_rules)}**
"""
    )
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Management Summary
# ==========================================================
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("📋 Management Summary")

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
    width="stretch",
    hide_index=True,
)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Executive Action Plan
# ==========================================================
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("🎯 Executive Action Plan")

action_plan = [
    "Continue using the best-performing forecasting model for demand planning.",
    "Prioritize retention campaigns for high-risk customers identified by the churn model.",
    "Follow notebook-generated inventory recommendations to optimize stock levels.",
    "Use personalized product recommendations to improve cross-selling opportunities.",
    "Monitor business KPIs regularly through the RetailPulse dashboard.",
]

for i, action in enumerate(action_plan, start=1):
    st.write(f"{i}. {action}")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# CEO Executive Summary
# ==========================================================
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("📊 CEO Executive Summary")

info_banner(
    f"""
### RetailPulse Executive Report

Forecasting Model
**{best_model}**

Forecast Period
**{format_number(forecast_days)} Days**

Customers Analysed
**{format_number(customers)}**

Inventory Products
**{format_number(inventory_products)}**

Recommendation Records
**{format_number(recommended_customers)}**

Business Recommendations
**{format_number(business_rules)}**
"""
)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Overall Business Health
# ==========================================================
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("🚦 Overall Business Health")

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
    success_banner(f"Overall Business Health: Excellent ({health_score}/100)")
elif health_score >= 75:
    success_banner(f"Overall Business Health: Good ({health_score}/100)")
elif health_score >= 60:
    warning_banner(f"Overall Business Health: Moderate ({health_score}/100)")
else:
    st.error(f"Overall Business Health: Needs Attention ({health_score}/100)")

st.progress(health_score / 100)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Executive Notes
# ==========================================================
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("📝 Executive Notes")

st.markdown(
    """
- This dashboard is generated from notebook-produced reports.
- All analytics displayed are read-only visualizations.
- Forecasting, churn prediction, inventory optimization, and recommendation logic remain in the notebook pipeline.
- Streamlit serves as the presentation and decision-support layer.
"""
)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Footer
# ==========================================================
dashboard_footer()
