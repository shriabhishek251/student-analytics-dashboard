# app.py
import pandas as pd
import streamlit as st
from modules.loader import load_file
from modules.cleaner import clean_data
from modules.metrics import compute_metrics

st.set_page_config(
    page_title="Student Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ── Session state ──────────────────────────────────────────────────────────────
if "df_raw" not in st.session_state:
    st.session_state.df_raw = None
if "df_clean" not in st.session_state:
    st.session_state.df_clean = None
if "clean_report" not in st.session_state:
    st.session_state.clean_report = None
if "summary" not in st.session_state:
    st.session_state.summary = None
if "class_stats" not in st.session_state:
    st.session_state.class_stats = None

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("📊 Student Analytics Dashboard")
st.markdown("Upload your student marks data to get instant performance insights.")

st.sidebar.title("Navigation")
st.sidebar.markdown("**Step 1:** Upload your file below.")

# ── File Upload ────────────────────────────────────────────────────────────────
st.header("📂 Upload Data")

uploaded_file = st.file_uploader(
    label="Choose a CSV or Excel file",
    type=["csv", "xlsx", "xls"],
    help="File should contain student names and subject marks."
)

if uploaded_file is not None:
    df_raw, error = load_file(uploaded_file)

    if error:
        st.error(f"❌ {error}")
    else:
        df_clean, report = clean_data(df_raw)
        marks_cols = report["marks_columns"]
        summary, class_stats = compute_metrics(df_clean, marks_cols)

        st.session_state.df_raw = df_raw
        st.session_state.df_clean = df_clean
        st.session_state.clean_report = report
        st.session_state.summary = summary
        st.session_state.class_stats = class_stats

        st.success(f"✅ File uploaded, cleaned, and analysed: `{uploaded_file.name}`")

# ── Cleaning Report ────────────────────────────────────────────────────────────
if st.session_state.clean_report is not None:
    report = st.session_state.clean_report

    st.header("🧹 Data Cleaning Report")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Original Rows", report["original_rows"])
    col2.metric("Duplicates Removed", report["duplicates_removed"])
    col3.metric("Missing Values Filled", report["missing_values_filled"])
    col4.metric("Invalid Marks Fixed", report["invalid_marks_found"])

    if report["columns_renamed"]:
        st.warning("⚠️ Some column names were standardized:")
        for change in report["columns_renamed"]:
            st.write(f"  - `{change}`")

# ── Class Overview ─────────────────────────────────────────────────────────────
if st.session_state.class_stats is not None:
    stats = st.session_state.class_stats

    st.header("📈 Class Overview")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", stats["total_students"])
    col2.metric("Class Average", f"{stats['class_average']}%")
    col3.metric("Passed", stats["passed"])
    col4.metric("Failed", stats["failed"])

    col5, col6, col7 = st.columns(3)
    col5.metric("Pass Rate", f"{stats['pass_rate']}%")
    col6.metric("Highest Score", f"{stats['highest_score']}%")
    col7.metric("Lowest Score", f"{stats['lowest_score']}%")

    st.subheader("Grade Distribution")
    grade_df = pd.DataFrame(
        list(stats["grade_distribution"].items()),
        columns=["Grade", "Count"]
    ).sort_values("Grade")
    st.dataframe(grade_df, width='stretch')

# ── Student Summary Table ──────────────────────────────────────────────────────
if st.session_state.summary is not None:
    st.header("🎓 Student Performance Summary")
    st.dataframe(st.session_state.summary, width='stretch')

    if st.checkbox("Show only first 5 rows"):
        st.dataframe(st.session_state.summary.head(), width='stretch')