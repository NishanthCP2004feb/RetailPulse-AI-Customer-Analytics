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
    page_title="Recommendation System",
    page_icon="🎯",
    layout="wide",
)

load_css()

# ==========================================================
# Header
# ==========================================================

st.title("🎯 Product Recommendation System")

st.caption(
    "RetailPulse • Personalized Product Recommendations"
)

st.markdown("---")

# ==========================================================
# Load Recommendation Report
# ==========================================================

@st.cache_data
def load_recommendations():

    return pd.read_csv(
        "reports/customer_product_recommendations.csv"
    )

df = load_recommendations()

if df.empty:
    st.error("Recommendation report not found.")
    st.stop()

# ==========================================================
# Sidebar Filters
# ==========================================================

st.sidebar.header("🎯 Recommendation Filters")

segments = sorted(
    df["Segment"].dropna().unique()
)

selected_segments = st.sidebar.multiselect(
    "Customer Segment",
    segments,
    default=segments,
)

filtered_df = df[
    df["Segment"].isin(selected_segments)
]

if filtered_df.empty:
    st.warning("No recommendations found.")
    st.stop()

# ==========================================================
# KPI Calculations
# ==========================================================

total_customers = len(filtered_df)

total_segments = (
    filtered_df["Segment"]
    .nunique()
)

average_products = (
    filtered_df["RecommendedProducts"]
    .fillna("")
    .str.split(",")
    .apply(len)
    .mean()
)

largest_segment = (
    filtered_df["Segment"]
    .value_counts()
    .idxmax()
)

largest_segment_count = (
    filtered_df["Segment"]
    .value_counts()
    .max()
)

# ==========================================================
# KPI Cards
# ==========================================================

st.subheader("📊 Recommendation Overview")

k1, k2, k3 = st.columns(3)

k1.metric(
    "Customers",
    f"{total_customers:,}"
)

k2.metric(
    "Segments",
    total_segments
)

k3.metric(
    "Avg Recommendations",
    f"{average_products:.1f}"
)

k4, k5, k6 = st.columns(3)

k4.metric(
    "Largest Segment",
    largest_segment
)

k5.metric(
    "Customers in Segment",
    f"{largest_segment_count:,}"
)

k6.metric(
    "Recommendation Rows",
    f"{len(filtered_df):,}"
)

st.markdown("---")

# ==========================================================
# Customer Segment Distribution
# ==========================================================

left_chart, right_chart = st.columns(2)

with left_chart:

    st.subheader("👥 Customer Segment Distribution")

    segment_distribution = (
        filtered_df["Segment"]
        .value_counts()
        .reset_index()
    )

    segment_distribution.columns = [
        "Segment",
        "Customers",
    ]

    fig_segment_distribution = px.pie(
        segment_distribution,
        names="Segment",
        values="Customers",
        hole=0.45,
        title="Customer Segments"
    )

    fig_segment_distribution.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
    )

    st.plotly_chart(
        fig_segment_distribution,
        use_container_width=True,
        key="recommendation_segment_distribution"
    )

# ==========================================================
# Recommendations by Segment
# ==========================================================

with right_chart:

    st.subheader("📊 Customers per Segment")

    fig_segment_bar = px.bar(
        segment_distribution,
        x="Segment",
        y="Customers",
        color="Customers",
        text_auto=True,
        title="Segment Size"
    )

    fig_segment_bar.update_layout(
        template="plotly_white",
        height=500,
        title_x=0.5,
        xaxis_title="Segment",
        yaxis_title="Customers"
    )

    st.plotly_chart(
        fig_segment_bar,
        use_container_width=True,
        key="segment_bar_chart"
    )

st.markdown("---")

# ==========================================================
# Most Recommended Products
# ==========================================================

st.subheader("📦 Most Frequently Recommended Products")

product_list = (
    filtered_df["RecommendedProducts"]
    .fillna("")
    .str.split(",")
    .explode()
    .str.strip()
)

top_products = (
    product_list
    .value_counts()
    .head(15)
    .reset_index()
)

top_products.columns = [
    "Product",
    "Recommendations",
]

fig_top_products = px.bar(
    top_products,
    x="Recommendations",
    y="Product",
    orientation="h",
    color="Recommendations",
    text_auto=True,
    title="Top Recommended Products"
)

fig_top_products.update_layout(
    template="plotly_white",
    height=600,
    title_x=0.5,
    yaxis_title="",
)

st.plotly_chart(
    fig_top_products,
    use_container_width=True,
    key="top_recommended_products"
)

st.markdown("---")

# ==========================================================
# Recommendation Explorer
# ==========================================================

st.subheader("🔍 Recommendation Explorer")

selected_segment = st.selectbox(
    "Choose Customer Segment",
    sorted(filtered_df["Segment"].unique())
)

segment_df = (
    filtered_df[
        filtered_df["Segment"] == selected_segment
    ]
)

