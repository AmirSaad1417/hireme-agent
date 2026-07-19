import streamlit as st
from src.parsers.cv_extractor import extract_cv_text
from src.parsers.cv_parser import parse_cv_text_with_ai
from src.memory.cv_store import save_cv

def upload_page():
    # Custom CSS for high-quality card layout and styling
    st.markdown("""
        <style>
        .upload-header {
            text-align: center;
            padding: 10px 0px 20px 0px;
        }
        .upload-logo {
            font-size: 50px;
            text-align: center;
            margin-bottom: 10px;
        }
        .info-card {
            background-color: rgba(255, 255, 255, 0.05);
            border-left: 5px solid #ff4b4b;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='upload-logo'>💼</div>", unsafe_allow_html=True)
    st.markdown("<h2 class='upload-header'>Smart CV & Job Matcher</h2>", unsafe_allow_html=True)
    
    st.markdown("""
        <div class='info-card'>
            <strong>How it works:</strong><br>
            1. Upload your resume in PDF or Word (.docx) format.<br>
            2. Our AI will automatically analyze your skills, experience level, and target roles.<br>
            3. We will query job markets to match you with live job openings!
        </div>
    """, unsafe_allow_html=True)

    # Show last error if any
    if st.session_state.error:
        st.error(f"⚠️ **Last parsing error:** {st.session_state.error}")
        if st.button("Clear Error"):
            st.session_state.error = None
            st.rerun()

    # Upload file widget
    uploaded_file = st.file_uploader(
        "Drag and drop your CV here", 
        type=["pdf", "docx"],
        help="Supported formats: PDF (.pdf) and Word (.docx)"
    )

    if uploaded_file is not None:
        # Create a unique identifier for the uploaded file
        file_id = f"{uploaded_file.name}_{uploaded_file.size}"
        
        if st.session_state.last_file != file_id:
            st.info("🔄 File uploaded successfully! Initiating processing...")
            
            try:
                # Read bytes
                file_bytes = uploaded_file.read()
                
                # 1. Extract text from document
                with st.spinner("📖 Extracting text from CV..."):
                    raw_text = extract_cv_text(uploaded_file.name, file_bytes)
                
                if not raw_text.strip():
                    raise ValueError("The uploaded file appears to have no text content. Scanned images are not supported.")

                # 2. Parse text with Groq LLM
                with st.spinner("🤖 Analyzing skills and career goals with Groq AI..."):
                    cv_data = parse_cv_text_with_ai(raw_text)
                
                # 3. Store the structured CV profile
                save_cv(cv_data)
                
                # 4. Save to session state
                st.session_state.cv_data = cv_data
                st.session_state.last_file = file_id
                st.session_state.error = None
                st.session_state.stage = "results"
                
                st.success("✅ CV successfully parsed! Redirecting to matches...")
                st.rerun()

            except Exception as e:
                st.session_state.error = str(e)
                st.error(f"❌ Failed to process CV: {str(e)}")
                st.rerun()
