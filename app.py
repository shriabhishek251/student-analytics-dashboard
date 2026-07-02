# app.py
import pandas as pd
import streamlit as st
from modules.loader import load_file
from modules.cleaner import clean_data
from modules.metrics import compute_metrics
from modules.subject_analysis import analyse_subjects
from modules.student_insights import get_toppers, get_at_risk_students

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
if "subject_df" not in st.session_state:
    st.session_state.subject_df = None
if "subject_insights" not in st.session_state:
    st.session_state.subject_insights = None
if "toppers" not in st.session_state:
    st.session_state.toppers = None
if "at_risk" not in st.session_state:
    st.session_state.at_risk = None

# ── Header ─────────────────────────────────────────────────────────────────────
st.title("📊 Student Analytics Dashboard")
st.markdown("Upload your student marks data to get instant performance insights.")

st.sidebar.title("Navigation")
st.sidebar.markdown("**Step 1:** Upload your file below.")
st.sidebar.markdown("---")
st.sidebar.subheader("⚙️ Settings")

n_toppers = st.sidebar.slider(
    "Number of toppers to show", 
    min_value=1, max_value=10, value=3
)
risk_threshold = st.sidebar.slider(
    "At-risk threshold (%)", 
    min_value=30, max_value=70, value=50
)

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
        subject_df, subject_insights = analyse_subjects(df_clean, marks_cols)
        
        toppers = get_toppers(summary, n=n_toppers)
        at_risk = get_at_risk_students(summary, df_clean, marks_cols, threshold=risk_threshold)

        st.session_state.toppers = toppers
        st.session_state.at_risk = at_risk
        st.session_state.subject_df = subject_df
        st.session_state.subject_insights = subject_insights
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

# ── Subject-wise Analysis ──────────────────────────────────────────────────────
if st.session_state.subject_df is not None:
    st.header("📚 Subject-wise Analysis")

    insights = st.session_state.subject_insights

    # Insight callouts
    col1, col2 = st.columns(2)
    col1.success(
        f"🏆 Strongest Subject: **{insights['best_subject']}** "
        f"({insights['best_avg']}% avg)"
    )
    col2.error(
        f"⚠️ Weakest Subject: **{insights['worst_subject']}** "
        f"({insights['worst_avg']}% avg)"
    )

    # Subjects needing attention
    if insights["needs_attention"]:
        st.warning(
            f"🔴 Subjects where fewer than 50% of students passed: "
            f"{', '.join(insights['needs_attention'])}"
        )
    else:
        st.info("✅ All subjects have a pass rate above 50%.")

    # Subject summary table
    st.subheader("Subject Performance Breakdown")
    st.dataframe(st.session_state.subject_df, width='stretch')

# ── Toppers ────────────────────────────────────────────────────────────────────
if st.session_state.toppers is not None:
    st.header("🏆 Top Performers")

    toppers = st.session_state.toppers
    cols = st.columns(len(toppers))

    for i, (_, student) in enumerate(toppers.iterrows()):
        medal = ["🥇", "🥈", "🥉"][i] if i < 3 else f"#{i+1}"
        cols[i].metric(
            label=f"{medal} {student.get('name', 'Student')}",
            value=f"{student['percentage']}%",
            delta=f"Grade {student['grade']}"
        )

    with st.expander("See full topper details"):
        st.dataframe(toppers, width='stretch')

# ── At-Risk Students ───────────────────────────────────────────────────────────
if st.session_state.at_risk is not None:
    st.header("⚠️ At-Risk Students")

    at_risk = st.session_state.at_risk

    if at_risk.empty:
        st.success("✅ No at-risk students detected.")
    else:
        st.warning(
            f"⚠️ {len(at_risk)} student(s) flagged as at-risk. "
            f"Review and consider intervention."
        )
        st.dataframe(at_risk, width='stretch')