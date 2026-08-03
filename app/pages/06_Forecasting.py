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
    page_title="Forecasting Analytics",
    page_icon="📈",
    layout="wide",
)

load_css()

# ==========================================================
# Header
# ==========================================================

st.title("📈 Sales Forecasting")

st.caption(
    "RetailPulse • Demand Forecasting Dashboard"
)

st.markdown("---")

# ==========================================================
# Load Reports
# ==========================================================

@st.cache_data
def load_forecast_reports():

    forecast_df = pd.read_csv(
        "reports/forecast_results.csv"
    )

    model_df = pd.read_csv(
        "reports/forecasting_model_comparison.csv"
    )

    summary_df = pd.read_csv(
        "reports/forecasting_dataset_summary.csv"
    )

    forecast_df["Date"] = pd.to_datetime(
        forecast_df["Date"]
    )

    return (
        forecast_df,
        model_df,
        summary_df,
    )

forecast_df, model_df, summary_df = load_forecast_reports()

# ==========================================================
# Sidebar Filters
# ==========================================================

st.sidebar.header("📅 Forecast Filters")

start_date = forecast_df["Date"].min()

end_date = forecast_df["Date"].max()

selected_dates = st.sidebar.date_input(
    "Forecast Date Range",
    value=(
        start_date,
        end_date,
    ),
)

if len(selected_dates) == 2:

    forecast_df = forecast_df[
        (
            forecast_df["Date"]
            >= pd.Timestamp(selected_dates[0])
        )
        &
        (
            forecast_df["Date"]
            <= pd.Timestamp(selected_dates[1])
        )
    ]

# ==========================================================
# KPI Calculations
# ==========================================================

best_model = (
    model_df
    .sort_values("RMSE")
    .iloc[0]
)

forecast_days = len(forecast_df)

average_actual = (
    forecast_df["ActualSales"]
    .mean()
)

average_predicted = (
    forecast_df["PredictedSales"]
    .mean()
)

lowest_mae = (
    model_df["MAE"].min()
)

lowest_rmse = (
    model_df["RMSE"].min()
)

# ==========================================================
# KPI Cards
# ==========================================================

st.subheader("📊 Forecast Overview")

k1, k2, k3 = st.columns(3)

k1.metric(
    "Best Model",
    best_model["Model"],
)

k2.metric(
    "Lowest MAE",
    f"{lowest_mae:.2f}",
)

k3.metric(
    "Lowest RMSE",
    f"{lowest_rmse:.2f}",
)

k4, k5, k6 = st.columns(3)

k4.metric(
    "Forecast Days",
    forecast_days,
)

k5.metric(
    "Avg Actual Sales",
    f"{average_actual:,.2f}",
)

k6.metric(
    "Avg Predicted Sales",
    f"{average_predicted:,.2f}",
)

st.markdown("---")

# ==========================================================
# Actual vs Predicted Sales
# ==========================================================

st.subheader("📈 Actual vs Predicted Sales")

fig_actual_vs_predicted = px.line(
    forecast_df,
    x="Date",
    y=["ActualSales", "PredictedSales"],
    markers=True,
    title="Actual vs Predicted Sales"
)

fig_actual_vs_predicted.update_layout(
    template="plotly_white",
    height=550,
    title_x=0.5,
    xaxis_title="Date",
    yaxis_title="Sales",
    legend_title="Series"
)

st.plotly_chart(
    fig_actual_vs_predicted,
    use_container_width=True,
    key="actual_vs_predicted_chart"
)

st.markdown("---")

# ==========================================================
# Forecast Error Analysis
# ==========================================================

forecast_df["ForecastError"] = (
    forecast_df["PredictedSales"]
    - forecast_df["ActualSales"]
)

left_chart, right_chart = st.columns(2)

with left_chart:

    st.subheader("📉 Forecast Error Trend")

    fig_error = px.line(
        forecast_df,
        x="Date",
        y="ForecastError",
        markers=True,
        title="Prediction Error"
    )

    fig_error.add_hline(
        y=0,
        line_dash="dash",
        line_color="red"
    )

    fig_error.update_layout(
        template="plotly_white",
        height=450,
        title_x=0.5
    )

    st.plotly_chart(
        fig_error,
        use_container_width=True,
        key="forecast_error_chart"
    )

with right_chart:

    st.subheader("📊 Forecast Error Distribution")

    fig_error_distribution = px.histogram(
        forecast_df,
        x="ForecastError",
        nbins=25,
        title="Forecast Error Distribution"
    )

    fig_error_distribution.update_layout(
        template="plotly_white",
        height=450,
        title_x=0.5
    )

    st.plotly_chart(
        fig_error_distribution,
        use_container_width=True,
        key="forecast_error_distribution"
    )

