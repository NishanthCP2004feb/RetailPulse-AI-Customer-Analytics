"""
RetailPulse Helper Utilities

Common formatting functions used across
the Streamlit dashboard.
"""


def format_currency(value):
    """Format a numeric value as GBP currency."""
    return f"£{value:,.2f}"


def format_number(value):
    """Format an integer with thousands separators."""
    return f"{int(value):,}"


def format_percentage(value, decimals=2):
    """Format a numeric value as a percentage."""
    return f"{value:.{decimals}f}%"


def format_date(date):
    """Return a readable date string."""
    return date.strftime("%d %b %Y")


def safe_divide(numerator, denominator):
    """
    Prevent division-by-zero errors.
    """
    if denominator == 0:
        return 0
    return numerator / denominator