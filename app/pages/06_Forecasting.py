import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================================
# Page Configuration
# ==========================================================
st.set_page_config(
    page_title="Forecasting Analytics",
    page_icon="📈",
    layout="wide",
)

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
    error_banner
)
from utils.data_loader import load_forecast_reports
from utils.helpers import format_currency, format_number, format_percentage

from utils.chart_utils import (
    create_bar_chart, 
    create_line_chart, 
    create_forecast_chart, 
    apply_chart_layout
)

load_css()

# ==========================================================
# Header
# ==========================================================
page_header('📈 Demand Forecasting', 'RetailPulse • AI-Powered Sales Forecasting')
dashboard_divider()

# ==========================================================
# Load Reports
# ==========================================================
forecast_df, model_df, summary_df = load_forecast_reports()

# ==========================================================
# Sidebar Filters
# ==========================================================
st.sidebar.header("📅 Forecast Filters")
start_date = forecast_df["Date"].min()
end_date = forecast_df["Date"].max()

selected_dates = st.sidebar.date_input(
    "Forecast Date Range",
    value=(start_date, end_date),
    key="forecast_date_range"
)

if len(selected_dates) == 2:
    forecast_df = forecast_df[
        (forecast_df["Date"] >= pd.Timestamp(selected_dates[0])) &
        (forecast_df["Date"] <= pd.Timestamp(selected_dates[1]))
    ]

# ==========================================================
# KPI Calculations
# ==========================================================
best_model_row = model_df.sort_values("RMSE").iloc[0]
best_model_name = best_model_row["Model"]
lowest_mae = model_df["MAE"].min()
lowest_rmse = model_df["RMSE"].min()

forecast_days = len(forecast_df)
average_actual = forecast_df["ActualSales"].mean()
average_predicted = forecast_df["PredictedSales"].mean()

# ==========================================================
# KPI Cards
# ==========================================================
section_header("📊 Forecast Overview")

kpi_data_1 = [
    {"title": "Best Model", "value": best_model_name, "icon": "🤖"},
    {"title": "Lowest MAE", "value": format_number(lowest_mae), "icon": "📉"},
    {"title": "Lowest RMSE", "value": format_number(lowest_rmse), "icon": "🎯"},
]
render_kpi_row(kpi_data_1)

kpi_data_2 = [
    {"title": "Forecast Days", "value": str(forecast_days), "icon": "📅"},
    {"title": "Avg Actual Sales", "value": format_currency(average_actual), "icon": "💰"},
    {"title": "Avg Predicted Sales", "value": format_currency(average_predicted), "icon": "🔮"},
]
render_kpi_row(kpi_data_2)

dashboard_divider()

# ==========================================================
# Actual vs Predicted Sales
# ==========================================================
section_header("📈 Actual vs Predicted Sales")
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
fig_actual_vs_predicted = create_forecast_chart(
    forecast_df, 
    date_column="Date", 
    actual_column="ActualSales", 
    forecast_column="PredictedSales"
)
st.plotly_chart(fig_actual_vs_predicted, use_container_width=True, key="actual_vs_predicted_chart")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Forecast Error Analysis
# ==========================================================
forecast_df["ForecastError"] = forecast_df["PredictedSales"] - forecast_df["ActualSales"]

left_chart, right_chart = st.columns(2)
with left_chart:
    section_header("📉 Forecast Error Trend")
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    fig_error = create_line_chart(
        forecast_df,
        x="Date",
        y="ForecastError",
        title="Prediction Error"
    )
    fig_error.add_hline(y=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig_error, use_container_width=True, key="forecast_error_chart")
    st.markdown('</div>', unsafe_allow_html=True)

with right_chart:
    section_header("📊 Forecast Error Distribution")
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    fig_error_distribution = px.histogram(
        forecast_df,
        x="ForecastError",
        nbins=25,
        title="Forecast Error Distribution"
    )
    fig_error_distribution = apply_chart_layout(fig_error_distribution)
    st.plotly_chart(fig_error_distribution, use_container_width=True, key="forecast_error_distribution")
    st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Monthly Forecast Summary
