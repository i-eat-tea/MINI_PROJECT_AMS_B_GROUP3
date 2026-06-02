# Cambodia Education Analysis Dashboard (2015-2026) 🇰🇭

A comprehensive data science pipeline and interactive dashboard for analyzing trends, infrastructure, and student flow in the Cambodian education system. This project uses historical data to provide insights into enrollment, teacher quality, and student outcomes, with predictive modeling for future trends.

## 📁 Project Structure

```text
Group_3_mini_project/
├── dashboard/              # Streamlit Application
│   └── app.py              # Main dashboard script
├── data/                   # Data Storage
│   ├── raw/                # Original PDF and Excel reports
│   ├── appendix.csv        # Long-term historical trends
│   └── cleaned_new_data.csv # Main processed dataset
├── notebooks/              # Research & Development
│   ├── 01_cleaning.ipynb   # PDF/Excel to CSV processing logic
│   └── 02_modelling.ipynb  # ML models (XGBoost, Random Forest)
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
*   Open `notebooks/02_modelling.ipynb` to view the forecasting models for dropout rates and enrollment.

## 📊 Key Features
*   **KPI Overview**: Real-time metrics for schools, students, and teachers.
*   **Infrastructure Analysis**: Tracking building materials and school facilities.
*   **Student Flow**: Detailed grade-by-grade analysis of promotion, repetition, and dropout rates.
*   **Teacher Quality**: Visualizing the educational background and qualification indices of teaching staff.
*   **Provincial Deep Dive**: Filterable analysis for every province in Cambodia.
*   **Machine Learning**: Predictive forecasting for enrollment and dropout trends through 2026.

## 🛠️ Tech Stack
*   **Language**: Python
*   **Dashboard**: Streamlit
*   **Visualization**: Plotly, Seaborn, Matplotlib
*   **Data Handling**: Pandas, NumPy, GeoPandas
*   **ML**: Scikit-Learn, XGBoost

---
*Developed as part of the AMS_B Group 3 Mini Project.*
