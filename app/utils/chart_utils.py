"""
RetailPulse Chart Utilities
===========================

Reusable Plotly chart functions for the
RetailPulse Streamlit Dashboard.

This module centralizes all chart creation
and styling to ensure a consistent UI across
all dashboard pages.

Author: RetailPulse
"""

from __future__ import annotations

from typing import Optional

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================================
# Default Theme
# ==========================================================

DEFAULT_TEMPLATE = "plotly_white"

DEFAULT_HEIGHT = 460

DEFAULT_COLOR_SEQUENCE = px.colors.qualitative.Set2


# ==========================================================
# Common Layout
# ==========================================================

def apply_chart_layout(
    fig: go.Figure,
    title: Optional[str] = None,
    height: int = DEFAULT_HEIGHT,
) -> go.Figure:
    """
    Apply the common RetailPulse layout to a Plotly chart.
    """

    if title:
        fig.update_layout(title=title)

    fig.update_layout(

        template=DEFAULT_TEMPLATE,

        height=height,

        title_x=0.5,

        font=dict(family="Inter, Arial, sans-serif", size=13, color="#1F2937"),

        legend_title_text="",

        hovermode="x unified",

        margin=dict(l=24, r=24, t=56, b=36),

        colorway=DEFAULT_COLOR_SEQUENCE,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="#FFFFFF",
        hoverlabel=dict(bgcolor="#0F172A", font_color="#FFFFFF"),

    )

    return fig


# ==========================================================
# Generic Bar Chart
# ==========================================================

def create_bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: Optional[str] = None,
    text_auto=True,
):

    fig = px.bar(

        data,

        x=x,

        y=y,

        color=color if color else y,

        text_auto=text_auto,

        title=title,

    )

    return apply_chart_layout(fig, title)


# ==========================================================
# Horizontal Bar Chart
# ==========================================================

def create_horizontal_bar_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: Optional[str] = None,
    text_auto=".2s",
):

    fig = px.bar(

        data,

        x=x,

        y=y,

        orientation="h",

        color=color if color else x,

        text_auto=text_auto,

        title=title,

    )

    fig.update_layout(
        yaxis_title=""
    )

    return apply_chart_layout(fig, title)


# ==========================================================
# Generic Line Chart
# ==========================================================

def create_line_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    markers: bool = True,
):

    fig = px.line(

        data,

        x=x,

        y=y,

        markers=markers,

        title=title,

    )

    return apply_chart_layout(fig, title)


# ==========================================================
# Generic Pie Chart
# ==========================================================

def create_pie_chart(
    data: pd.DataFrame,
    names: str,
    values: str,
    title: str = "",
    hole: float = 0.45,
):

    fig = px.pie(

        data,

        names=names,

        values=values,

        hole=hole,

        title=title,

    )

    return apply_chart_layout(fig, title)

# ==========================================================
# Generic Scatter Chart
# ==========================================================

def create_scatter_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: Optional[str] = None,
    size: Optional[str] = None,
    hover_name: Optional[str] = None,
):

    fig = px.scatter(
        data,
        x=x,
        y=y,
        color=color,
        size=size,
        hover_name=hover_name,
        title=title,
        render_mode="svg",
    )

    return apply_chart_layout(fig, title)


# ==========================================================
# Generic Histogram
# ==========================================================

def create_histogram(
    data: pd.DataFrame,
    x: str,
    title: str = "",
    nbins: int = 30,
):

    fig = px.histogram(
        data,
        x=x,
        nbins=nbins,
        title=title,
    )

    return apply_chart_layout(fig, title)


# ==========================================================
# Generic Heatmap
# ==========================================================

def create_heatmap(
    data,
    title: str = "Heatmap",
):

    fig = px.imshow(
        data,
        aspect="auto",
        text_auto=".1f",
        title=title,
    )

    return apply_chart_layout(
        fig,
        title,
        height=650,
    )


# ==========================================================
# Generic Area Chart
# ==========================================================

def create_area_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
):

    fig = px.area(
        data,
        x=x,
        y=y,
        title=title,
    )

    return apply_chart_layout(fig, title)


# ==========================================================
# Generic Box Plot
# ==========================================================

def create_box_plot(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str = "",
    color: Optional[str] = None,
):

    fig = px.box(
        data,
        x=x,
        y=y,
        color=color,
        title=title,
    )

    return apply_chart_layout(fig, title)


# ==========================================================
# Monthly Sales Chart
# ==========================================================

