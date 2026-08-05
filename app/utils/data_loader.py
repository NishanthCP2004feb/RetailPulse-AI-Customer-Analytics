"""Cached, deployment-safe loaders for RetailPulse data assets."""

from __future__ import annotations

from pathlib import Path
from typing import NoReturn

import pandas as pd
import requests
import streamlit as st
from pandas.errors import EmptyDataError, ParserError
from requests.exceptions import ConnectionError, HTTPError, Timeout


# ==========================================================
# Base Directories
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
REPORTS_DIR = PROJECT_ROOT / "reports"
MODELS_DIR = PROJECT_ROOT / "models"


# ==========================================================
# Download Configuration
# ==========================================================

DATASET_URLS = {
    "retail_cleaned.csv": (
        "https://huggingface.co/datasets/NishanthCP/retailpulse-data/"
        "resolve/main/retail_cleaned.csv?download=true"
    ),
    "analysis_data.csv": (
        "https://huggingface.co/datasets/NishanthCP/retailpulse-data/"
        "resolve/main/analysis_data.csv?download=true"
    ),
}
DOWNLOAD_CHUNK_SIZE = 1024 * 1024
DOWNLOAD_TIMEOUT = (30, 600)
MIN_DOWNLOADED_FILE_SIZE = 1024 * 1024
LFS_POINTER_MARKER = b"version https://git-lfs.github.com/spec/v1"


def _stop_with_error(message: str) -> NoReturn:
    """Display a user-facing Streamlit error and halt the current page."""
    st.error(message)
    st.stop()
    raise RuntimeError(message)  # Satisfies static type checkers if st.stop returns.


def _is_lfs_pointer(path: Path) -> bool:
    """Return whether *path* is a Git LFS pointer rather than CSV content."""
    try:
        with path.open("rb") as file_handle:
            return LFS_POINTER_MARKER in file_handle.read(4096)
    except (FileNotFoundError, PermissionError, OSError):
        return False


def _remove_file(path: Path) -> None:
    """Remove a known-invalid temporary or pointer file where possible."""
    try:
        if path.exists():
            path.unlink()
    except (PermissionError, OSError):
        pass


def _download_dataset(path: Path, url: str) -> None:
    """Download one supported dataset atomically, with validation."""
    temporary_path = path.with_name(f"{path.name}.part")

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        _remove_file(temporary_path)

        with st.spinner(f"Downloading {path.name}..."):
            with requests.get(url, stream=True, timeout=DOWNLOAD_TIMEOUT) as response:
                response.raise_for_status()
                with temporary_path.open("wb") as file_handle:
                    for chunk in response.iter_content(chunk_size=DOWNLOAD_CHUNK_SIZE):
                        if chunk:
                            file_handle.write(chunk)

        if not temporary_path.exists() or temporary_path.stat().st_size == 0:
            _remove_file(temporary_path)
            _stop_with_error(
                f"Download failed: {path.name} was empty. Please try again."
            )

        if _is_lfs_pointer(temporary_path):
            _remove_file(temporary_path)
            _stop_with_error(
                f"Download failed: {path.name} is a Git LFS pointer, not the "
                "actual dataset."
            )

        if temporary_path.stat().st_size <= MIN_DOWNLOADED_FILE_SIZE:
            _remove_file(temporary_path)
            _stop_with_error(
                f"Download failed: {path.name} appears incomplete or corrupted."
            )

        temporary_path.replace(path)
    except ConnectionError:
        _remove_file(temporary_path)
        _stop_with_error(
            f"Unable to download {path.name}: network connection failed."
        )
    except Timeout:
        _remove_file(temporary_path)
        _stop_with_error(f"Unable to download {path.name}: request timed out.")
    except HTTPError as error:
        _remove_file(temporary_path)
        _stop_with_error(
            f"Unable to download {path.name}: server returned HTTP "
            f"{error.response.status_code if error.response else 'error'}."
        )
    except FileNotFoundError:
        _remove_file(temporary_path)
        _stop_with_error(f"Unable to save {path.name}: download path was not found.")
    except PermissionError:
        _remove_file(temporary_path)
        _stop_with_error(f"Unable to save {path.name}: permission was denied.")
    except requests.RequestException:
        _remove_file(temporary_path)
        _stop_with_error(f"Unable to download {path.name}. Please try again.")
    except OSError:
        _remove_file(temporary_path)
        _stop_with_error(f"Unable to save {path.name}: a filesystem error occurred.")


def _ensure_dataset(path: Path) -> None:
    """Ensure remote-backed datasets exist locally and are not LFS pointers."""
    url = DATASET_URLS.get(path.name)

    if path.exists() and _is_lfs_pointer(path):
        _remove_file(path)

    if path.exists():
        return

    if url is None:
        _stop_with_error(f"Missing file:\n{path}")

    _download_dataset(path, url)


# ==========================================================
# Generic CSV Loader
# ==========================================================