# ==========================================================
monthly_forecast = forecast_df.copy()
monthly_forecast["Month"] = monthly_forecast["Date"].dt.to_period("M").astype(str)
monthly_summary = monthly_forecast.groupby("Month", as_index=False).agg(
    ActualSales=("ActualSales", "sum"),
    PredictedSales=("PredictedSales", "sum"),
)

section_header("📅 Monthly Forecast Summary")
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
fig_monthly_forecast = px.bar(
    monthly_summary,
    x="Month",
    y=["ActualSales", "PredictedSales"],
    barmode="group",
    title="Monthly Actual vs Predicted Sales"
)
fig_monthly_forecast = apply_chart_layout(fig_monthly_forecast)
st.plotly_chart(fig_monthly_forecast, use_container_width=True, key="monthly_forecast_summary")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Model Performance Dashboard
# ==========================================================
section_header("🏆 Forecast Model Performance")

render_insight_card(
    "Best Forecasting Model",
    f"""
    **{best_model_name}**
    
    Lowest RMSE : **{format_number(best_model_row['RMSE'])}**
    
    Lowest MAE : **{format_number(best_model_row['MAE'])}**
    """
)

dashboard_divider()

# ==========================================================
# MAE & RMSE Comparison
# ==========================================================
left_model, right_model = st.columns(2)

with left_model:
    section_header("📊 MAE Comparison")
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    fig_mae = create_bar_chart(
        model_df,
        x="Model",
        y="MAE",
        color="MAE",
        title="Model MAE Comparison"
    )
    st.plotly_chart(fig_mae, use_container_width=True, key="forecast_mae_chart")
    st.markdown('</div>', unsafe_allow_html=True)

with right_model:
    section_header("📈 RMSE Comparison")
    st.markdown('<div class="rp-card">', unsafe_allow_html=True)
    fig_rmse = create_bar_chart(
        model_df,
        x="Model",
        y="RMSE",
        color="RMSE",
        title="Model RMSE Comparison"
    )
    st.plotly_chart(fig_rmse, use_container_width=True, key="forecast_rmse_chart")
    st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# MAE vs RMSE Analysis
