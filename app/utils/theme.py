"""
RetailPulse Theme Utilities
===========================

Global theme configuration for the
RetailPulse Dashboard.

Lightweight rendering layer.
All styling is defined in assets/style.css.
This module generates HTML structure only.

Centralizes

• Colors
• Chart palette
• CSS loader
• Page headers
• Dashboard styling

Author:
RetailPulse
"""

from pathlib import Path

import plotly.express as px
import streamlit as st

# ==========================================================
# Brand Colors
# ==========================================================

PRIMARY = "#2563EB"

SECONDARY = "#0EA5E9"

SUCCESS = "#22C55E"

WARNING = "#F59E0B"

DANGER = "#EF4444"

INFO = "#06B6D4"

BACKGROUND = "#F8FAFC"

CARD = "#FFFFFF"

TEXT = "#1F2937"

MUTED = "#6B7280"

BORDER = "#E5E7EB"

# ==========================================================
# Plotly Color Sequence
# ==========================================================

CHART_COLORS = [
    "#2563EB",
    "#22C55E",
    "#F59E0B",
    "#EF4444",
    "#8B5CF6",
    "#06B6D4",
    "#14B8A6",
    "#F97316",
]

PLOTLY_SEQUENCE = px.colors.qualitative.Set2

# ==========================================================
# CSS Loader
# ==========================================================


def load_css():
    """
    Load the global stylesheet.
    """
    css_path = (
        Path(__file__).resolve().parents[1]
        / "assets"
        / "style.css"
    )

    if css_path.exists():
        with open(css_path, encoding="utf-8") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True,
            )
    else:
        st.warning("style.css not found.")


# ==========================================================
# Page Header
# ==========================================================


def page_header(title: str, subtitle: str = ""):
    """
    Display a consistent page header.

    Uses CSS class .rp-page-header from style.css.
    """
    subtitle_html = ""
    if subtitle:
        subtitle_html = f'<p class="rp-subtitle">{subtitle}</p>'

    st.markdown(
        f'<div class="rp-page-header"><h1>{title}</h1>{subtitle_html}</div>',
        unsafe_allow_html=True,
    )


# ==========================================================
# Section Header
# ==========================================================


def section_header(title: str):
    """
    Display a styled section header.

    Uses CSS class .rp-section-header from style.css.
    """
    st.markdown(
        f'<h3 class="rp-section-header">{title}</h3>',
        unsafe_allow_html=True,
    )


# ==========================================================
# Divider
# ==========================================================


def dashboard_divider():
    """
    Display a styled horizontal divider.

    Uses the global hr style from style.css.
    """
    st.markdown("<hr>", unsafe_allow_html=True)


# ==========================================================
# Success Banner
# ==========================================================


def success_banner(message: str):
    """
    Display a success banner.

    Uses CSS classes .rp-banner .rp-banner-success from style.css.
    """
    st.markdown(
        f'<div class="rp-banner rp-banner-success">✅ {message}</div>',
        unsafe_allow_html=True,
    )


# ==========================================================
# Warning Banner
# ==========================================================


def warning_banner(message: str):
    """
    Display a warning banner.

    Uses CSS classes .rp-banner .rp-banner-warning from style.css.
    """
    st.markdown(
        f'<div class="rp-banner rp-banner-warning">⚠️ {message}</div>',
        unsafe_allow_html=True,
    )


# ==========================================================
# Error Banner
# ==========================================================


def error_banner(message: str):
    """
    Display an error banner.

    Uses CSS classes .rp-banner .rp-banner-danger from style.css.
    """
    st.markdown(
        f'<div class="rp-banner rp-banner-danger">❌ {message}</div>',
        unsafe_allow_html=True,
    )


# ==========================================================
# Info Banner
# ==========================================================


def info_banner(message: str):
    """
    Display an info banner.

    Uses CSS classes .rp-banner .rp-banner-info from style.css.
    """
    st.markdown(
        f'<div class="rp-banner rp-banner-info">ℹ️ {message}</div>',
        unsafe_allow_html=True,
    )


# ==========================================================
# KPI Card
# ==========================================================


def kpi_card(
    title: str,
    value: str,
    icon: str = "📊",
    color: str = PRIMARY,
):
    """
    Display a reusable KPI card.

    Uses CSS class .rp-kpi-card from style.css.
    The border-left-color is set via inline style
    to support dynamic colors per card.
    """
    st.markdown(
        f'<div class="rp-kpi-card" style="border-left-color:{color}">'
        f'<div class="kpi-label">{icon} {title}</div>'
        f'<div class="kpi-value">{value}</div>'
        f'</div>',
        unsafe_allow_html=True,
    )


# ==========================================================
# Status Badge
# ==========================================================


