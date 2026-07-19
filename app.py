import streamlit as st
from src.ui.upload_page import upload_page
from src.ui.results_page import results_page

# Set page configuration
st.set_page_config(
    page_title="HireMe Agent",
    page_icon="💼",
    layout="centered"
)

# Initialize session state keys if not already set
if "stage" not in st.session_state:
    st.session_state.stage = "upload"
if "cv_data" not in st.session_state:
    st.session_state.cv_data = None
if "results" not in st.session_state:
    st.session_state.results = []
if "location" not in st.session_state:
    st.session_state.location = ""
if "count" not in st.session_state:
    st.session_state.count = 3
if "error" not in st.session_state:
    st.session_state.error = None
if "last_file" not in st.session_state:
    st.session_state.last_file = None

# Route to the correct page based on current stage value
if st.session_state.stage == "upload":
    upload_page()
elif st.session_state.stage == "results":
    results_page()