# ==========================================================
section_header("📉 MAE vs RMSE Analysis")
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
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
fig_model_scatter.update_traces(textposition="top center")
fig_model_scatter = apply_chart_layout(fig_model_scatter, height=550)
st.plotly_chart(fig_model_scatter, use_container_width=True, key="forecast_model_scatter")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Model Performance Table
# ==========================================================
section_header("📋 Model Comparison")
model_table = model_df.sort_values("RMSE").reset_index(drop=True)
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
st.dataframe(model_table, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Forecast Results Table
# ==========================================================
section_header("📋 Forecast Results")
forecast_display = forecast_df.sort_values("Date").copy()
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
st.dataframe(forecast_display, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Forecast Dataset Summary
# ==========================================================
section_header("📊 Forecast Dataset Summary")
st.markdown('<div class="rp-card">', unsafe_allow_html=True)
st.dataframe(summary_df, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Download Reports
# ==========================================================
st.markdown('<div class="rp-download-btn">', unsafe_allow_html=True)
left_download, right_download = st.columns(2)

with left_download:
    forecast_csv = forecast_display.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Forecast Results",
        data=forecast_csv,
        file_name="forecast_results.csv",
        mime="text/csv",
        key="download_forecast_results"
    )

with right_download:
    model_csv = model_table.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Model Comparison",
        data=model_csv,
        file_name="forecasting_model_comparison.csv",
        mime="text/csv",
        key="download_model_comparison"
    )
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Forecast Business Insights
# ==========================================================
forecast_display["AbsoluteError"] = forecast_display["ForecastError"].abs()
largest_gap = forecast_display.sort_values("AbsoluteError", ascending=False).iloc[0]
average_error = forecast_display["AbsoluteError"].mean()
maximum_actual = forecast_display["ActualSales"].max()
maximum_prediction = forecast_display["PredictedSales"].max()

left_info, right_info = st.columns(2)

with left_info:
    render_insight_card(
        "📈 Forecast Insights",
        f"""
        Best Model: **{best_model_name}**
        
        Average Forecast Error: **{format_number(average_error)}**
        
        Maximum Actual Sales: **{format_currency(maximum_actual)}**
        
        Maximum Predicted Sales: **{format_currency(maximum_prediction)}**
        """
    )

with right_info:
    render_insight_card(
        "📊 Prediction Insights",
        f"""
        Largest Prediction Gap: **{largest_gap['Date'].strftime('%Y-%m-%d')}**
        
        Actual Sales: **{format_currency(largest_gap['ActualSales'])}**
        
        Predicted Sales: **{format_currency(largest_gap['PredictedSales'])}**
        
        Absolute Error: **{format_number(largest_gap['AbsoluteError'])}**
        """
    )

dashboard_divider()

# ==========================================================
# Executive Forecast Summary
# ==========================================================
section_header("📊 Executive Forecast Summary")

total_actual_sales = forecast_df["ActualSales"].sum()
total_predicted_sales = forecast_df["PredictedSales"].sum()
overall_forecast_error = forecast_display["AbsoluteError"].mean()
forecast_accuracy = 100 - (overall_forecast_error / forecast_df["ActualSales"].mean() * 100)
forecast_accuracy = max(0, min(forecast_accuracy, 100))

summary_left, summary_right = st.columns(2)

with summary_left:
    render_insight_card(
        "📈 Forecast Overview",
        f"""
        Forecast Period: **{forecast_days} Days**
        
        Total Actual Sales: **{format_currency(total_actual_sales)}**
        
        Total Predicted Sales: **{format_currency(total_predicted_sales)}**
        """
    )

with summary_right:
    render_insight_card(
        "🎯 Model Performance",
        f"""
        Selected Model: **{best_model_name}**
        
        Estimated Forecast Accuracy: **{format_percentage(forecast_accuracy, 2)}**
        
        Average Absolute Error: **{format_number(overall_forecast_error)}**
        """
    )

dashboard_divider()

# ==========================================================
# Forecast Recommendations
# ==========================================================
section_header("💡 Business Recommendations")

with st.expander("View Detailed Recommendations", expanded=True):
    recommendations = []
    if forecast_accuracy >= 95:
        recommendations.append("Excellent forecasting performance. Continue using the current forecasting pipeline.")
    elif forecast_accuracy >= 90:
        recommendations.append("Forecast accuracy is very good. Continue monitoring weekly.")
    elif forecast_accuracy >= 80:
        recommendations.append("Forecast accuracy is acceptable. Review unusual sales periods for improvement.")
    else:
        recommendations.append("Forecast accuracy is relatively low. Review feature engineering and model assumptions in the notebook before future retraining.")

    if largest_gap["AbsoluteError"] > overall_forecast_error * 2:
        recommendations.append("Investigate the period with the largest prediction error for unusual business events.")

    recommendations.append("Use forecast outputs for inventory planning and demand estimation only.")
    recommendations.append("Retraining should only be performed through the notebook workflow, not from the Streamlit application.")

    for index, recommendation in enumerate(recommendations, start=1):
        st.write(f"{index}. {recommendation}")

dashboard_divider()

# ==========================================================
# Forecast Health Status
# ==========================================================
section_header("🚦 Forecast Health")

if forecast_accuracy >= 95:
    success_banner("Forecast Health: Excellent")
elif forecast_accuracy >= 90:
    success_banner("Forecast Health: Good")
elif forecast_accuracy >= 80:
    warning_banner("Forecast Health: Acceptable")
else:
    error_banner("Forecast Health: Needs Review")

dashboard_divider()

# ==========================================================
# Footer
# ==========================================================
dashboard_footer()