st.markdown("---")

# ==========================================================
# Monthly Forecast Summary
# ==========================================================

monthly_forecast = (
    forecast_df
    .copy()
)

monthly_forecast["Month"] = (
    monthly_forecast["Date"]
    .dt.to_period("M")
    .astype(str)
)

monthly_summary = (
    monthly_forecast
    .groupby("Month", as_index=False)
    .agg(
        ActualSales=("ActualSales", "sum"),
        PredictedSales=("PredictedSales", "sum"),
    )
)

st.subheader("📅 Monthly Forecast Summary")

fig_monthly_forecast = px.bar(
    monthly_summary,
    x="Month",
    y=["ActualSales", "PredictedSales"],
    barmode="group",
    title="Monthly Actual vs Predicted Sales"
)

fig_monthly_forecast.update_layout(
    template="plotly_white",
    height=500,
    title_x=0.5,
    xaxis_title="Month",
    yaxis_title="Sales"
)

st.plotly_chart(
    fig_monthly_forecast,
    use_container_width=True,
    key="monthly_forecast_summary"
)

st.markdown("---")

# ==========================================================
# Model Performance Dashboard
# ==========================================================

st.subheader("🏆 Forecast Model Performance")

best_model_row = (
    model_df
    .sort_values("RMSE")
    .iloc[0]
)

best_model_name = best_model_row["Model"]

st.success(
    f"""
### Best Forecasting Model

**{best_model_name}**

Lowest RMSE : **{best_model_row['RMSE']:.2f}**

Lowest MAE : **{best_model_row['MAE']:.2f}**
"""
)

st.markdown("---")

# ==========================================================
# MAE & RMSE Comparison
# ==========================================================

left_model, right_model = st.columns(2)

with left_model:

    st.subheader("📊 MAE Comparison")

    fig_mae = px.bar(
        model_df,
        x="Model",
        y="MAE",
        color="MAE",
        text_auto=".2f",
        title="Model MAE Comparison"
    )

    fig_mae.update_layout(
        template="plotly_white",
        height=450,
        title_x=0.5,
        xaxis_title="Model",
        yaxis_title="MAE"
    )

    st.plotly_chart(
        fig_mae,
        use_container_width=True,
        key="forecast_mae_chart"
    )

with right_model:

    st.subheader("📈 RMSE Comparison")

    fig_rmse = px.bar(
        model_df,
        x="Model",
        y="RMSE",
        color="RMSE",
        text_auto=".2f",
        title="Model RMSE Comparison"
    )

    fig_rmse.update_layout(
        template="plotly_white",
        height=450,
        title_x=0.5,
        xaxis_title="Model",
        yaxis_title="RMSE"
    )

    st.plotly_chart(
        fig_rmse,
        use_container_width=True,
        key="forecast_rmse_chart"
    )

st.markdown("---")

# ==========================================================
# MAE vs RMSE Analysis
# ==========================================================

st.subheader("📉 MAE vs RMSE Analysis")

fig_model_scatter = px.scatter(
    model_df,
    x="MAE",
    y="RMSE",
    color="Model",
    size="RMSE",
    hover_name="Model",
    text="Model",
    title="Forecast Model Comparison"
)

fig_model_scatter.update_traces(
    textposition="top center"
)

fig_model_scatter.update_layout(
    template="plotly_white",
    height=550,
    title_x=0.5,
)

st.plotly_chart(
    fig_model_scatter,
    use_container_width=True,
    key="forecast_model_scatter"
)

st.markdown("---")

# ==========================================================
# Model Performance Table
# ==========================================================

st.subheader("📋 Model Comparison")

model_table = (
    model_df
    .sort_values("RMSE")
    .reset_index(drop=True)
)

