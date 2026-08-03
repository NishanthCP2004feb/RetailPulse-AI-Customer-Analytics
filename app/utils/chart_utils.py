"""
RetailPulse Chart Utilities

Reusable Plotly chart functions for the
RetailPulse Streamlit dashboard.

All functions are read-only and return Plotly Figure objects.
"""

import plotly.express as px


def create_monthly_sales_chart(df):
    """
    Create a monthly revenue bar chart.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    plotly.graph_objects.Figure
    """

    monthly_sales = (
        df.groupby("InvoiceMonthYear", as_index=False)["TotalAmount"]
        .sum()
        .sort_values("InvoiceMonthYear")
    )

    fig = px.bar(
        monthly_sales,
        x="InvoiceMonthYear",
        y="TotalAmount",
        title="Monthly Sales Revenue",
        labels={
            "InvoiceMonthYear": "Month",
            "TotalAmount": "Revenue (£)"
        },
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Month",
        yaxis_title="Revenue (£)",
        title_x=0.5,
        height=450,
    )

    return fig


def create_top_products_chart(df, top_n=10):
    """
    Create Top-N products by revenue.
    """

    products = (
        df.groupby("ProductDescription", as_index=False)["TotalAmount"]
        .sum()
        .nlargest(top_n, "TotalAmount")
    )

    fig = px.bar(
        products,
        x="TotalAmount",
        y="ProductDescription",
        orientation="h",
        title=f"Top {top_n} Products by Revenue",
        labels={
            "TotalAmount": "Revenue (£)",
            "ProductDescription": "Product",
        },
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        height=500,
    )

    return fig