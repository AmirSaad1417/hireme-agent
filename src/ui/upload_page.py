"""
Upload and search configuration page for HireMe Agent.
Implements a guided 3-step workflow (Upload -> Verify -> Search)
with interactive pills, career tier selector, and live progress state.
"""

import time
from typing import Dict
import streamlit as st

from src.agents import run_agent
from src.parsers import ingest_cv
from src.ui.components import show_cv_summary, show_error, show_header, show_step_header

COUNTRY_MAP: Dict[str, str] = {
    "United Kingdom (UK)": "gb",
    "United States (US)": "us",
    "Canada": "ca",
    "Germany": "de",
    "Australia": "au",
    "India": "in",
    "South Africa": "za",
    "France": "fr",
    "Netherlands": "nl",
}

EXP_PILLS = [
    "Auto-detect",
    "Internship / Student",
    "Junior / Fresh",
    "Mid-Level",
    "Senior / Lead",
]

PILL_TO_LEVEL = {
    "Auto-detect": "Auto-detect from CV",
    "Internship / Student": "Internship / Student",
    "Junior / Fresh": "Fresh Graduate / Entry Level",
    "Mid-Level": "Mid-Level (3-5 years)",
    "Senior / Lead": "Senior (5+ years)",
}

LEVEL_TO_PILL = {v: k for k, v in PILL_TO_LEVEL.items()}


