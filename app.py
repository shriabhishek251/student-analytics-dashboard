import streamlit as st

# Page configuration — this must be the first Streamlit command
st.set_page_config(
    page_title="Student Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title and description
st.title("📊 Student Analytics Dashboard")
st.markdown("Upload your student marks data to get instant performance insights.")

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.info("Upload a file to get started.")

# Placeholder content
st.info("👆 File upload will appear here in Milestone 2.")