st.dataframe(
    model_table,
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")

# ==========================================================
# Forecast Results Table
# ==========================================================

st.subheader("📋 Forecast Results")

forecast_display = (
    forecast_df
    .sort_values("Date")
    .copy()
)

forecast_display["ForecastError"] = (
    forecast_display["PredictedSales"]
    - forecast_display["ActualSales"]
)

st.dataframe(
    forecast_display,
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")

# ==========================================================
# Forecast Dataset Summary
# ==========================================================

st.subheader("📊 Forecast Dataset Summary")

st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")

# ==========================================================
# Download Reports
# ==========================================================

left_download, right_download = st.columns(2)

with left_download:

    forecast_csv = (
        forecast_display
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        label="📥 Download Forecast Results",
        data=forecast_csv,
        file_name="forecast_results.csv",
        mime="text/csv",
    )

with right_download:

    model_csv = (
        model_table
        .to_csv(index=False)
        .encode("utf-8")
    )

    st.download_button(
        label="📥 Download Model Comparison",
        data=model_csv,
        file_name="forecasting_model_comparison.csv",
        mime="text/csv",
    )

st.markdown("---")

# ==========================================================
# Forecast Business Insights
# ==========================================================

forecast_display["AbsoluteError"] = (
    forecast_display["ForecastError"]
    .abs()
)

largest_gap = (
    forecast_display
    .sort_values(
        "AbsoluteError",
        ascending=False
    )
    .iloc[0]
)

average_error = (
    forecast_display["AbsoluteError"]
    .mean()
)

maximum_actual = (
    forecast_display["ActualSales"]
    .max()
)

maximum_prediction = (
    forecast_display["PredictedSales"]
    .max()
)

left_info, right_info = st.columns(2)

with left_info:

    st.success(
        f"""
### 📈 Forecast Insights

Best Model

**{best_model_name}**

Average Forecast Error

**{average_error:.2f}**

Maximum Actual Sales

**{maximum_actual:,.2f}**

Maximum Predicted Sales

**{maximum_prediction:,.2f}**
"""
    )

with right_info:

    st.success(
        f"""
### 📊 Prediction Insights

Largest Prediction Gap

**{largest_gap['Date'].strftime('%Y-%m-%d')}**

Actual Sales

**{largest_gap['ActualSales']:,.2f}**

Predicted Sales

**{largest_gap['PredictedSales']:,.2f}**

Absolute Error

**{largest_gap['AbsoluteError']:,.2f}**
"""
    )

st.markdown("---")

# ==========================================================
# Executive Forecast Summary
# ==========================================================

st.subheader("📊 Executive Forecast Summary")

total_actual_sales = (
    forecast_df["ActualSales"]
    .sum()
)

total_predicted_sales = (
    forecast_df["PredictedSales"]
    .sum()
)

overall_forecast_error = (
    forecast_display["AbsoluteError"]
    .mean()
)

forecast_accuracy = (
    100
    - (
        overall_forecast_error
        / forecast_df["ActualSales"].mean()
        * 100
    )
)

forecast_accuracy = max(
    0,
    min(
        forecast_accuracy,
        100,
    ),
)

summary_left, summary_right = st.columns(2)

with summary_left:

    st.info(
        f"""
### 📈 Forecast Overview

Forecast Period

**{forecast_days} Days**

Total Actual Sales

**{total_actual_sales:,.2f}**

Total Predicted Sales

**{total_predicted_sales:,.2f}**
"""
    )

with summary_right:

    st.info(
        f"""
### 🎯 Model Performance

Selected Model

**{best_model_name}**

Estimated Forecast Accuracy

**{forecast_accuracy:.2f}%**

Average Absolute Error

**{overall_forecast_error:.2f}**
"""
    )

st.markdown("---")

# ==========================================================
# Forecast Recommendations
# ==========================================================

st.subheader("💡 Business Recommendations")

recommendations = []

if forecast_accuracy >= 95:
    recommendations.append(
        "Excellent forecasting performance. Continue using the current forecasting pipeline."
    )

elif forecast_accuracy >= 90:
    recommendations.append(
        "Forecast accuracy is very good. Continue monitoring weekly."
    )

elif forecast_accuracy >= 80:
    recommendations.append(
        "Forecast accuracy is acceptable. Review unusual sales periods for improvement."
    )

else:
    recommendations.append(
        "Forecast accuracy is relatively low. Review feature engineering and model assumptions in the notebook before future retraining."
    )

if largest_gap["AbsoluteError"] > overall_forecast_error * 2:
    recommendations.append(
        "Investigate the period with the largest prediction error for unusual business events."
    )

recommendations.append(
    "Use forecast outputs for inventory planning and demand estimation only."
)

recommendations.append(
    "Retraining should only be performed through the notebook workflow, not from the Streamlit application."
)

for index, recommendation in enumerate(recommendations, start=1):
    st.write(f"{index}. {recommendation}")

st.markdown("---")

# ==========================================================
# Forecast Health Status
# ==========================================================

st.subheader("🚦 Forecast Health")

if forecast_accuracy >= 95:
    st.success("Forecast Health: Excellent")

elif forecast_accuracy >= 90:
    st.success("Forecast Health: Good")

elif forecast_accuracy >= 80:
    st.warning("Forecast Health: Acceptable")

else:
    st.error("Forecast Health: Needs Review")

st.markdown("---")

# ==========================================================
# Footer
# ==========================================================

st.caption(
    """
RetailPulse

Sales Forecasting Dashboard

Notebook Outputs : Read Only

Reports :
forecast_results.csv
forecasting_model_comparison.csv
forecasting_dataset_summary.csv

Version : 1.0
"""
)