def show_upload_page() -> None:
    """Render the upload and search preferences page following the 3-step SaaS workflow."""
    has_cv = st.session_state.get("cv_data") is not None
    current_step = 2 if has_cv else 1

    show_header(current_step=current_step)
    show_error()

    # -------------------------------------------------------------------------
    # STEP 1: Upload CV
    # -------------------------------------------------------------------------
    show_step_header(
        1,
        "Upload Your CV",
        "Upload your resume in PDF (.pdf) or Word (.docx) format to extract your skills and experience.",
    )

    uploaded_file = st.file_uploader(
        "Upload your resume",
        type=["pdf", "docx"],
        help="Supported formats: PDF (.pdf) and Word documents (.docx).",
        label_visibility="collapsed",
    )

    # Automatic parsing when a new file is uploaded
    if uploaded_file is not None:
        last_file = st.session_state.get("last_file")
        if last_file != uploaded_file.name:
            with st.status("Analyzing CV & Extracting Profile...", expanded=True) as status:
                status.write("Reading document text...")
                time.sleep(0.2)
                status.write("Extracting skills, career history, and education...")
                try:
                    cv_data = ingest_cv(uploaded_file)
                    st.session_state.cv_data = cv_data
                    st.session_state.last_file = uploaded_file.name
                    if cv_data.get("location") and not st.session_state.get("location"):
                        st.session_state.location = cv_data.get("location")
                    st.session_state.error = None
                    st.rerun()
                except Exception as err:
                    status.update(label="Failed to parse CV", state="error", expanded=True)
                    st.session_state.error = f"Failed to parse CV: {err}"
                    st.session_state.last_file = uploaded_file.name
                    st.session_state.cv_data = None
                    st.rerun()

    cv_data = st.session_state.get("cv_data")

    # -------------------------------------------------------------------------
    # STEP 2: Verify Extracted Profile
    # -------------------------------------------------------------------------
    show_step_header(
        2,
        "Verify Extracted Profile",
        "Confirm your detected career level and extracted skills before starting your search.",
    )

    if cv_data:
        show_cv_summary(cv_data)
    else:
        st.markdown(
            """
            <div class="hireme-card" style="padding: 14px 18px; margin-bottom: 20px;">
              <span style="font-size: 0.875rem; color: var(--text-dim);">
                Pending CV upload. Upload your resume in Step 1 to inspect your extracted profile.
              </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -------------------------------------------------------------------------
    # STEP 3: Search & Preferences
    # -------------------------------------------------------------------------
    show_step_header(
        3,
        "Search Preferences",
        "Customize target seniority, location market, and remote work preferences.",
    )

    # Interactive Pills for Career Stage
    st.markdown("<label style='font-size: 0.875rem; font-weight: 600; color: var(--text-main); margin-bottom: 6px; display: block;'>Target Career Level</label>", unsafe_allow_html=True)
    if "selected_career_pill" not in st.session_state:
        saved_level = st.session_state.get("exp_level", "Auto-detect from CV")
        st.session_state.selected_career_pill = LEVEL_TO_PILL.get(saved_level, "Auto-detect")

    selected_pill = st.segmented_control(
        "Target Career Level",
        options=EXP_PILLS,
        key="selected_career_pill",
        label_visibility="collapsed",
    )
    if not selected_pill:
        selected_pill = "Auto-detect"
        st.session_state.selected_career_pill = "Auto-detect"

    st.session_state.exp_level = PILL_TO_LEVEL.get(selected_pill, "Auto-detect from CV")

    # Specific Target Role (Optional override)
    target_role = st.text_input(
        "Specific Job Title (Optional)",
        value=st.session_state.get("custom_role", ""),
        placeholder="e.g. AI Engineer, Python Intern, Frontend Developer — leave blank for AI match",
        help="Type a specific job title to target, or leave blank to let the AI pick the best match from your CV.",
    )
    st.session_state.custom_role = target_role.strip()

    # Country & Remote Settings
    col_country, col_count = st.columns([2, 1])
    with col_country:
        country_names = list(COUNTRY_MAP.keys())
        saved_country = st.session_state.get("country_label", "United Kingdom (UK)")
        default_country_idx = country_names.index(saved_country) if saved_country in country_names else 0
        country_choice = st.selectbox(
            "Target Country / Job Market",
            options=country_names,
            index=default_country_idx,
            help="Select the live job market to search via Adzuna.",
        )
        st.session_state.country_label = country_choice
        st.session_state.country_code = COUNTRY_MAP[country_choice]

    with col_count:
        count_options = [3, 5, 10]
        current_count = st.session_state.get("count", 3)
        default_index = count_options.index(current_count) if current_count in count_options else 0
        count_val = st.selectbox(
            "Vacancies to Match",
            options=count_options,
            index=default_index,
            help="Choose how many matching jobs to search and draft cover letters for.",
        )
        st.session_state.count = count_val

    # Remote toggle & City
    remote_only = st.checkbox(
        "Remote Roles Only (Work from anywhere / WFH)",
        value=st.session_state.get("remote_only", False),
        help="Filter strictly for remote vacancies to bypass regional residency restrictions.",
    )
    st.session_state.remote_only = remote_only

    current_loc = st.session_state.get("location", "")
    placeholder_text = "e.g. London, Manchester, New York..." if not remote_only else "Remote (Automatic)"
    location_val = st.text_input(
        "Target City / Region",
        value="Remote" if remote_only else current_loc,
        placeholder=placeholder_text,
        disabled=remote_only,
        help="Specify a city or region. Automatically disabled when 'Remote Roles Only' is active.",
    )
    if not remote_only and location_val != current_loc:
        st.session_state.location = location_val

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

    # Form Validation - allow search if CV is present
    can_submit = has_cv

    submit_button = st.button(
        "Find Matching Jobs & Write Cover Letters",
        type="primary",
        use_container_width=True,
        disabled=not can_submit,
    )

    if not has_cv:
        st.caption("Please upload your resume in Step 1 to begin job matching.")

    # Agent Execution - Fast, responsive spinner with zero artificial delays
    if submit_button:
        # If custom role was entered, prioritize it in preferred_roles
        if cv_data and st.session_state.get("custom_role"):
            custom_r = st.session_state.custom_role
            if "preferred_roles" in cv_data and custom_r not in cv_data["preferred_roles"]:
                cv_data["preferred_roles"].insert(0, custom_r)

        effective_loc = "Remote" if remote_only else (st.session_state.get("location") or "").strip()
        effective_exp = st.session_state.get("exp_level", "Auto-detect from CV")
        target_country = st.session_state.get("country_code", "gb")
        num_vacancies = st.session_state.get("count", 3)

        with st.spinner("Finding live matching vacancies and drafting tailored cover letters..."):
            try:
                results = run_agent(
                    location=effective_loc,
                    count=num_vacancies,
                    experience_level=effective_exp,
                    remote_only=remote_only,
                    country=target_country,
                )
                st.session_state.results = results
                st.session_state.stage = "results"
                st.session_state.error = None
                st.rerun()
            except Exception as err:
                st.session_state.error = f"Job search encountered an error: {err}"
                st.rerun()


# Alias for app.py
upload_page = show_upload_page
