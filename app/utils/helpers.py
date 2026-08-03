"""
RetailPulse Helper Utilities
============================

Reusable formatting and helper functions
used across the RetailPulse dashboard.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any


# ==========================================================
# Currency Formatting
# ==========================================================

def format_currency(value: float) -> str:
    """Format currency as GBP."""

    if value is None:
        value = 0

    return f"£{value:,.2f}"


# ==========================================================
# Compact Currency
# ==========================================================

def format_compact_currency(value: float) -> str:

    if value is None:
        return "£0"

    value = float(value)

    if abs(value) >= 1_000_000:
        return f"£{value/1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"£{value/1_000:.2f}K"

    return f"£{value:,.2f}"


# ==========================================================
# Number Formatting
# ==========================================================

def format_number(value: Any) -> str:

    if value is None:
        value = 0

    return f"{int(value):,}"


# ==========================================================
# Compact Number
# ==========================================================

def format_compact_number(value: Any) -> str:

    if value is None:
        return "0"

    value = float(value)

    if abs(value) >= 1_000_000:
        return f"{value/1_000_000:.2f}M"

    if abs(value) >= 1_000:
        return f"{value/1_000:.2f}K"

    return f"{value:,.0f}"


# ==========================================================
# Percentage
# ==========================================================

def format_percentage(
    value: float,
    decimals: int = 2,
) -> str:

    if value is None:
        value = 0

    return f"{value:.{decimals}f}%"


# ==========================================================
# Date Formatting
# ==========================================================

def format_date(date: datetime) -> str:

    if date is None:
        return "-"

    return date.strftime("%d %b %Y")

# ==========================================================
# Safe Division
# ==========================================================

def safe_divide(
    numerator: float,
    denominator: float,
) -> float:
    """
    Prevent division-by-zero errors.
    """

    if denominator in (0, None):
        return 0.0

    return numerator / denominator


# ==========================================================
# Growth Percentage
# ==========================================================

def calculate_growth(
    current: float,
    previous: float,
) -> float:
    """
    Calculate percentage growth.
    """

    if previous in (0, None):
        return 0.0

    return ((current - previous) / previous) * 100


# ==========================================================
# KPI Delta Formatter
# ==========================================================

def format_delta(value: float) -> str:
    """
    Format KPI delta.
    """

    if value > 0:
        return f"▲ {value:.2f}%"

    if value < 0:
        return f"▼ {abs(value):.2f}%"

    return "0.00%"


# ==========================================================
# Trend Indicator
# ==========================================================

def trend_indicator(value: float) -> str:
    """
    Return trend icon.
    """

    if value > 0:
        return "🟢"

    if value < 0:
        return "🔴"

    return "🟡"


# ==========================================================
# Safe Percentage
# ==========================================================

def safe_percentage(
    numerator: float,
    denominator: float,
) -> float:
    """
    Safe percentage calculation.
    """

    return safe_divide(
        numerator * 100,
        denominator,
    )


# ==========================================================
# Missing Value Handler
# ==========================================================

def safe_value(
    value,
    default="-",
):
    """
    Return default if value is None or NaN.
    """

    if value is None:
        return default

    try:
        if value != value:  # NaN check
            return default
    except Exception:
        pass

    return value


# ==========================================================
# Text Truncation
# ==========================================================

def truncate_text(
    text: str,
    max_length: int = 40,
) -> str:
    """
    Truncate long text.
    """

    if text is None:
        return ""

    if len(text) <= max_length:
        return text

    return text[: max_length - 3] + "..."


# ==========================================================
# Export Functions
# ==========================================================

__all__ = [

    "format_currency",

    "format_compact_currency",

    "format_number",

    "format_compact_number",

    "format_percentage",

    "format_date",

    "safe_divide",

    "calculate_growth",

    "format_delta",

    "trend_indicator",

    "safe_percentage",

    "safe_value",

    "truncate_text",

]