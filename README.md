<p align="center">
  <h1 align="center">🛍️ RetailPulse</h1>
  <p align="center"><strong>AI-Powered Customer Analytics & Demand Forecasting</strong></p>
  <p align="center">
    An end-to-end retail intelligence platform combining customer segmentation, demand forecasting, churn prediction, inventory optimization, and AI-driven product recommendations — presented through an interactive Streamlit dashboard.
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-1.24+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/Plotly-5.14+-3F4F75?style=for-the-badge&logo=plotly&logoColor=white" alt="Plotly">
  <img src="https://img.shields.io/badge/Scikit--learn-1.2+-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge" alt="License">
</p>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Usage](#-usage)
- [Dashboard Modules](#-dashboard-modules)
- [Data Pipeline](#-data-pipeline)
- [ML Models](#-ml-models)
- [Notebook Pipeline](#-notebook-pipeline)
- [Contributing](#-contributing)
- [License](#-license)
- [Author](#-author)

---

## 🎯 Overview

**RetailPulse** is a production-grade retail analytics platform built on the [UCI Online Retail II](https://archive.ics.uci.edu/ml/datasets/Online+Retail+II) dataset. The project follows a two-stage architecture:

1. **Notebook Pipeline** — Jupyter notebooks handle data cleaning, feature engineering, model training, and report generation.
2. **Streamlit Dashboard** — A read-only, multi-page dashboard consumes the pre-computed datasets, trained models, and exported reports to deliver interactive business intelligence.

> **Important:** The Streamlit application does **not** retrain models or modify datasets. It operates as a presentation and decision-support layer on top of the notebook-generated artifacts.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 📊 **Executive Dashboard** | High-level KPIs, revenue trends, and business overview |
| 📈 **Sales Analytics** | Revenue analysis by country, product, time period, and day of week |
| 📦 **Product Performance** | Product-level revenue, Pareto analysis, and performance ranking |
| 👥 **Customer Analytics** | Customer segmentation, RFM analysis, and behavior patterns |
| 🌍 **Country Analytics** | Geographic revenue distribution and market comparison |
| 📉 **Demand Forecasting** | ML-powered sales forecasting with model comparison |
| ⚠️ **Churn Prediction** | Customer churn risk scoring with retention recommendations |
| 📦 **Inventory Optimization** | Stock management, demand tracking, and restock recommendations |
| 🎯 **Recommendation System** | AI-driven personalized product recommendations per customer segment |
| 💡 **Business Insights** | Cross-module executive intelligence and health scoring |
| 📊 **Interactive Analytics** | Self-service data exploration with dynamic filtering and chart builder |

---

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Raw Data (Excel)                    │
│              data/raw/online_retail_II.xlsx          │
└──────────────────────┬──────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────┐
│             Notebook Pipeline (Jupyter)              │
│  01_data_preparation → 02_EDA → 03_RFM_segmentation │
│  04_forecast_prep → 05_forecasting → 06_churn       │
│  07_inventory → 08_recommendations → 09_dashboard   │
└──────────┬─────────────────────┬────────────────────┘
           │                     │
     ┌─────▼─────┐        ┌─────▼─────┐
     │  data/     │        │  reports/ │
     │ processed/ │        │  *.csv    │
     │  *.csv     │        │  figures/ │
     └─────┬──────┘        └─────┬────┘
           │                     │
     ┌─────▼─────┐              │
     │  models/  │              │
     │  *.pkl    │              │
     └─────┬─────┘              │
           │                    │
           ▼                    ▼
┌─────────────────────────────────────────────────────┐
│          Streamlit Dashboard (Read-Only)             │
│                  app/app.py                          │
│              app/pages/01–11_*.py                    │
│              app/utils/*.py                          │
└─────────────────────────────────────────────────────┘
```

---

## 🛠 Tech Stack

| Category | Technologies |
|----------|-------------|
| **Language** | Python 3.9+ |
| **Frontend** | Streamlit |
| **Visualization** | Plotly Express, Plotly Graph Objects |
| **Data Processing** | Pandas, NumPy |
| **Machine Learning** | Scikit-learn (KMeans, Churn Classification) |
| **Forecasting** | Model comparison pipeline (Prophet, ARIMA, etc. via notebooks) |
| **Model Serialization** | Joblib |
| **Styling** | Custom CSS with glassmorphism, Inter font, responsive design |

---

## 📁 Project Structure

```
RetailPulse-AI-Customer-Analytics/
│
├── app/                            # Streamlit application
│   ├── app.py                      # Main entry point
│   ├── .streamlit/
│   │   └── config.toml             # Streamlit theme & server config
│   ├── assets/
│   │   └── style.css               # Enterprise CSS theme (583 lines)
│   ├── pages/                      # Multi-page dashboard modules
│   │   ├── 01_Executive_Dashboard.py
│   │   ├── 02_Sales_Analytics.py
│   │   ├── 03_Product_Performance.py
│   │   ├── 04_Customer_Analytics.py
│   │   ├── 05_Country_Analytics.py
│   │   ├── 06_Forecasting.py
│   │   ├── 07_Churn_Analytics.py
│   │   ├── 08_Inventory_Optimization.py
│   │   ├── 09_Recommendation_System.py
│   │   ├── 10_Business_Insights.py
│   │   └── 11_Interactive_Analytics.py
│   └── utils/                      # Shared utility modules
│       ├── __init__.py
│       ├── chart_utils.py          # Plotly chart factory (614 lines)
│       ├── data_loader.py          # Centralized data I/O (208 lines)
│       ├── helpers.py              # Formatting utilities (306 lines)
│       ├── metrics.py              # KPI calculation engine (469 lines)
│       ├── model_loader.py         # ML model loading interface (163 lines)
│       └── theme.py                # UI component library (508 lines)
│
├── data/
│   ├── raw/                        # Original dataset
│   │   └── online_retail_II.xlsx
│   ├── processed/                  # Cleaned & feature-engineered data
│   │   ├── retail_cleaned.csv
│   │   ├── analysis_data.csv
│   │   ├── customer_rfm.csv
│   │   ├── customer_features.csv
│   │   ├── customer_segments.csv
│   │   ├── daily_sales.csv
│   │   ├── daily_sales_features.csv
│   │   ├── train_sales.csv
│   │   ├── test_sales.csv
│   │   └── cluster_validation.csv
│   └── external/                   # External data sources (placeholder)
│
├── models/                         # Trained ML model artifacts
│   ├── best_forecasting_model.pkl
│   ├── customer_churn_model.pkl
│   ├── churn_prediction_model.pkl
│   ├── kmeans_model.pkl
│   └── scaler.pkl
│
├── notebooks/                      # Jupyter notebook pipeline
│   ├── 01_data_preparation.ipynb
│   ├── 02_exploratory_data_analysis.ipynb
│   ├── 03_customer_segmentation_rfm.ipynb
│   ├── 04_sales_forecasting_data_preparation.ipynb
│   ├── 05_sales_forecasting_model_development.ipynb
│   ├── 05A_customer_feature_engineering.ipynb
│   ├── 06_customer_churn_prediction.ipynb
│   ├── 07_inventory_optimization_and_business_recommendations.ipynb
│   ├── 08_recommendation_system.ipynb
│   ├── 09_retailpulse_dashboard.ipynb
│   └── 10_streamlit_deployment.ipynb
│
├── reports/                        # Notebook-generated reports
│   ├── forecast_results.csv
│   ├── forecasting_model_comparison.csv
│   ├── forecasting_dataset_summary.csv
│   ├── high_risk_customers.csv
│   ├── inventory_summary.csv
│   ├── inventory_recommendations.csv
│   ├── customer_product_recommendations.csv
│   ├── business_recommendations.csv
│   ├── figures/                    # 34 analysis visualizations
│   └── pdf/                        # PDF reports (placeholder)
│
├── src/                            # Python source modules (scaffolding)
│   ├── data/
│   ├── features/
│   ├── forecasting/
│   ├── inventory/
│   ├── ml/
│   ├── utils/
│   └── visualization/
│
├── tests/                          # Test suite (placeholder)
├── docs/                           # Documentation (placeholder)
│
├── requirements.txt                # Python dependencies
├── LICENSE                         # MIT License
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

---

## 🚀 Installation

### Prerequisites

- **Python** 3.9 or higher
- **pip** package manager
- **Git** (for cloning)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/NishanthCP2004feb/RetailPulse-AI-Customer-Analytics.git
cd RetailPulse-AI-Customer-Analytics

# 2. Create a virtual environment (recommended)
python -m venv .venv

# 3. Activate the virtual environment
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt
```

---

## ▶️ Usage

### Running the Dashboard

```bash
# Navigate to the app directory
cd app

# Launch the Streamlit dashboard
streamlit run app.py
```

The dashboard will open in your default browser at `http://localhost:8501`.

### Running the Notebook Pipeline

To regenerate the processed datasets and trained models:

```bash
# Open Jupyter and run notebooks 01–10 in order
jupyter notebook notebooks/
```

> **Note:** Run notebooks sequentially (01 → 10). Each notebook depends on the outputs of the previous one.

---

## 📊 Dashboard Modules

### 1. Executive Dashboard
High-level business overview with revenue, orders, customer, and product KPIs. Includes monthly sales trends and top product rankings.

### 2. Sales Analytics
Deep-dive into sales performance with filters by country, year, and month. Features revenue trends, day-of-week analysis, distribution charts, and scatter plots.

### 3. Product Performance
Product-level analytics including revenue ranking, Pareto (80/20) analysis, quantity distribution, and a searchable product table with export capability.

### 4. Customer Analytics
Customer behavior analysis with RFM-based segmentation, top customer identification, revenue distribution, and monthly active customer tracking.

### 5. Country Analytics
Geographic market analysis with country-level KPIs, revenue contribution, Pareto analysis, and interactive search with downloadable reports.

### 6. Demand Forecasting
ML model performance dashboard comparing forecasting models by MAE/RMSE. Includes actual vs. predicted visualization, error analysis, and monthly summaries.

### 7. Churn Analytics
Customer churn risk assessment with probability distributions, revenue-at-risk calculations, customer lifetime analysis, and retention recommendations.

### 8. Inventory Optimization
Stock management dashboard with inventory status tracking, demand classification, product search, and notebook-generated restock recommendations.

### 9. Recommendation System
Personalized product recommendation viewer organized by customer segment. Includes recommendation coverage analysis and cross-selling insights.

### 10. Business Insights
Executive-level cross-module intelligence dashboard combining forecasting, churn, inventory, and recommendation data with a composite health score.

### 11. Interactive Analytics
Self-service analytics workbench with a dynamic chart builder, date range filtering, revenue heatmaps, hourly sales analysis, and data export.

---

## 🔄 Data Pipeline

```
Raw Excel → Data Cleaning → Feature Engineering → Model Training → Report Export → Dashboard
```

| Stage | Notebook | Output |
|-------|----------|--------|
| Data Preparation | `01_data_preparation.ipynb` | `retail_cleaned.csv` |
| EDA | `02_exploratory_data_analysis.ipynb` | 34 analysis figures |
| Customer Segmentation | `03_customer_segmentation_rfm.ipynb` | `customer_rfm.csv`, `customer_segments.csv`, `kmeans_model.pkl` |
| Forecast Preparation | `04_sales_forecasting_data_preparation.ipynb` | `daily_sales.csv`, `daily_sales_features.csv` |
| Feature Engineering | `05A_customer_feature_engineering.ipynb` | `customer_features.csv` |
| Sales Forecasting | `05_sales_forecasting_model_development.ipynb` | `best_forecasting_model.pkl`, `forecast_results.csv` |
| Churn Prediction | `06_customer_churn_prediction.ipynb` | `customer_churn_model.pkl`, `high_risk_customers.csv` |
| Inventory Optimization | `07_inventory_optimization_and_business_recommendations.ipynb` | `inventory_summary.csv`, `inventory_recommendations.csv` |
| Recommendations | `08_recommendation_system.ipynb` | `customer_product_recommendations.csv` |
| Dashboard Report | `09_retailpulse_dashboard.ipynb` | `analysis_data.csv`, `business_recommendations.csv` |

---

## 🤖 ML Models

| Model | File | Purpose |
|-------|------|---------|
| **Forecasting** | `best_forecasting_model.pkl` (949 KB) | Time-series demand prediction |
| **Churn Classifier** | `customer_churn_model.pkl` (1.7 MB) | Customer churn probability scoring |
| **Churn Predictor** | `churn_prediction_model.pkl` (1.3 KB) | Lightweight churn prediction |
| **KMeans Clustering** | `kmeans_model.pkl` (24 KB) | Customer segmentation |
| **Feature Scaler** | `scaler.pkl` (642 B) | StandardScaler for feature normalization |

---

## 📓 Notebook Pipeline

The notebook pipeline must be executed in order. Each notebook is self-contained with its own documentation:

| # | Notebook | Description |
|---|----------|-------------|
| 01 | Data Preparation | Raw data loading, cleaning, and initial feature creation |
| 02 | Exploratory Data Analysis | Comprehensive statistical analysis and visualization |
| 03 | Customer Segmentation (RFM) | Recency-Frequency-Monetary analysis with KMeans clustering |
| 04 | Forecast Data Preparation | Time-series data preparation for forecasting models |
| 05 | Sales Forecasting | Model training, evaluation, and comparison |
| 05A | Customer Feature Engineering | Advanced customer-level feature creation |
| 06 | Churn Prediction | Customer churn classification model development |
| 07 | Inventory Optimization | Stock analysis and business recommendation generation |
| 08 | Recommendation System | Collaborative filtering and product recommendation |
| 09 | Dashboard Report | Final data preparation for the Streamlit dashboard |
| 10 | Streamlit Deployment | Deployment configuration and instructions |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Nishanth C P**

---

<p align="center">
  <strong>RetailPulse</strong> • AI-Powered Customer Analytics & Demand Forecasting<br>
  Built with ❤️ using Python, Streamlit, Plotly, and Scikit-learn
</p>
