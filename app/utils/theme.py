"""
RetailPulse Theme Utilities
===========================

Global theme configuration for the
RetailPulse Dashboard.

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

        with open(

            css_path,

            encoding="utf-8",

        ) as f:

            st.markdown(

                f"<style>{f.read()}</style>",

                unsafe_allow_html=True,

            )

    else:

        st.warning(

            "style.css not found."

        )

        # ==========================================================
# Page Header
# ==========================================================

def page_header(
    title: str,
    subtitle: str = "",
):
    """
    Display a consistent page header.
    """

    st.markdown(
        f"""
<div style="padding:12px 0 20px 0;">
    <h1 style="
        margin-bottom:4px;
        color:{PRIMARY};
        font-size:34px;
        font-weight:700;
    ">
        {title}
    </h1>

    <p style="
        color:{MUTED};
        font-size:16px;
        margin-top:0;
    ">
        {subtitle}
    </p>
</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Section Header
# ==========================================================

def section_header(
    title: str,
):

    st.markdown(
        f"""
<h3 style="
color:{TEXT};
margin-top:18px;
margin-bottom:10px;
font-weight:600;
border-left:5px solid {PRIMARY};
padding-left:10px;
">
{title}
</h3>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Divider
# ==========================================================

def dashboard_divider():

    st.markdown(
        """
<hr style="
margin-top:15px;
margin-bottom:20px;
border:0;
height:1px;
background:#E5E7EB;
">
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Success Banner
# ==========================================================

def success_banner(message: str):

    st.markdown(
        f"""
<div style="
background:#ECFDF5;
border-left:6px solid {SUCCESS};
padding:14px;
border-radius:8px;
margin-bottom:18px;
font-weight:500;
color:#065F46;
">
✅ {message}
</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Warning Banner
# ==========================================================

def warning_banner(message: str):

    st.markdown(
        f"""
<div style="
background:#FFFBEB;
border-left:6px solid {WARNING};
padding:14px;
border-radius:8px;
margin-bottom:18px;
font-weight:500;
color:#92400E;
">
⚠️ {message}
</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Error Banner
# ==========================================================

def error_banner(message: str):

    st.markdown(
        f"""
<div style="
background:#FEF2F2;
border-left:6px solid {DANGER};
padding:14px;
border-radius:8px;
margin-bottom:18px;
font-weight:500;
color:#991B1B;
">
❌ {message}
</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Info Banner
# ==========================================================

def info_banner(message: str):

    st.markdown(
        f"""
<div style="
background:#EFF6FF;
border-left:6px solid {PRIMARY};
padding:14px;
border-radius:8px;
margin-bottom:18px;
font-weight:500;
color:#1E3A8A;
">
ℹ️ {message}
</div>
""",
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
    """

    st.markdown(
        f"""
<div style="
background:white;
padding:18px;
border-radius:14px;
border-left:6px solid {color};
box-shadow:0 2px 8px rgba(0,0,0,0.08);
margin-bottom:12px;
">

<div style="
font-size:15px;
color:{MUTED};
margin-bottom:8px;
">

{icon} {title}

</div>

<div style="
font-size:30px;
font-weight:700;
color:{TEXT};
">

{value}

</div>

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Status Badge
# ==========================================================

def status_badge(
    text: str,
    color: str = SUCCESS,
):

    st.markdown(
        f"""
<span style="
display:inline-block;
padding:6px 12px;
border-radius:20px;
background:{color};
color:white;
font-size:13px;
font-weight:600;
">
{text}
</span>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Footer
# ==========================================================

def dashboard_footer():

    st.markdown(
        f"""
<hr>

<div style="
text-align:center;
padding:15px;
font-size:13px;
color:{MUTED};
">

RetailPulse • AI-Powered Customer Analytics & Demand Forecasting

Built using Streamlit • Python • Plotly • Scikit-learn

</div>
""",
        unsafe_allow_html=True,
    )


# ==========================================================
# Plotly Theme
# ==========================================================

def apply_plotly_theme(fig):

    fig.update_layout(

        template="plotly_white",

        colorway=CHART_COLORS,

        paper_bgcolor=BACKGROUND,

        plot_bgcolor="white",

        font=dict(

            family="Arial",

            size=13,

            color=TEXT,

        ),

        title_x=0.5,

        legend_title_text="",

        margin=dict(

            l=20,

            r=20,

            t=60,

            b=20,

        ),

    )

    return fig


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

    "THEME",

]
