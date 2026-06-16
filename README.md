# Student Analytics Dashboard

A web-based dashboard built with Python and Streamlit to analyze student performance data from CSV/Excel files.

## Features
- Upload marks data (CSV/Excel)
- Automatic data cleaning
- Performance metrics & grade distribution
- Subject-wise analysis
- Topper & at-risk student identification
- Visual charts
- Export reports

## Tech Stack
Python · Pandas · Plotly · Streamlit

## Setup
```bash
git clone <your-repo-url>
cd student-analytics-dashboard
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```