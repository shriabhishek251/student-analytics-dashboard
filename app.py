# app.py

import streamlit as st
from modules.loader import load_file
from modules.cleaner import clean_data

st.set_page_config(
    page_title="Student Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ── Session state ─────────────────────────────────────────────────────────────
if "df_raw" not in st.session_state:
    st.session_state.df_raw = None
if "df_clean" not in st.session_state:
    st.session_state.df_clean = None
if "clean_report" not in st.session_state:
    st.session_state.clean_report = None

# ── Header ────────────────────────────────────────────────────────────────────
st.title("📊 Student Analytics Dashboard")
st.markdown("Upload your student marks data to get instant performance insights.")

st.sidebar.title("Navigation")
st.sidebar.markdown("**Step 1:** Upload your file below.")

# ── File Upload ───────────────────────────────────────────────────────────────
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
        st.session_state.df_raw = df_raw
        st.session_state.df_clean = df_clean
        st.session_state.clean_report = report
        st.success(f"✅ File uploaded and cleaned: `{uploaded_file.name}`")

# ── Cleaning Report ───────────────────────────────────────────────────────────
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

    st.markdown(f"**Marks columns detected:** `{report['marks_columns']}`")

# ── Data Display ──────────────────────────────────────────────────────────────
if st.session_state.df_clean is not None:
    df = st.session_state.df_clean

    st.header("🗂️ Cleaned Data Preview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Subjects Detected", len(st.session_state.clean_report["marks_columns"]))

    st.markdown("**Columns:**")
    st.write(list(df.columns))

    st.dataframe(df, width='stretch')

    if st.checkbox("Show only first 5 rows"):
        st.dataframe(df.head(), width='stretch')