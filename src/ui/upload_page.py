import streamlit as st
import time
import textwrap
from src.parsers.cv_extractor import extract_cv_text
from src.parsers.cv_parser import parse_cv_text_with_ai
from src.memory.cv_store import save_cv

def upload_page():
    # Custom CSS for modern uploader and timeline aesthetics
    st.markdown("""
        <style>
        /* Hero title styling */
        .hero-title {
            text-align: center;
            font-size: 38px;
            font-weight: 800;
            margin-bottom: 8px;
            font-family: 'Plus Jakarta Sans', sans-serif;
            background: linear-gradient(135deg, #a78bfa 0%, #3b82f6 50%, #06b6d4 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .hero-subtitle {
            text-align: center;
            font-size: 16px;
            color: #9ca3af;
            margin-bottom: 40px;
        }
        
        /* Glassmorphism dropzone styling */
        .dropzone-container {
            background: rgba(255, 255, 255, 0.03);
            border: 2px dashed rgba(167, 139, 250, 0.3);
            border-radius: 20px;
            padding: 40px 30px;
            text-align: center;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            margin-bottom: 30px;
        }
        .dropzone-container:hover {
            border-color: #6366f1;
            background: rgba(99, 102, 241, 0.05);
            box-shadow: 0 15px 35px rgba(99, 102, 241, 0.15);
            transform: translateY(-2px);
        }
        .upload-icon {
            font-size: 55px;
            margin-bottom: 15px;
            animation: bounce 2s infinite;
        }
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
        
        /* Guide step cards */
        .guide-container {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 20px;
            margin-top: 20px;
        }
        .guide-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.05);
            border-radius: 12px;
            padding: 20px;
            transition: all 0.3s ease;
        }
        .guide-card:hover {
            background: rgba(255, 255, 255, 0.04);
            border-color: rgba(99, 102, 241, 0.2);
        }
        .guide-num {
            font-size: 12px;
            font-weight: 700;
            color: #818cf8;
            text-transform: uppercase;
            margin-bottom: 8px;
            letter-spacing: 1px;
        }
        .guide-title {
            font-size: 15px;
            font-weight: 600;
            color: #f3f4f6;
            margin-bottom: 5px;
        }
        .guide-desc {
            font-size: 13px;
            color: #9ca3af;
            line-height: 1.4;
        }
        
        /* Timeline processing animation styles */
        .timeline-box {
            background: rgba(13, 12, 21, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 30px;
            max-width: 600px;
            margin: 0 auto;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
            backdrop-filter: blur(15px);
        }
        .timeline-title {
            font-size: 18px;
            font-weight: 700;
            margin-bottom: 25px;
            text-align: center;
            background: linear-gradient(90deg, #6366f1, #06b6d4);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .step-row {
            display: flex;
            align-items: flex-start;
            margin-bottom: 20px;
            opacity: 0.3;
            transition: all 0.4s ease;
        }
        .step-row.completed {
            opacity: 1;
        }
        .step-row.active {
            opacity: 1;
        }
        .step-bullet {
            width: 28px;
            height: 28px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            margin-right: 15px;
            border: 2px solid rgba(255, 255, 255, 0.2);
            background: #111827;
            flex-shrink: 0;
            transition: all 0.3s ease;
        }
        .step-row.completed .step-bullet {
            background: rgba(16, 185, 129, 0.15);
            border-color: #10b981;
            color: #10b981;
        }
        .step-row.active .step-bullet {
            background: rgba(6, 182, 212, 0.15);
            border-color: #06b6d4;
            color: #06b6d4;
            box-shadow: 0 0 10px rgba(6, 182, 212, 0.4);
            animation: pulse-border 1.5s infinite;
        }
        @keyframes pulse-border {
            0% { transform: scale(0.95); }
            50% { transform: scale(1.05); }
            100% { transform: scale(0.95); }
        }
        .step-info {
            flex-grow: 1;
        }
        .step-text {
            font-size: 14px;
            font-weight: 500;
            color: #e5e7eb;
        }
        .step-status {
            font-size: 11px;
            color: #9ca3af;
            margin-top: 3px;
        }
        .step-row.completed .step-status {
            color: #10b981;
        }
        .step-row.active .step-status {
            color: #06b6d4;
            font-weight: 600;
        }
        </style>
    """, unsafe_allow_html=True)

    # Hero Banner
    st.markdown("<h1 class='hero-title'>AI Career Assistant</h1>", unsafe_allow_html=True)
    st.markdown("<p class='hero-subtitle'>Let personal intelligence evaluate your path and match you with global job opportunities.</p>", unsafe_allow_html=True)

    # Error handling
    if st.session_state.error:
        st.error(f"⚠️ **Parsing Error:** {st.session_state.error}")
        if st.button("Clear Cache & Try Again"):
            st.session_state.error = None
            st.session_state.last_file = None
            st.rerun()

    # Form Centering Container
    col_center, _ = st.columns([8, 1]) # Shift slightly right for centered layout
    with col_center:
        # File uploader widget inside a visually formatted dropzone container
        uploaded_file = st.file_uploader(
            "Choose a file", 
            type=["pdf", "docx"],
            label_visibility="collapsed" # Hide standard label to use our custom header
        )

        if not uploaded_file:
            # Custom styled Drop Zone if empty
            st.markdown(textwrap.dedent("""
                <div class="dropzone-container">
                    <div class="upload-icon">📤</div>
                    <h3 style="margin-top: 0; font-size: 20px; font-weight: 700; color: #f3f4f6;">Drag and drop your CV here</h3>
                    <p style="color: #9ca3af; font-size: 14px; margin-bottom: 5px;">Accepts PDF (.pdf) and Word (.docx) files</p>
                    <p style="color: #6366f1; font-size: 12px; font-weight: 600;">Max size: 10MB</p>
                </div>
            """), unsafe_allow_html=True)
            
            # Guidelines Cards
            st.markdown("<div class='guide-container'>", unsafe_allow_html=True)
            st.markdown(textwrap.dedent("""
                <div class="guide-card">
                    <div class="guide-num">Step 01</div>
                    <div class="guide-title">Upload Profile</div>
                    <div class="guide-desc">Upload your latest CV. We support formatted text parsing for PDFs and Word docs.</div>
                </div>
                <div class="guide-card">
                    <div class="guide-num">Step 02</div>
                    <div class="guide-title">AI Processing</div>
                    <div class="guide-desc">The model analyzes your skills, experiences, and assigns custom ATS readiness scores.</div>
                </div>
                <div class="guide-card">
                    <div class="guide-num">Step 03</div>
                    <div class="guide-title">Search Jobs</div>
                    <div class="guide-desc">Instantly query active job boards globally to match with direct job recommenders.</div>
                </div>
            """), unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        else:
            # File is uploaded! Begin animated processing timeline.
            file_id = f"{uploaded_file.name}_{uploaded_file.size}"
            
            if st.session_state.last_file != file_id:
                # Placeholder to render the timeline updates
                timeline_placeholder = st.empty()
                
                # Definitions of steps in the timeline
                steps = [
                    ("📄", "Reading CV binary document from upload stream..."),
                    ("📖", "Extracting raw structured text content..."),
                    ("🧠", "Analyzing experience depth & mapping career seniority..."),
                    ("💡", "Categorizing skills, frameworks, and specialized domains..."),
                    ("📈", "Evaluating ATS formatting score & resume layout..."),
                    ("🎯", "Generating candidate summary and target roles profile...")
                ]
                
                try:
                    # Helper function to render current state of the timeline
                    def render_timeline(active_idx):
                        html_content = '<div class="timeline-box">'
                        html_content += '<div class="timeline-title">🤖 Personal AI Advisor Processing</div>'
                        for i, (icon, desc) in enumerate(steps):
                            if i < active_idx:
                                status = "Completed"
                                css_class = "completed"
                                bullet = "✓"
                            elif i == active_idx:
                                status = "Processing..."
                                css_class = "active"
                                bullet = icon
                            else:
                                status = "Pending"
                                css_class = "pending"
                                bullet = icon
                            
                            html_content += f"""
                                <div class="step-row {css_class}">
                                    <div class="step-bullet">{bullet}</div>
                                    <div class="step-info">
                                        <div class="step-text">{desc}</div>
                                        <div class="step-status">{status}</div>
                                    </div>
                                </div>
                            """
                        html_content += '</div>'
                        timeline_placeholder.markdown(html_content, unsafe_allow_html=True)

                    # Step 0: Reading CV document
                    render_timeline(0)
                    time.sleep(0.8)
                    file_bytes = uploaded_file.read()
                    
                    # Step 1: Extract text
                    render_timeline(1)
                    raw_text = extract_cv_text(uploaded_file.name, file_bytes)
                    time.sleep(0.8)
                    if not raw_text.strip():
                        raise ValueError("The uploaded CV contains no text elements or is a scanned image scan.")

                    # Step 2: Analyzing experience level (Initiating Groq)
                    render_timeline(2)
                    time.sleep(0.6)
                    
                    # Step 3: Categorizing skills (Making the actual Groq API call)
                    render_timeline(3)
                    cv_data = parse_cv_text_with_ai(raw_text)
                    
                    # Step 4: Evaluating ATS Score
                    render_timeline(4)
                    time.sleep(0.8)
                    
                    # Step 5: Generating target roles profile
                    render_timeline(5)
                    time.sleep(0.8)
                    
                    # Save parsed results
                    save_cv(cv_data)
                    st.session_state.cv_data = cv_data
                    st.session_state.last_file = file_id
                    st.session_state.error = None
                    st.session_state.stage = "results"
                    
                    # Force final refresh and route
                    st.rerun()

                except Exception as e:
                    st.session_state.error = str(e)
                    st.session_state.last_file = None
                    st.rerun()