st.dataframe(
    segment_df,
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")

# ==========================================================
# Customer Search
# ==========================================================

st.subheader("🔍 Customer Recommendation Search")

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
# Recommendation Coverage Analysis
# ==========================================================

left_analysis, right_analysis = st.columns(2)

with left_analysis:

    st.subheader("📈 Recommendation Coverage")

    display_df["RecommendationCount"] = (
        display_df["RecommendedProducts"]
        .fillna("")
        .str.split(",")
        .apply(len)
    )

    fig_recommendation_count = px.histogram(
        display_df,
        x="RecommendationCount",
        nbins=15,
        title="Recommendations per Customer"
    )

    fig_recommendation_count.update_layout(
        template="plotly_white",
        height=450,
        title_x=0.5,
        xaxis_title="Recommendations",
        yaxis_title="Customers"
    )

    st.plotly_chart(
        fig_recommendation_count,
        use_container_width=True,
        key="recommendation_count_chart"
    )

with right_analysis:

    st.subheader("📊 Segment Recommendation Coverage")

    segment_summary = (
        display_df
        .groupby("Segment", as_index=False)
        .agg(
            Customers=("CustomerID", "count"),
            AvgRecommendations=("RecommendationCount", "mean"),
        )
    )

    fig_segment_summary = px.bar(
        segment_summary,
        x="Segment",
        y="AvgRecommendations",
        color="Customers",
        text_auto=".1f",
        title="Average Recommendations by Segment"
    )

    fig_segment_summary.update_layout(
        template="plotly_white",
        height=450,
        title_x=0.5,
    )

    st.plotly_chart(
        fig_segment_summary,
        use_container_width=True,
        key="segment_recommendation_summary"
    )

st.markdown("---")

# ==========================================================
# Recommendation Table
# ==========================================================

st.subheader("📋 Customer Recommendations")

st.dataframe(
    display_df.sort_values(
        "Segment"
    ),
    use_container_width=True,
    hide_index=True,
)

st.markdown("---")

# ==========================================================
# Download Recommendation Report
# ==========================================================

recommendation_csv = (
    display_df
    .drop(columns=["RecommendationCount"])
    .to_csv(index=False)
    .encode("utf-8")
)

st.download_button(
    label="📥 Download Recommendation Report",
    data=recommendation_csv,
    file_name="customer_product_recommendations.csv",
    mime="text/csv",
)

st.markdown("---")

# ==========================================================
# Recommendation Insights
# ==========================================================

largest_segment = (
    display_df["Segment"]
    .value_counts()
    .idxmax()
)

largest_segment_size = (
    display_df["Segment"]
    .value_counts()
    .max()
)

average_recommendations = (
    display_df["RecommendationCount"]
    .mean()
)

most_recommended = (
    top_products.iloc[0]
)

left_info, right_info = st.columns(2)

with left_info:

    st.success(
        f"""
### 🎯 Segment Insights

Largest Customer Segment

**{largest_segment}**

Customers

**{largest_segment_size:,}**

Average Recommendations

**{average_recommendations:.2f}**
"""
    )

with right_info:

    st.success(
        f"""
### 📦 Product Insights

Most Recommended Product

**{most_recommended['Product']}**

Recommendation Count

**{most_recommended['Recommendations']}**

Active Segments

**{total_segments}**
"""
    )

st.markdown("---")

# ==========================================================
# Executive Recommendation Summary
# ==========================================================

st.subheader("📊 Executive Recommendation Summary")

total_recommendations = (
    display_df["RecommendationCount"]
    .sum()
)

summary_left, summary_right = st.columns(2)

with summary_left:

    st.info(
        f"""
### 👥 Customer Recommendation Overview

Customers Analysed

**{total_customers:,}**

Customer Segments

**{total_segments}**

Total Recommendations

**{int(total_recommendations):,}**
"""
    )

with summary_right:

    st.info(
        f"""
### 🎯 Recommendation Performance

Average Recommendations

**{average_recommendations:.2f}**

Largest Segment

**{largest_segment}**

Customers in Largest Segment

**{largest_segment_size:,}**
"""
    )

st.markdown("---")

# ==========================================================
# Business Recommendations
# ==========================================================

st.subheader("💡 Business Recommendations")

recommendations = []

if average_recommendations >= 5:
    recommendations.append(
        "Customers receive multiple product recommendations, enabling broader cross-selling opportunities."
    )
elif average_recommendations >= 3:
    recommendations.append(
        "Recommendation coverage is balanced and suitable for personalized marketing."
    )
else:
    recommendations.append(
        "Consider improving recommendation diversity during future notebook retraining."
    )

recommendations.append(
    f"Focus promotional campaigns on the '{largest_segment}' customer segment because it contains the largest customer base."
)

recommendations.append(
    f"Use '{most_recommended['Product']}' as a featured recommendation in marketing campaigns."
)

recommendations.append(
    "Recommendation logic should remain notebook-driven. The Streamlit dashboard should only visualize exported results."
)

for i, recommendation in enumerate(recommendations, start=1):
    st.write(f"{i}. {recommendation}")

st.markdown("---")

# ==========================================================
# Recommendation System Health
# ==========================================================

st.subheader("🚦 Recommendation System Health")

if average_recommendations >= 5:
    st.success("Recommendation Health: Excellent")

elif average_recommendations >= 3:
    st.success("Recommendation Health: Good")

elif average_recommendations >= 2:
    st.warning("Recommendation Health: Moderate")

else:
    st.error("Recommendation Health: Needs Improvement")

st.markdown("---")

# ==========================================================
# Footer
# ==========================================================

st.caption(
    """
RetailPulse

Recommendation System Dashboard

Notebook Outputs : Read Only

Report:
customer_product_recommendations.csv

Version : 1.0
"""
)
