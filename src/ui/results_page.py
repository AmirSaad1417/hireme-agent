import streamlit as st
import re
from src.memory.cv_store import get_cv, is_cv_loaded, clear_cv
from src.tools.job_search import search_adzuna_jobs

def results_page():
    # Custom CSS for the redesigned, premium results interface
    st.markdown("""
        <style>
        /* General layout & grid resets */
        .results-container {
            display: flex;
            gap: 30px;
            margin-top: 20px;
        }
        
        /* Profile Column glass card */
        .profile-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 25px;
            box-shadow: 0 15px 35px rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
        }
        .profile-avatar {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            background: linear-gradient(135deg, #a78bfa 0%, #6366f1 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 32px;
            margin: 0 auto 15px auto;
            box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4);
        }
        .profile-name {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 22px;
            font-weight: 800;
            text-align: center;
            color: #ffffff;
            margin-bottom: 5px;
        }
        .profile-email {
            font-size: 13px;
            color: #9ca3af;
            text-align: center;
            margin-bottom: 25px;
        }
        
        /* Stats & Score rings layout */
        .score-row {
            display: flex;
            justify-content: space-around;
            align-items: center;
            margin-bottom: 25px;
            background: rgba(0, 0, 0, 0.2);
            padding: 15px;
            border-radius: 12px;
            border: 1px solid rgba(255, 255, 255, 0.04);
        }
        .score-box {
            text-align: center;
        }
        .score-val {
            font-size: 24px;
            font-weight: 800;
            background: linear-gradient(135deg, #06b6d4, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .score-val.ats {
            background: linear-gradient(135deg, #10b981, #059669);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .score-label {
            font-size: 11px;
            font-weight: 600;
            color: #9ca3af;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 5px;
        }
        
        /* Categorized Skill Tag Pills */
        .skill-group-title {
            font-size: 12px;
            font-weight: 700;
            color: #818cf8;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-top: 15px;
            margin-bottom: 8px;
        }
        .skill-pill {
            display: inline-block;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid rgba(255, 255, 255, 0.08);
            color: #e5e7eb;
            padding: 4px 10px;
            border-radius: 15px;
            font-size: 12px;
            margin: 3px;
            transition: all 0.2s ease;
        }
        .skill-pill:hover {
            background: rgba(99, 102, 241, 0.15);
            border-color: #6366f1;
            color: #ffffff;
            transform: scale(1.05);
        }
        
        /* Accordion Insights styling */
        .insight-card {
            background: rgba(255, 255, 255, 0.02);
            border-radius: 10px;
            border-left: 4px solid #6366f1;
            padding: 12px 15px;
            margin-bottom: 12px;
        }
        .insight-card.strength { border-left-color: #10b981; }
        .insight-card.weakness { border-left-color: #f59e0b; }
        .insight-card.gap { border-left-color: #ef4444; }
        
        .insight-title {
            font-size: 13px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 6px;
            color: #ffffff;
        }
        .insight-text {
            font-size: 13px;
            color: #d1d5db;
            line-height: 1.4;
        }
        .insight-item {
            display: flex;
            align-items: flex-start;
            gap: 8px;
            margin-bottom: 6px;
            font-size: 13px;
            color: #d1d5db;
        }
        .insight-icon {
            font-size: 14px;
            flex-shrink: 0;
            margin-top: 1px;
        }
        
        /* Job Card Styling */
        .job-card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.06);
            border-radius: 16px;
            padding: 22px;
            margin-bottom: 20px;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            backdrop-filter: blur(5px);
        }
        .job-card:hover {
            border-color: rgba(99, 102, 241, 0.4);
            background: rgba(99, 102, 241, 0.02);
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.4);
            transform: translateY(-2px);
        }
        .job-header-row {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 15px;
            margin-bottom: 8px;
        }
        .job-title {
            font-family: 'Plus Jakarta Sans', sans-serif;
            font-size: 18px;
            font-weight: 700;
            color: #ffffff;
        }
        .match-badge {
            background: rgba(16, 185, 129, 0.1);
            border: 1px solid rgba(16, 185, 129, 0.3);
            color: #10b981;
            padding: 3px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
        }
        .job-meta-row {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            font-size: 13px;
            color: #9ca3af;
            margin-bottom: 12px;
        }
        .job-meta-item {
            display: flex;
            align-items: center;
            gap: 5px;
        }
        .job-desc {
            font-size: 13.5px;
            color: #d1d5db;
            line-height: 1.5;
            margin-bottom: 18px;
        }
        
        /* Pill badges for salary / remote */
        .badge-salary {
            background: rgba(16, 185, 129, 0.1);
            color: #10b981;
            border: 1px solid rgba(16, 185, 129, 0.2);
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 600;
        }
        .badge-type {
            background: rgba(6, 182, 212, 0.1);
            color: #06b6d4;
            border: 1px solid rgba(6, 182, 212, 0.2);
            padding: 2px 8px;
            border-radius: 4px;
            font-weight: 600;
        }
        
        /* Direct Action Button */
        .apply-btn {
            background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
            color: #ffffff;
            border: none;
            padding: 8px 18px;
            border-radius: 8px;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            box-shadow: 0 4px 10px rgba(99, 102, 241, 0.3);
            transition: all 0.2s ease;
        }
        .apply-btn:hover {
            box-shadow: 0 6px 15px rgba(99, 102, 241, 0.45);
            transform: scale(1.02);
            color: #ffffff;
        }
        </style>
    """, unsafe_allow_html=True)

    # State restoration logic
    if not st.session_state.cv_data and is_cv_loaded():
        st.session_state.cv_data = get_cv()

    # Route back to upload if empty
    if not st.session_state.cv_data:
        st.warning("⚠️ No parsed candidate profile is currently cached. Please upload a CV first.")
        if st.button("Go to Uploader Page"):
            st.session_state.stage = "upload"
            st.rerun()
        return

    cv = st.session_state.cv_data

    # Layout split: Left (Candidate Card) & Right (Recommendations)
    col_profile, col_jobs = st.columns([1, 2], gap="large")

    with col_profile:
        # Profile header card
        st.markdown(f"""
            <div class="profile-card">
                <div class="profile-avatar">👨‍💻</div>
                <div class="profile-name">{cv.get('name', 'Candidate')}</div>
                <div class="profile-email">✉️ {cv.get('email', 'No email identified')}</div>
                
                <!-- Scores Row -->
                <div class="score-row">
                    <div class="score-box">
                        <div class="score-val">{cv.get('career_score', 80)}%</div>
                        <div class="score-label">Match Score</div>
                    </div>
                    <div class="score-box" style="border-left: 1px solid rgba(255,255,255,0.1); padding-left: 20px;">
                        <div class="score-val ats">{cv.get('ats_score', 85)}%</div>
                        <div class="score-label">ATS Rank</div>
                    </div>
                </div>
                
                <p style="font-size: 14px; line-height: 1.5; color: #d1d5db; margin-bottom: 20px;">
                    <strong>Overview:</strong><br>
                    <span style="font-size: 13px; color: #9ca3af;">{cv.get('summary', '')}</span>
                </p>
            </div>
        """, unsafe_allow_html=True)

        # Categorized Skills Tags
        st.markdown("<h4 style='margin-top:20px; font-weight:700;'>Categorized Skills</h4>", unsafe_allow_html=True)
        categories = cv.get("skill_categories", {})
        
        if categories and isinstance(categories, dict):
            for cat_name, cat_skills in categories.items():
                if cat_skills:
                    st.markdown(f"<div class='skill-group-title'>{cat_name}</div>", unsafe_allow_html=True)
                    pills_html = "".join([f'<span class="skill-pill">{s}</span>' for s in cat_skills])
                    st.markdown(f"<div>{pills_html}</div>", unsafe_allow_html=True)
        else:
            # Fallback to standard key_skills if not categorized
            st.markdown("<div class='skill-group-title'>Core Technologies</div>", unsafe_allow_html=True)
            pills_html = "".join([f'<span class="skill-pill">{s}</span>' for s in cv.get('key_skills', [])])
            st.markdown(f"<div>{pills_html}</div>", unsafe_allow_html=True)

        # AI Career Insights Card Accordion
        st.markdown("<h4 style='margin-top:25px; font-weight:700;'>AI Career Insights</h4>", unsafe_allow_html=True)
        
        # Strengths Card
        strengths = cv.get("strengths", ["Strong programming background", "Good core problem solving"])
        st.markdown(f"""
            <div class="insight-card strength">
                <div class="insight-title">💪 Top Strengths</div>
                {"".join([f'<div class="insight-item"><span class="insight-icon">✓</span>{item}</div>' for item in strengths])}
            </div>
        """, unsafe_allow_html=True)

        # Weaknesses / Development Areas Card
        weaknesses = cv.get("weaknesses", ["Expand cloud certifications"])
        st.markdown(f"""
            <div class="insight-card weakness">
                <div class="insight-title">⚠️ Growth Areas</div>
                {"".join([f'<div class="insight-item"><span class="insight-icon">⚠</span>{item}</div>' for item in weaknesses])}
            </div>
        """, unsafe_allow_html=True)

        # Skill Gaps Card
        gaps = cv.get("skill_gaps", [])
        if gaps:
            st.markdown(f"""
                <div class="insight-card gap">
                    <div class="insight-title">🎯 Identified Skill Gaps</div>
                    {"".join([f'<div class="insight-item"><span class="insight-icon">✗</span>{item}</div>' for item in gaps])}
                </div>
            """, unsafe_allow_html=True)

        # Career advice Card
        advice = cv.get("career_advice", "")
        if advice:
            st.markdown(f"""
                <div class="insight-card" style="border-left-color: #06b6d4;">
                    <div class="insight-title">💡 Strategic Career Tip</div>
                    <div class="insight-text">{advice}</div>
                </div>
            """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        
        # Reset/Restart Page
        if st.button("🔄 Restart & Parse New CV", use_container_width=True):
            clear_cv()
            st.session_state.cv_data = None
            st.session_state.results = []
            st.session_state.location = ""
            st.session_state.count = 3
            st.session_state.error = None
            st.session_state.last_file = None
            st.session_state.stage = "upload"
            st.rerun()

    with col_jobs:
        st.markdown("<h3 style='margin-top:0; font-weight:800; font-family:Plus Jakarta Sans;'>Job Match Center</h3>", unsafe_allow_html=True)

        # Define supported countries dictionary
        country_options = {
            "United Kingdom 🇬🇧": "gb",
            "United States 🇺🇸": "us",
            "Canada 🇨🇦": "ca",
            "India 🇮🇳": "in",
            "Germany 🇩🇪": "de",
            "Australia 🇦🇺": "au",
            "Singapore 🇸🇬": "sg",
            "South Africa 🇿🇦": "za",
            "France 🇫🇷": "fr"
        }

        # Filter Panel (Glassmorphism layout container)
        default_role = cv.get('target_roles', ["Software Engineer"])[0] if cv.get('target_roles') else "Software Engineer"
        
        # If candidate is Junior and query is default, adjust query to search for "Junior" roles
        exp_level = cv.get("experience_level", "Junior")
        if exp_level.lower() == "junior" and default_role.lower() == "software engineer":
            default_role = "Junior Software Engineer"

        with st.expander("🔍 Adjust Search Query & Global Location", expanded=True):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                role_query = st.text_input("Target Job Title Query", value=default_role)
                location_query = st.text_input("City/Region Filter", value=st.session_state.location)
                st.session_state.location = location_query
            with f_col2:
                # Country Selector! Dynamic global searching
                country_name = st.selectbox("Search Country Database", list(country_options.keys()), index=0)
                selected_country_code = country_options[country_name]
                
                results_count = st.number_input("Maximum Matches to Display", min_value=1, max_value=10, value=st.session_state.count)
                st.session_state.count = results_count
                
            trigger_search = st.button("Query Global Job Markets 🚀", use_container_width=True)

        # Execute Search automatically or on filter trigger
        if trigger_search or not st.session_state.results:
            with st.spinner("Searching matching jobs globally..."):
                try:
                    jobs = search_adzuna_jobs(
                        query=role_query,
                        location=st.session_state.location,
                        count=st.session_state.count,
                        country=selected_country_code
                    )
                    
                    # Core Experience Alignment Filter
                    # If Junior, filter out titles matching Senior Keywords (Director, Manager, Lead, Senior)
                    if exp_level.lower() == "junior":
                        filtered_jobs = []
                        for job in jobs:
                            title_lower = job["title"].lower()
                            senior_keywords = ["senior", "lead", "manager", "director", "head of", "principal", "sr.", "sr "]
                            if not any(kw in title_lower for kw in senior_keywords):
                                filtered_jobs.append(job)
                        st.session_state.results = filtered_jobs
                    else:
                        st.session_state.results = jobs
                        
                except Exception as e:
                    st.error(f"Failed to query job listings: {str(e)}")
                    st.session_state.results = []

        # Display Recomendation List
        if st.session_state.results:
            st.write(f"Displaying top {len(st.session_state.results)} personalized matches based on experience level ({exp_level}):")
            
            for index, job in enumerate(st.session_state.results):
                # Calculate matching percentage
                # Base is 85%, add/subtract based on keywords matching skills
                match_percentage = 85
                title_lower = job.get("title", "").lower()
                desc_lower = job.get("description", "").lower()
                
                # Check skill overlaps to adjust match percentage
                matched_count = 0
                for skill in cv.get("key_skills", []):
                    if skill.lower() in title_lower or skill.lower() in desc_lower:
                        matched_count += 1
                
                match_percentage += min(matched_count * 2, 14) # max 99%
                
                # Format Salary
                sal_min = job.get("salary_min")
                sal_max = job.get("salary_max")
                salary_html = ""
                
                # Deduce currency based on selected country
                currency_symbol = "£"
                if selected_country_code in ["us", "ca", "sg", "au"]:
                    currency_symbol = "$"
                elif selected_country_code in ["in"]:
                    currency_symbol = "₹"
                elif selected_country_code in ["de", "fr"]:
                    currency_symbol = "€"
                elif selected_country_code in ["za"]:
                    currency_symbol = "R"
                
                if sal_min and sal_max:
                    salary_html = f'<span class="badge-salary">{currency_symbol}{int(sal_min):,} - {currency_symbol}{int(sal_max):,}</span>'
                elif sal_min:
                    salary_html = f'<span class="badge-salary">{currency_symbol}{int(sal_min):,}+</span>'
                    
                # Deduce job type badge (remote / hybrid / office)
                type_html = ""
                full_text = title_lower + " " + desc_lower
                if "remote" in full_text or "work from home" in full_text or "wfh" in full_text:
                    type_html = '<span class="badge-type">🌐 Remote</span>'
                elif "hybrid" in full_text or "flexible work" in full_text:
                    type_html = '<span class="badge-type">🏢 Hybrid</span>'
                else:
                    type_html = '<span class="badge-type">📍 On-site</span>'

                # Strip HTML from description
                clean_desc = re.sub('<[^<]+?>', '', job.get('description', ''))
                if len(clean_desc) > 220:
                    clean_desc = clean_desc[:220].strip() + "..."

                # Render Card
                st.markdown(f"""
                    <div class="job-card">
                        <div class="job-header-row">
                            <div class="job-title">{job.get('title')}</div>
                            <div class="match-badge">{match_percentage}% Match</div>
                        </div>
                        <div class="job-meta-row">
                            <div class="job-meta-item">🏢 <strong>{job.get('company')}</strong></div>
                            <div class="job-meta-item">📍 {job.get('location')}</div>
                            <div class="job-meta-item">{salary_html}</div>
                            <div class="job-meta-item">{type_html}</div>
                        </div>
                        <div class="job-desc">{clean_desc}</div>
                        <a href="{job.get('url')}" target="_blank" style="text-decoration:none;">
                            <div class="apply-btn">
                                View Job Details & Apply 🚀
                            </div>
                        </a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.info("ℹ️ No jobs matched your profile. Try modifying the job title query, location, or changing the country database.")