@st.cache_data(show_spinner=False)
def _load_csv(path: Path, parse_dates=None):
    """Load a CSV without changing its schema or values."""
    _ensure_dataset(path)

    try:
        return pd.read_csv(path, parse_dates=parse_dates)
    except FileNotFoundError:
        _stop_with_error(f"Missing file:\n{path}")
    except PermissionError:
        _stop_with_error(f"Unable to load {path.name}: permission was denied.")
    except (EmptyDataError, ParserError, UnicodeDecodeError):
        _stop_with_error(
            f"Unable to load {path.name}: the CSV is invalid or corrupted."
        )
    except (OSError, ValueError) as error:
        _stop_with_error(f"Unable to load\n{path.name}\n\n{error}")
    except Exception as error:
        _stop_with_error(f"Unable to load\n{path.name}\n\n{error}")


# ==========================================================
# Retail Dataset
# ==========================================================

@st.cache_data(show_spinner=False)
def load_retail_data():
    """Load the cleaned retail transaction dataset."""
    return _load_csv(PROCESSED_DIR / "retail_cleaned.csv", parse_dates=["InvoiceDate"])


# ==========================================================
# Customer RFM
# ==========================================================

@st.cache_data(show_spinner=False)
def load_customer_rfm():
    """Load customer RFM metrics."""
    return _load_csv(PROCESSED_DIR / "customer_rfm.csv")


# ==========================================================
# Customer Features
# ==========================================================

@st.cache_data(show_spinner=False)
def load_customer_features():
    """Load customer features."""
    return _load_csv(PROCESSED_DIR / "customer_features.csv")


# ==========================================================
# Daily Sales
# ==========================================================

@st.cache_data(show_spinner=False)
def load_daily_sales():
    """Load daily sales data."""
    return _load_csv(PROCESSED_DIR / "daily_sales.csv", parse_dates=["Date"])


# ==========================================================
# Analysis Dataset
# ==========================================================

@st.cache_data(show_spinner=False)
def load_analysis_data():
    """Load the dashboard analysis dataset."""
    return _load_csv(PROCESSED_DIR / "analysis_data.csv", parse_dates=["InvoiceDate"])


# ==========================================================
# Forecast Reports
# ==========================================================

@st.cache_data(show_spinner=False)
def load_forecast_results():
    """Load forecast results."""
    return _load_csv(REPORTS_DIR / "forecast_results.csv", parse_dates=["Date"])


@st.cache_data(show_spinner=False)
def load_forecast_model_comparison():
    """Load forecasting-model comparison results."""
    return _load_csv(REPORTS_DIR / "forecasting_model_comparison.csv")


@st.cache_data(show_spinner=False)
def load_forecast_dataset_summary():
    """Load the forecast dataset summary."""
    return _load_csv(REPORTS_DIR / "forecasting_dataset_summary.csv")


# ==========================================================
# Churn
# ==========================================================

@st.cache_data(show_spinner=False)
def load_churn_data():
    """Load high-risk customers with their purchase dates parsed."""
    df = _load_csv(REPORTS_DIR / "high_risk_customers.csv")

    if "FirstPurchase" in df.columns:
        df["FirstPurchase"] = pd.to_datetime(df["FirstPurchase"])

    if "LastPurchase" in df.columns:
        df["LastPurchase"] = pd.to_datetime(df["LastPurchase"])

    return df


# ==========================================================
# Inventory
# ==========================================================

@st.cache_data(show_spinner=False)
def load_inventory_summary():
    """Load inventory summary data."""
    return _load_csv(REPORTS_DIR / "inventory_summary.csv")


@st.cache_data(show_spinner=False)
def load_inventory_recommendations():
    """Load inventory recommendations."""
    return _load_csv(REPORTS_DIR / "inventory_recommendations.csv")


# ==========================================================
# Recommendation System
# ==========================================================

@st.cache_data(show_spinner=False)
def load_recommendations():
    """Load customer product recommendations."""
    return _load_csv(REPORTS_DIR / "customer_product_recommendations.csv")


# ==========================================================
# Business Recommendations
# ==========================================================

@st.cache_data(show_spinner=False)
def load_business_recommendations():
    """Load business recommendations."""
    return _load_csv(REPORTS_DIR / "business_recommendations.csv")


# ==========================================================
# Combined Loaders
# ==========================================================

@st.cache_data(show_spinner=False)
def load_forecast_reports():
    """Load all forecast report datasets."""
    return (
        load_forecast_results(),
        load_forecast_model_comparison(),
        load_forecast_dataset_summary(),
    )


@st.cache_data(show_spinner=False)
def load_inventory_reports():
    """Load inventory report datasets."""
    return load_inventory_summary(), load_inventory_recommendations()


@st.cache_data(show_spinner=False)
def load_business_reports():
    """Load all datasets used by the business reports."""
    return (
        load_forecast_results(),
        load_forecast_model_comparison(),
        load_churn_data(),
        load_inventory_summary(),
        load_recommendations(),
        load_business_recommendations(),
    )
