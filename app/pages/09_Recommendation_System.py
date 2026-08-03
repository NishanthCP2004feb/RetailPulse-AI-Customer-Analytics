import streamlit as st
import pandas as pd

from utils.theme import (
    load_css, 
    page_header, 
    section_header, 
    dashboard_divider, 
    dashboard_footer, 
    render_kpi_row, 
    render_insight_card, 
    success_banner
)
from utils.data_loader import load_recommendations
from utils.helpers import format_number, format_percentage, safe_value
from utils.metrics import get_recommendation_kpis
from utils.chart_utils import (
    create_bar_chart, 
    create_horizontal_bar_chart, 
    create_pie_chart, 
    create_histogram, 
    apply_chart_layout
)

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Recommendation System",
    page_icon="🎯",
    layout="wide",
)

load_css()

# ==========================================================
# Header
# ==========================================================

page_header('🎯 Recommendation System', 'RetailPulse • Personalized Product Recommendations')

dashboard_divider()

# ==========================================================
# Load Recommendation Report
# ==========================================================

df = load_recommendations()

if df.empty:
    st.error("Recommendation report not found.")
    st.stop()

# ==========================================================
# Sidebar Filters
# ==========================================================

st.sidebar.header("🎯 Recommendation Filters")

segments = sorted(df["Segment"].dropna().unique())

selected_segments = st.sidebar.multiselect(
    "Customer Segment",
    segments,
    default=segments,
)

filtered_df = df[df["Segment"].isin(selected_segments)].copy()

if filtered_df.empty:
    st.warning("No recommendations found.")
    st.stop()

# ==========================================================
# KPI Calculations
# ==========================================================

filtered_df["RecommendationCount"] = (
    filtered_df["RecommendedProducts"]
    .fillna("")
    .str.split(",")
    .apply(len)
)

total_customers = len(filtered_df)
total_segments = filtered_df["Segment"].nunique()
average_products = filtered_df["RecommendationCount"].mean()

largest_segment = filtered_df["Segment"].value_counts().idxmax() if not filtered_df.empty else "-"
largest_segment_count = filtered_df["Segment"].value_counts().max() if not filtered_df.empty else 0

# ==========================================================
# KPI Cards
# ==========================================================

section_header("📊 Recommendation Overview")

kpis_row_1 = [
    {"title": "Customers", "value": format_number(total_customers), "icon": "👥", "color": "#2563EB"},
    {"title": "Segments", "value": format_number(total_segments), "icon": "🏷️", "color": "#0EA5E9"},
    {"title": "Avg Recommendations", "value": f"{average_products:.1f}", "icon": "📦", "color": "#22C55E"}
]
render_kpi_row(kpis_row_1)

kpis_row_2 = [
    {"title": "Largest Segment", "value": largest_segment, "icon": "👑", "color": "#F59E0B"},
    {"title": "Customers in Segment", "value": format_number(largest_segment_count), "icon": "📊", "color": "#8B5CF6"},
    {"title": "Recommendation Rows", "value": format_number(len(filtered_df)), "icon": "📝", "color": "#6366F1"}
]
render_kpi_row(kpis_row_2)

dashboard_divider()

# ==========================================================
# Customer Segment Distribution
# ==========================================================

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
left_chart, right_chart = st.columns(2)

with left_chart:
    section_header("👥 Customer Segment Distribution")
    
    segment_distribution = filtered_df["Segment"].value_counts().reset_index()
    segment_distribution.columns = ["Segment", "Customers"]
    
    fig_segment_distribution = create_pie_chart(
        segment_distribution,
        names="Segment",
        values="Customers",
        title="Customer Segments",
        hole=0.45
    )
    st.plotly_chart(fig_segment_distribution, use_container_width=True, key="recommendation_segment_distribution")

with right_chart:
    section_header("📊 Customers per Segment")
    
    fig_segment_bar = create_bar_chart(
        segment_distribution,
        x="Segment",
        y="Customers",
        color="Customers",
        title="Segment Size"
    )
    st.plotly_chart(fig_segment_bar, use_container_width=True, key="segment_bar_chart")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Most Recommended Products
# ==========================================================

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("📦 Most Frequently Recommended Products")

product_list = (
    filtered_df["RecommendedProducts"]
    .fillna("")
    .str.split(",")
    .explode()
    .str.strip()
)
top_products = product_list.value_counts().head(15).reset_index()
top_products.columns = ["Product", "Recommendations"]

fig_top_products = create_horizontal_bar_chart(
    top_products,
    x="Recommendations",
    y="Product",
    color="Recommendations",
    title="Top Recommended Products"
)
st.plotly_chart(fig_top_products, use_container_width=True, key="top_recommended_products")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Recommendation Explorer
# ==========================================================

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("🔍 Recommendation Explorer")

selected_segment = st.selectbox(
    "Choose Customer Segment",
    sorted(filtered_df["Segment"].unique()),
    key="explorer_segment_select"
)
segment_df = filtered_df[filtered_df["Segment"] == selected_segment]

st.dataframe(segment_df, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Customer Search
# ==========================================================

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("🔍 Customer Recommendation Search")

search_customer = st.text_input(
    "Search Customer ID",
    placeholder="Enter Customer ID...",
    key="customer_search_input"
)

display_df = filtered_df.copy()

if search_customer:
    display_df = display_df[
        display_df["CustomerID"]
        .astype(str)
        .str.contains(search_customer, case=False, na=False)
    ]
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Recommendation Coverage Analysis
# ==========================================================

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
left_analysis, right_analysis = st.columns(2)

with left_analysis:
    section_header("📈 Recommendation Coverage")
    
    fig_recommendation_count = create_histogram(
        display_df,
        x="RecommendationCount",
        nbins=15,
        title="Recommendations per Customer"
    )
    st.plotly_chart(fig_recommendation_count, use_container_width=True, key="recommendation_count_chart")

with right_analysis:
    section_header("📊 Segment Recommendation Coverage")
    
    segment_summary = (
        display_df
        .groupby("Segment", as_index=False)
        .agg(
            Customers=("CustomerID", "count"),
            AvgRecommendations=("RecommendationCount", "mean"),
        )
    )
    
    fig_segment_summary = create_bar_chart(
        segment_summary,
        x="Segment",
        y="AvgRecommendations",
        color="Customers",
        title="Average Recommendations by Segment"
    )
    st.plotly_chart(fig_segment_summary, use_container_width=True, key="segment_recommendation_summary")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Recommendation Table
# ==========================================================

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("📋 Customer Recommendations")

st.dataframe(
    display_df.sort_values("Segment"),
    use_container_width=True,
    hide_index=True,
)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Download Recommendation Report
# ==========================================================

st.markdown('<div class="rp-download-btn">', unsafe_allow_html=True)
recommendation_csv = (
    display_df
    .drop(columns=["RecommendationCount"], errors="ignore")
    .to_csv(index=False)
    .encode("utf-8")
)

st.download_button(
    label="📥 Download Recommendation Report",
    data=recommendation_csv,
    file_name="customer_product_recommendations.csv",
    mime="text/csv",
    key="download_btn_recommendations"
)
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Recommendation Insights
# ==========================================================

largest_segment_display = display_df["Segment"].value_counts().idxmax() if not display_df.empty else "-"
largest_segment_size = display_df["Segment"].value_counts().max() if not display_df.empty else 0
average_recommendations = display_df["RecommendationCount"].mean() if not display_df.empty else 0
most_recommended = top_products.iloc[0] if not top_products.empty else pd.Series({"Product": "-", "Recommendations": 0})

left_info, right_info = st.columns(2)

with left_info:
    render_insight_card(
        "🎯 Segment Insights",
        f"""
        **Largest Customer Segment:** {largest_segment_display}
        
        **Customers:** {format_number(largest_segment_size)}
        
        **Average Recommendations:** {average_recommendations:.2f}
        """
    )

with right_info:
    render_insight_card(
        "📦 Product Insights",
        f"""
        **Most Recommended Product:** {most_recommended['Product']}
        
        **Recommendation Count:** {format_number(most_recommended['Recommendations'])}
        
        **Active Segments:** {total_segments}
        """
    )

dashboard_divider()

# ==========================================================
# Executive Recommendation Summary
# ==========================================================

section_header("📊 Executive Recommendation Summary")

total_recommendations = display_df["RecommendationCount"].sum() if not display_df.empty else 0

summary_left, summary_right = st.columns(2)

with summary_left:
    st.info(
        f"""
        ### 👥 Customer Recommendation Overview
        * **Customers Analysed:** {format_number(total_customers)}
        * **Customer Segments:** {format_number(total_segments)}
        * **Total Recommendations:** {format_number(int(total_recommendations))}
        """
    )

with summary_right:
    st.info(
        f"""
        ### 🎯 Recommendation Performance
        * **Average Recommendations:** {average_recommendations:.2f}
        * **Largest Segment:** {largest_segment_display}
        * **Customers in Largest Segment:** {format_number(largest_segment_size)}
        """
    )

dashboard_divider()

# ==========================================================
# Business Recommendations
# ==========================================================

st.markdown('<div class="rp-card">', unsafe_allow_html=True)
section_header("💡 Business Recommendations")

with st.expander("View Business Recommendations", expanded=True):
    recommendations = []

    if average_recommendations >= 5:
        recommendations.append("Customers receive multiple product recommendations, enabling broader cross-selling opportunities.")
    elif average_recommendations >= 3:
        recommendations.append("Recommendation coverage is balanced and suitable for personalized marketing.")
    else:
        recommendations.append("Consider improving recommendation diversity during future notebook retraining.")

    recommendations.append(f"Focus promotional campaigns on the '{largest_segment_display}' customer segment because it contains the largest customer base.")
    recommendations.append(f"Use '{most_recommended['Product']}' as a featured recommendation in marketing campaigns.")
    recommendations.append("Recommendation logic should remain notebook-driven. The Streamlit dashboard should only visualize exported results.")

    for i, recommendation in enumerate(recommendations, start=1):
        st.write(f"{i}. {recommendation}")
st.markdown('</div>', unsafe_allow_html=True)

dashboard_divider()

# ==========================================================
# Recommendation System Health
# ==========================================================

section_header("🚦 Recommendation System Health")

if average_recommendations >= 5:
    success_banner("Recommendation Health: Excellent")
elif average_recommendations >= 3:
    success_banner("Recommendation Health: Good")
elif average_recommendations >= 2:
    st.warning("Recommendation Health: Moderate")
else:
    st.error("Recommendation Health: Needs Improvement")

dashboard_divider()

# ==========================================================
# Footer
# ==========================================================

dashboard_footer()