def create_monthly_sales_chart(
    df: pd.DataFrame,
):

    monthly_sales = (
        df.groupby(
            "InvoiceMonthYear",
            as_index=False,
        )["TotalAmount"]
        .sum()
        .sort_values("InvoiceMonthYear")
    )

    fig = px.bar(
        monthly_sales,
        x="InvoiceMonthYear",
        y="TotalAmount",
        text_auto=".2s",
        title="Monthly Sales Revenue",
        labels={
            "InvoiceMonthYear": "Month",
            "TotalAmount": "Revenue (£)",
        },
    )

    return apply_chart_layout(
        fig,
        "Monthly Sales Revenue",
        450,
    )


# ==========================================================
# Top Products Chart
# ==========================================================

def create_top_products_chart(
    df: pd.DataFrame,
    top_n: int = 10,
):

    products = (
        df.groupby(
            "ProductDescription",
            as_index=False,
        )["TotalAmount"]
        .sum()
        .nlargest(
            top_n,
            "TotalAmount",
        )
    )

    fig = px.bar(
        products,
        x="TotalAmount",
        y="ProductDescription",
        orientation="h",
        text_auto=".2s",
        title=f"Top {top_n} Products by Revenue",
    )

    fig.update_layout(
        yaxis_title=""
    )

    return apply_chart_layout(fig, height=500)

# ==========================================================
# Country Sales Chart
# ==========================================================

def create_country_sales_chart(
    df: pd.DataFrame,
    top_n: int = 10,
):

    country_sales = (
        df.groupby(
            "Country",
            as_index=False,
        )["TotalAmount"]
        .sum()
        .sort_values(
            "TotalAmount",
            ascending=False,
        )
        .head(top_n)
    )

    return create_horizontal_bar_chart(
        country_sales,
        x="TotalAmount",
        y="Country",
        title=f"Top {top_n} Countries by Revenue",
    )


# ==========================================================
# Customer Segment Chart
# ==========================================================

def create_customer_segment_chart(
    df: pd.DataFrame,
    segment_column: str = "Segment",
):

    if segment_column not in df.columns:
        raise ValueError(
            f"'{segment_column}' column not found."
        )

    segment_data = (
        df.groupby(
            segment_column,
            as_index=False,
        )
        .size()
        .rename(
            columns={"size": "Customers"}
        )
    )

    return create_pie_chart(
        segment_data,
        names=segment_column,
        values="Customers",
        title="Customer Segments",
    )


# ==========================================================
# Forecast Chart
# ==========================================================

def create_forecast_chart(
    df: pd.DataFrame,
    date_column: str = "Date",
    actual_column: str = "Actual",
    forecast_column: str = "Forecast",
):

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df[date_column],
            y=df[actual_column],
            mode="lines",
            name="Actual",
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df[date_column],
            y=df[forecast_column],
            mode="lines",
            name="Forecast",
        )
    )

    return apply_chart_layout(
        fig,
        "Actual vs Forecast",
    )


# ==========================================================
# Inventory Status Chart
# ==========================================================

def create_inventory_chart(
    df: pd.DataFrame,
    category_col: str,
    value_col: str,
):

    return create_bar_chart(
        df,
        x=category_col,
        y=value_col,
        title="Inventory Status",
    )


# ==========================================================
# KPI Trend Chart
# ==========================================================

def create_kpi_trend_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
):

    fig = px.line(
        df,
        x=x,
        y=y,
        markers=True,
        title=title,
    )

    fig.update_traces(
        line=dict(width=3)
    )

    return apply_chart_layout(fig, title)


# ==========================================================
# Donut Chart
# ==========================================================

def create_donut_chart(
    data: pd.DataFrame,
    names: str,
    values: str,
    title: str,
):

    return create_pie_chart(
        data=data,
        names=names,
        values=values,
        title=title,
        hole=0.65,
    )


# ==========================================================
# Generic Time Series Chart
# ==========================================================

def create_time_series_chart(
    data: pd.DataFrame,
    x: str,
    y: str,
    title: str,
):

    fig = px.line(
        data,
        x=x,
        y=y,
        markers=True,
        title=title,
    )

    fig.update_traces(
        line=dict(width=3)
    )

    return apply_chart_layout(fig, title)


# ==========================================================
# Empty Figure
# ==========================================================

def create_empty_chart(
    message: str = "No data available",
):

    fig = go.Figure()

    fig.add_annotation(
        text=message,
        x=0.5,
        y=0.5,
        showarrow=False,
        font=dict(size=18),
        xref="paper",
        yref="paper",
    )

    fig.update_xaxes(visible=False)
    fig.update_yaxes(visible=False)

    return apply_chart_layout(
        fig,
        "Information",
        height=350,
    )


# ==========================================================
# RetailPulse Chart Utilities
# Version 2.0
# ==========================================================
