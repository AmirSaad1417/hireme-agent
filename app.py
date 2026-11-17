import streamlit as st
from src.ui.styles import inject_styles
from src.ui.upload_page import upload_page
from src.ui.results_page import results_page

st.set_page_config(
    page_title="HireMe Agent",
    page_icon="💼",
    layout="centered",
)

# Apply global design system CSS
inject_styles()

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
if "exp_level" not in st.session_state:
    st.session_state.exp_level = "Auto-detect from CV"
if "selected_career_pill" not in st.session_state:
    st.session_state.selected_career_pill = "Auto-detect"

if st.session_state.stage == "upload":
    upload_page()
elif st.session_state.stage == "results":
    results_page()
