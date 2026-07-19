import streamlit as st
import re
from src.memory.cv_store import get_cv, is_cv_loaded, clear_cv
from src.tools.job_search import search_adzuna_jobs

def results_page():
    # Custom CSS for premium UI styling
    st.markdown("""
        <style>
        .profile-container {
            background-color: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }
        .profile-header {
            font-size: 24px;
            font-weight: bold;
            color: #ff4b4b;
            margin-bottom: 10px;
        }
        .profile-sub {
            font-size: 14px;
            color: #888;
            margin-bottom: 15px;
        }
        .skill-pill {
            display: inline-block;
            background-color: rgba(255, 75, 75, 0.15);
            color: #ff4b4b;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 12px;
            margin: 3px;
            border: 1px solid rgba(255, 75, 75, 0.3);
        }
        .job-card {
            background-color: rgba(255, 255, 255, 0.04);
            border-radius: 8px;
            padding: 18px;
            margin-bottom: 15px;
            border: 1px solid rgba(255, 255, 255, 0.08);
            transition: all 0.3s ease;
        }
        .job-card:hover {
            border-color: #ff4b4b;
            background-color: rgba(255, 255, 255, 0.06);
            transform: translateY(-2px);
        }
        .job-title {
            font-size: 18px;
            font-weight: bold;
            color: #ff4b4b;
            margin-bottom: 5px;
        }
        .job-meta {
            font-size: 13px;
            color: #aaa;
            margin-bottom: 10px;
        }
        .job-desc {
            font-size: 14px;
            color: #ddd;
            margin-bottom: 12px;
            line-height: 1.4;
        }
        .salary-badge {
            background-color: rgba(46, 204, 113, 0.15);
            color: #2ecc71;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: bold;
            display: inline-block;
            margin-right: 10px;
        }
        </style>
    """, unsafe_allow_html=True)

    # Recovery: restore CV from cv_store if session state is cleared
    if not st.session_state.cv_data and is_cv_loaded():
        st.session_state.cv_data = get_cv()

    # If no CV data is loaded, redirect to upload
    if not st.session_state.cv_data:
        st.warning("⚠️ No CV profile is loaded. Please upload a CV first.")
        if st.button("Go to Upload Page"):
            st.session_state.stage = "upload"
            st.rerun()
        return

    cv = st.session_state.cv_data

    # Layout: Split into Profile Card and Job Matches
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("<h3 style='margin-top:0;'>Candidate Profile</h3>", unsafe_allow_html=True)
        
        # Profile Details Box
        with st.container():
            st.markdown(f"""
                <div class="profile-container">
                    <div class="profile-header">{cv.get('name', 'Unknown Candidate')}</div>
                    <div class="profile-sub">✉️ {cv.get('email', 'No email found')}</div>
                    <p><strong>Experience Level:</strong> {cv.get('experience_level', 'Not specified')}</p>
                    <p><strong>Professional Summary:</strong><br><span style="font-size: 13px; color:#ccc;">{cv.get('summary', '')}</span></p>
                </div>
            """, unsafe_allow_html=True)

            # Target Skills pills
            st.markdown("**Top Skills:**")
            skills_html = "".join([f'<span class="skill-pill">{skill}</span>' for skill in cv.get('key_skills', [])])
            st.markdown(f"<div>{skills_html}</div><br>", unsafe_allow_html=True)

            # Restart/Upload Button
            if st.button("🔄 Restart & Upload New CV", use_container_width=True):
                clear_cv()
                st.session_state.cv_data = None
                st.session_state.results = []
                st.session_state.location = ""
                st.session_state.count = 3
                st.session_state.error = None
                st.session_state.last_file = None
                st.session_state.stage = "upload"
                st.rerun()

    with col2:
        st.markdown("<h3 style='margin-top:0;'>Job Recommendations</h3>", unsafe_allow_html=True)
        
        # Search Filters Box
        default_role = cv.get('target_roles', ["Software Engineer"])[0] if cv.get('target_roles') else "Software Engineer"
        
        with st.expander("🔍 Adjust Search Query & Filters", expanded=True):
            role_query = st.text_input("Job Title / Role Query", value=default_role)
            
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                location_query = st.text_input("Location Filter (City/Region)", value=st.session_state.location)
                st.session_state.location = location_query
            with f_col2:
                results_count = st.number_input("Max Results to Fetch", min_value=1, max_value=10, value=st.session_state.count)
                st.session_state.count = results_count
                
            trigger_search = st.button("Search Jobs 🚀", use_container_width=True)

        # Trigger search automatically on first load or when "Search Jobs" is clicked
        if trigger_search or not st.session_state.results:
            with st.spinner("Searching matching jobs via Adzuna..."):
                try:
                    # Run search
                    jobs = search_adzuna_jobs(
                        query=role_query,
                        location=st.session_state.location,
                        count=st.session_state.count
                    )
                    st.session_state.results = jobs
                except Exception as e:
                    st.error(f"Failed to fetch jobs: {str(e)}")
                    st.session_state.results = []

        # Display matched jobs
        if st.session_state.results:
            st.write(f"Showing top {len(st.session_state.results)} matches:")
            for job in st.session_state.results:
                # Helper to format salary
                sal_min = job.get("salary_min")
                sal_max = job.get("salary_max")
                salary_str = ""
                if sal_min and sal_max:
                    salary_str = f'<span class="salary-badge">£{int(sal_min):,} - £{int(sal_max):,}</span>'
                elif sal_min:
                    salary_str = f'<span class="salary-badge">£{int(sal_min):,}+</span>'
                
                # HTML template for job recommendation card
                clean_desc = re.sub('<[^<]+?>', '', job.get('description', '')) # strip HTML
                if len(clean_desc) > 200:
                    clean_desc = clean_desc[:200] + "..."
                    
                st.markdown(f"""
                    <div class="job-card">
                        <div class="job-title">{job.get('title')}</div>
                        <div class="job-meta">
                            🏢 <strong>{job.get('company')}</strong> &nbsp;|&nbsp; 📍 {job.get('location')} &nbsp;|&nbsp; {salary_str}
                        </div>
                        <div class="job-desc">{clean_desc}</div>
                        <a href="{job.get('url')}" target="_blank" style="text-decoration:none;">
                            <button style="
                                background-color:#ff4b4b; 
                                color:white; 
                                border:none; 
                                padding:6px 12px; 
                                border-radius:4px; 
                                font-size:13px;
                                cursor:pointer;
                                font-weight:bold;
                            ">
                                View Job Details & Apply ↗
                            </button>
                        </a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ No matching jobs found. Try adjusting your search queries or changing filters.")
