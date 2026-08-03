from pathlib import Path

import streamlit as st


def load_css():
    """
    Load the global dashboard stylesheet.
    """
    css_path = (
        Path(__file__).resolve().parents[1]
        / "assets"
        / "style.css"
    )

    with open(css_path, encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )