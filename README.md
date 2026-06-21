# Cambodia Education Analysis Dashboard (2015-2030) 🇰🇭

A comprehensive data science pipeline and interactive dashboard for analyzing trends, infrastructure, and student flow in the Cambodian education system. This project uses historical data (2015–2026) to provide insights into enrollment, teacher quality, and student outcomes, with machine learning forecasting through 2030.
## Team members:
- Leang Darita
- Oun Sivting
- Mab Ramorn
- Moeung David
- Ly Laisrun
## 📁 Project Structure

```text
MINI_PROJECT_AMS_B_GROUP3/
├── dashboard/              # Streamlit Application
│   └── app.py              # Main dashboard script (1372 lines)
├── data/                   # Data Storage
│   ├── raw/                # Original PDF, Excel, and CSV reports
│   ├── appendix.csv        # Long-term historical trends (1960s–2020s)
│   └── cleaned_new_data.csv # Main processed dataset (2015–2026)
├── notebooks/              # Research & Development
│   ├── 01_cleaning.ipynb   # PDF/Excel to CSV processing logic
│   ├── 02_modelling.ipynb  # ML models — feature projection approach
│   └── 03_modelling_lag_features.ipynb  # ML models — lag-based recursive forecasting
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies
```

## 🚀 Getting Started

### 1. Setup Environment
Ensure you have Python 3.9+ installed. It is recommended to use a virtual environment:

```bash
# Create a virtual environment
python -m venv .venv

# Activate it (Windows)
.venv\Scripts\activate

# Activate it (Mac/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Dashboard
The interactive Streamlit dashboard provides a deep dive into the data.
```bash
streamlit run dashboard/app.py
```

### 3. Data Processing & Modeling
If you wish to re-run the cleaning pipeline or the machine learning experiments:
*   Open `notebooks/01_cleaning.ipynb` to see how the raw data is transformed.
*   Open `notebooks/02_modelling.ipynb` for the standard feature-projection ML pipeline.
*   Open `notebooks/03_modelling_lag_features.ipynb` for the lag-based recursive forecasting approach.

## 📊 Dashboard Pages

### Overview & KPIs
High-level metrics for schools, enrollment, teaching staff, and gender parity, with trend charts over selected years.

### Schools & Infrastructure
Breakdown of schools by level (preschool, primary, college, lycee), building materials (concrete, wooden, bamboo), and access to water, toilets, libraries, and offices.

### Student Flow
Grade-by-grade analysis of promotion, repetition, and dropout rates — including heatmaps of dropout by province and year.

### Teaching Staff & Quality
Education-level mix of teaching staff, teacher quality index splits, and pupil–teacher ratio trends.

### Provincial Deep Dive
Comprehensive per-province analysis with enrollment trends, dropout rates, teacher education mix, building types, and grade flow.

### Relationship Analysis
Correlation heatmaps, scatter plots, pairplots, and lag-feature correlation analysis exploring how infrastructure, funding, staffing, and demographics relate to enrollment, dropout, and teacher quality (excl. 2021 anomaly).

### Modelling & Forecasts
Two ML forecasting pipelines:
* **Standard (Feature Projection)** — projects independent features (classrooms, population, etc.) using best-fit curves, then predicts targets using Random Forest, XGBoost, Gradient Boosting, SVR, Ridge, and Lasso.
* **Lag-Based (Recursive)** — uses 1- and 2-year lagged values as predictors with recursive multi-step forecasting for 2027–2028.

### Long-term Trends
Historical data from the appendix showing decade-scale growth in schools, classes, students, and staff, with indexed growth (base-year = 100) for relative comparison.

## 🛠️ Tech Stack
*   **Language**: Python
*   **Dashboard**: Streamlit
*   **Visualization**: Plotly, Seaborn, Matplotlib
*   **Data Handling**: Pandas, NumPy, GeoPandas
*   **ML**: Scikit-Learn, XGBoost, pmdarima

---
*Developed as part of the AMS_B Group 3 Mini Project.*
