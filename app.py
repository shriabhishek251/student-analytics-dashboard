# app.py

import streamlit as st
from modules.loader import load_file

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="Student Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# ── Initialize session state ─────────────────────────────────────────────────
if "df" not in st.session_state:
    st.session_state.df = None

# ── Header ───────────────────────────────────────────────────────────────────
st.title("📊 Student Analytics Dashboard")
st.markdown("Upload your student marks data to get instant performance insights.")

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("Navigation")
st.sidebar.markdown("**Step 1:** Upload your file below.")

# ── File Upload Section ───────────────────────────────────────────────────────
st.header("📂 Upload Data")

uploaded_file = st.file_uploader(
    label="Choose a CSV or Excel file",
    type=["csv", "xlsx", "xls"],
    help="File should contain student names and subject marks."
)

if uploaded_file is not None:
    df, error = load_file(uploaded_file)

    if error:
        st.error(f"❌ {error}")
    else:
        st.session_state.df = df
        st.success(f"✅ File uploaded successfully: `{uploaded_file.name}`")

# ── Display Raw Data ──────────────────────────────────────────────────────────
if st.session_state.df is not None:
    df = st.session_state.df

    st.header("🗂️ Raw Data Preview")

    # Metadata row
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Subjects Detected", df.shape[1] - 2)  # rough estimate

    # Column names
    st.markdown("**Columns in your file:**")
    st.write(list(df.columns))

    # Full data table
    st.dataframe(df, width='stretch')

    # Show sample data option
    if st.checkbox("Show only first 5 rows"):
        st.dataframe(df.head(), width='stretch')