def status_badge(text: str, color: str = SUCCESS):
    """
    Display an inline status badge.

    Uses CSS class .rp-badge from style.css.
    Background color is set via inline style
    to support dynamic colors.
    """
    st.markdown(
        f'<span class="rp-badge" style="background:{color}">{text}</span>',
        unsafe_allow_html=True,
    )


# ==========================================================
# Footer
# ==========================================================


def dashboard_footer():
    """
    Display a consistent dashboard footer.

    Uses CSS class .rp-footer from style.css.
    """
    st.markdown(
        '<div class="rp-footer">'
        '<p>RetailPulse • AI-Powered Customer Analytics &amp; Demand Forecasting</p>'
        '<p>Built using Streamlit • Python • Plotly • Scikit-learn</p>'
        '</div>',
        unsafe_allow_html=True,
    )


# ==========================================================
# Plotly Theme
# ==========================================================


def apply_plotly_theme(fig):
    """
    Apply the RetailPulse Plotly theme to a figure.
    """
    fig.update_layout(
        template="plotly_white",
        colorway=CHART_COLORS,
        paper_bgcolor=BACKGROUND,
        plot_bgcolor="white",
        font=dict(
            family="Inter, Arial, sans-serif",
            size=13,
            color=TEXT,
        ),
        title_x=0.5,
        legend_title_text="",
        margin=dict(l=20, r=20, t=60, b=20),
    )
    return fig


# ==========================================================
# Render KPI Row
# ==========================================================


def render_kpi_row(kpis: list):
    """
    Render a row of KPI cards.

    Parameters
    ----------
    kpis : list of dict
        Each dict has keys: title, value, icon (optional),
        color (optional).

    Example
    -------
    render_kpi_row([
        {"title": "Revenue", "value": "£1,234", "icon": "💰"},
        {"title": "Orders", "value": "567", "icon": "📦"},
    ])
    """
    cols = st.columns(len(kpis))

    for col, kpi in zip(cols, kpis):
        with col:
            kpi_card(
                title=kpi.get("title", ""),
                value=str(kpi.get("value", "")),
                icon=kpi.get("icon", "📊"),
                color=kpi.get("color", PRIMARY),
            )


# ==========================================================
# Sidebar Filters
# ==========================================================


def sidebar_filters(df, filters=None):
    """
    Render reusable sidebar filters and return
    the filtered dataframe.

    Parameters
    ----------
    df : pd.DataFrame
        The source dataframe.
    filters : list of str, optional
        Column names to create multiselect filters for.
        Defaults to ["Country", "InvoiceYear"].

    Returns
    -------
    pd.DataFrame
        The filtered dataframe.
    """
    if filters is None:
        filters = ["Country", "InvoiceYear"]

    filtered = df.copy()

    for col in filters:
        if col not in df.columns:
            continue

        unique_values = sorted(
            df[col].dropna().unique()
        )

        selected = st.sidebar.multiselect(
            col,
            unique_values,
            default=unique_values,
            key=f"sidebar_filter_{col}",
        )

        filtered = filtered[
            filtered[col].isin(selected)
        ]

    return filtered


# ==========================================================
# Insight Card
# ==========================================================


def render_insight_card(
    title: str,
    items: list,
    card_type: str = "success",
):
    """
    Render a styled insight card with bullet points.

    Parameters
    ----------
    title : str
        Card heading.
    items : list of str
        Bullet-point items.
    card_type : str
        One of 'success', 'info', 'warning', 'danger'.

    Uses CSS classes from style.css:
    .rp-insight-card, .rp-info-card, .rp-risk-card, .rp-warning-card
    """
    class_map = {
        "success": "rp-insight-card",
        "info": "rp-info-card",
        "warning": "rp-warning-card",
        "danger": "rp-risk-card",
    }

    css_class = class_map.get(card_type, "rp-info-card")

    bullet_html = "".join(
        f"<p>• {item}</p>" for item in items
    )

    st.markdown(
        f'<div class="{css_class}"><h4>{title}</h4>{bullet_html}</div>',
        unsafe_allow_html=True,
    )


# ==========================================================
# Theme Dictionary
# ==========================================================

THEME = {
    "primary": PRIMARY,
    "secondary": SECONDARY,
    "success": SUCCESS,
    "warning": WARNING,
    "danger": DANGER,
    "info": INFO,
    "background": BACKGROUND,
    "card": CARD,
    "text": TEXT,
    "muted": MUTED,
    "border": BORDER,
    "chart_colors": CHART_COLORS,
}


# ==========================================================
# Export
# ==========================================================

__all__ = [
    "load_css",
    "page_header",
    "section_header",
    "dashboard_divider",
    "success_banner",
    "warning_banner",
    "error_banner",
    "info_banner",
    "kpi_card",
    "status_badge",
    "dashboard_footer",
    "apply_plotly_theme",
    "render_kpi_row",
    "sidebar_filters",
    "render_insight_card",
    "THEME",
]
