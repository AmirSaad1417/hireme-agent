import streamlit as st
from src.ui.upload_page import upload_page
from src.ui.results_page import results_page

# Set page configuration (must be called first)
st.set_page_config(
    page_title="HireMe Agent | AI Career Assistant",
    page_icon="💼",
    layout="wide"  # Changed to wide for premium split-screen dashboards
)

# Global UI Redesign: Injecting styles and custom fonts
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
    
    /* Global Styles */
    html, body, [data-testid="stAppViewContainer"] {
        background: radial-gradient(circle at 50% 50%, #151329 0%, #0d0c15 100%) !important;
        background-attachment: fixed !important;
        color: #f3f4f6 !important;
        font-family: 'Plus Jakarta Sans', 'Inter', sans-serif !important;
    }
    
    /* Hide Default Header/Footer */
    [data-testid="stHeader"] {
        background: transparent !important;
        backdrop-filter: none !important;
    }
    footer {visibility: hidden !important;}
    
    /* Floating Navbar styles */
    .floating-navbar {
        position: fixed;
        top: 15px;
        left: 50%;
        transform: translateX(-50%);
        width: 90%;
        max-width: 1000px;
        background: rgba(13, 12, 21, 0.7);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 40px;
        padding: 12px 30px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        z-index: 9999;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.6);
        transition: all 0.3s ease;
    }
    .nav-brand {
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-weight: 800;
        font-size: 18px;
        background: linear-gradient(135deg, #a78bfa 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 0.5px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .nav-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 11px;
        font-weight: 600;
        color: #06b6d4;
        background: rgba(6, 182, 212, 0.08);
        padding: 5px 14px;
        border-radius: 20px;
        border: 1px solid rgba(6, 182, 212, 0.2);
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #06b6d4;
        border-radius: 50%;
        box-shadow: 0 0 10px #06b6d4;
        animation: navPulse 1.8s infinite;
    }
    @keyframes navPulse {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(6, 182, 212, 0.7); }
        70% { transform: scale(1.1); box-shadow: 0 0 0 10px rgba(6, 182, 212, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(6, 182, 212, 0); }
    }
    
    /* Buffer spacer for top layout */
    .navbar-spacer {
        height: 70px;
    }
    </style>
""", unsafe_allow_html=True)

# Render floating glassmorphism navbar
st.markdown("""
    <div class="floating-navbar">
        <div class="nav-brand">✨ HIREME AGENT</div>
        <div class="nav-indicator">
            <span class="pulse-dot"></span>
            AI Career Engine Active
        </div>
    </div>
    <div class="navbar-spacer"></div>
""", unsafe_allow_html=True)

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
