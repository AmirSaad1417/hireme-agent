"""
Results page for HireMe Agent.
Presents matched job opportunities, local Match % badges, sorting,
shortlisting, editable cover letters, copy/download actions, and direct apply links.
"""

import re
from typing import Any, Dict, List
import urllib.parse
import streamlit as st

from src.memory.cv_store import clear_cv
from src.ui.components import (
    ICON_ALERT,
    ICON_BUILDING,
    ICON_CHECK,
    ICON_DOWNLOAD,
    ICON_GLOBE,
    ICON_MAP_PIN,
    ICON_SALARY,
    ICON_SPARKLES,
    ICON_STAR,
    compute_match_score,
    show_error,
    show_header,
)


def _render_job_card(
    idx: int,
    job: Dict[str, Any],
    cv_data: Dict[str, Any],
    saved_ids: set,
) -> None:
    """Render a single modern SaaS job card with interactive actions."""
    job_id = str(job.get("id") or f"job_{idx}")
    job_title = job.get("job_title") or job.get("title") or "Opportunity"
    company = job.get("company") or job.get("company_name") or "Company not specified"
    location = job.get("location") or "Location not specified"
    salary = job.get("salary") or job.get("salary_range") or "Not specified"
    job_url = job.get("job_url") or job.get("url") or "#"
    description = job.get("description", "")
    cover_letter = job.get("cover_letter", "")
    country = job.get("country", "")

    # Local Match % computation (Zero API cost)
    match_score = compute_match_score(cv_data, job)

    is_remote_job = (
        "remote" in location.lower()
        or "remote" in job_title.lower()
        or "remote" in description.lower()
    )
    remote_badge = (
        f'<span class="hireme-chip hireme-chip-remote">{ICON_GLOBE} Remote</span>'
        if is_remote_job
        else ""
    )
    country_badge = f'<span class="hireme-chip">{country}</span>' if country else ""
    match_badge = f'<span class="hireme-match-chip">{ICON_SPARKLES} {match_score}% Match</span>'

    # Global search queries that bypass geoblocks
    clean_company = re.sub(r"[^\w\s]", "", company).strip()
    clean_title = re.sub(r"[^\w\s]", "", job_title).strip()
    search_query = f"{clean_company} {clean_title} jobs apply"
    google_url = f"https://www.google.com/search?q={urllib.parse.quote_plus(search_query)}"
    linkedin_url = f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote_plus(clean_company + ' ' + clean_title)}"

    is_saved = job_id in saved_ids

    # Outer card
    st.markdown(
        f"""
        <div class="hireme-job-card hireme-fade-in">
          <div class="hireme-job-card-header">
            <div>
              <h3 class="hireme-job-title">{job_title}</h3>
              <div class="hireme-job-company">{ICON_BUILDING} {company}</div>
            </div>
            <div>{match_badge}</div>
          </div>
          <div class="hireme-chip-container">
            <span class="hireme-chip">{ICON_MAP_PIN} {location}</span>
            <span class="hireme-chip">{ICON_SALARY} {salary}</span>
            {remote_badge}
            {country_badge}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # In-app Job Description Expander
    if description:
        with st.expander("Job Description & Requirements", expanded=False):
            st.write(description)

    # Editable Cover Letter Expander
    with st.expander("Tailored Cover Letter (Editable)", expanded=True):
        letter_key = f"cover_letter_text_{idx}_{job_id}"
        edited_letter = st.text_area(
            "Cover Letter",
            value=cover_letter,
            height=200,
            key=letter_key,
            label_visibility="collapsed",
        )

        # Action bar under cover letter: Copy & Download
        c_copy, c_dl, c_save = st.columns([1.1, 1.3, 1])
        with c_copy:
            if st.button("Copy Letter", key=f"btn_copy_{idx}_{job_id}", type="secondary", use_container_width=True):
                st.session_state[f"copied_{idx}_{job_id}"] = True
                st.toast("Cover letter copied! Use Ctrl+C / Cmd+C.")

            if st.session_state.get(f"copied_{idx}_{job_id}"):
                st.markdown(
                    f'<span style="color: var(--success-text); font-size: 0.75rem; font-weight: 700;">{ICON_CHECK} Copied!</span>',
                    unsafe_allow_html=True,
                )

        with c_dl:
            file_title = clean_title.replace(" ", "_")[:25]
            file_comp = clean_company.replace(" ", "_")[:20]
            st.download_button(
                label="Download (.txt)",
                data=edited_letter,
                file_name=f"CoverLetter_{file_comp}_{file_title}.txt",
                mime="text/plain",
                key=f"btn_dl_{idx}_{job_id}",
                use_container_width=True,
            )

        with c_save:
            save_label = "Unsave" if is_saved else "Save Job"
            if st.button(save_label, key=f"btn_save_{idx}_{job_id}", type="secondary", use_container_width=True):
                if is_saved:
                    saved_ids.remove(job_id)
                else:
                    saved_ids.add(job_id)
                st.session_state.saved_job_ids = list(saved_ids)
                st.rerun()

    # Application links
    col_apply, col_li, col_src = st.columns([1.5, 1.2, 1])
    with col_apply:
        st.link_button("Apply Direct / Google", url=google_url, type="primary", use_container_width=True)
    with col_li:
        st.link_button("Search on LinkedIn", url=linkedin_url, use_container_width=True)
    with col_src:
        if job_url and job_url != "#":
            st.link_button("Source Page", url=job_url, use_container_width=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)


def show_results_page() -> None:
    """Render the results dashboard with structured job cards, tabs, and filters."""
    show_header(current_step=3)
    show_error()

    results: List[Dict[str, Any]] = st.session_state.get("results", [])
    cv_data: Dict[str, Any] = st.session_state.get("cv_data") or {}

    # Initialize shortlist in session state
    if "saved_job_ids" not in st.session_state:
        st.session_state.saved_job_ids = []
    saved_ids = set(st.session_state.saved_job_ids)

    # Top Bar: Heading & Start Over popover confirmation
    col_summary, col_reset = st.columns([3, 1])
    with col_summary:
        st.markdown(
            f"""
            <div style="display: flex; align-items: baseline; gap: 10px; margin-bottom: 8px;">
              <h2 style="font-size: 1.35rem; font-weight: 700; margin: 0; color: var(--text-main);">
                Recommended Opportunities
              </h2>
              <span class="hireme-chip hireme-chip-primary">{len(results)} Total Matches</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col_reset:
        with st.popover("Start Over", use_container_width=True):
            st.markdown("**Reset current search?**")
            st.caption("This will clear current recommendations and generated cover letters.")
            if st.button("Confirm Reset", type="primary", use_container_width=True):
                clear_cv()
                st.session_state.cv_data = None
                st.session_state.results = []
                st.session_state.location = ""
                st.session_state.count = 3
                st.session_state.error = None
                st.session_state.last_file = None
                st.session_state.remote_only = False
                st.session_state.saved_job_ids = []
                st.session_state.stage = "upload"
                st.rerun()

    # Informational notice on regional access and direct apply options
    st.markdown(
        f"""
        <div class="hireme-alert hireme-alert-info">
          <span class="hireme-alert-icon">{ICON_GLOBE}</span>
          <div>
            <strong>Direct Applications:</strong>
            Use the <strong>Apply Direct / Google</strong> and <strong>LinkedIn</strong> buttons below to apply directly on company portals without regional geoblocks.
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Empty State Guard
    if not results:
        st.markdown(
            f"""
            <div class="hireme-card" style="text-align: center; padding: 40px 24px; margin-top: 16px;">
              <div style="color: var(--text-dim); margin-bottom: 12px;">{ICON_ALERT}</div>
              <h3 style="font-size: 1.15rem; font-weight: 600; color: var(--text-main); margin-bottom: 8px;">
                No Matching Vacancies Found
              </h3>
              <p style="font-size: 0.875rem; color: var(--text-muted); max-width: 480px; margin: 0 auto 20px auto; line-height: 1.5;">
                We could not find active vacancies matching your exact criteria. Try broadening your location,
                selecting a different career level, or enabling <strong>Remote Roles Only</strong>.
              </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Adjust Search Preferences", type="primary"):
            st.session_state.stage = "upload"
            st.rerun()
        return

    # Tabs: All Matches vs Shortlisted Jobs
    saved_jobs = [j for j in results if str(j.get("id") or "") in saved_ids]
    tab_all, tab_saved = st.tabs([f"All Matches ({len(results)})", f"Shortlisted ({len(saved_jobs)})"])

    # Filter & Sort Controls
    col_filter, col_sort = st.columns([1, 1])
    with col_filter:
        filter_remote = st.checkbox("Show Remote Only", value=False, key="filter_remote_cb")
    with col_sort:
        sort_by = st.selectbox(
            "Sort by",
            options=["Best Match %", "Title (A-Z)"],
            index=0,
            key="sort_results_by",
            label_visibility="collapsed",
        )

    # Helper function to sort and filter
    def _prepare_list(jobs_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        filtered = jobs_list
        if filter_remote:
            filtered = [
                j for j in filtered
                if "remote" in (j.get("location") or "").lower()
                or "remote" in (j.get("job_title") or j.get("title") or "").lower()
                or "remote" in (j.get("description") or "").lower()
            ]

        if sort_by == "Best Match %":
            filtered.sort(key=lambda j: compute_match_score(cv_data, j), reverse=True)
        elif sort_by == "Title (A-Z)":
            filtered.sort(key=lambda j: (j.get("job_title") or j.get("title") or "").lower())

        return filtered

    # Render All Matches Tab
    with tab_all:
        display_all = _prepare_list(results)
        if not display_all:
            st.info("No jobs match the current filter. Try unchecking 'Show Remote Only'.")
        else:
            for idx, job in enumerate(display_all, start=1):
                _render_job_card(idx, job, cv_data, saved_ids)

    # Render Shortlisted Tab
    with tab_saved:
        display_saved = _prepare_list(saved_jobs)
        if not display_saved:
            st.markdown(
                """
                <div class="hireme-card" style="text-align: center; padding: 30px; margin-top: 10px;">
                  <div style="font-size: 0.9375rem; color: var(--text-muted);">
                    No jobs saved yet. Click <strong>Save Job</strong> on any opportunity to shortlist it here.
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            for idx, job in enumerate(display_saved, start=1):
                _render_job_card(idx, job, cv_data, saved_ids)

    # Footer
    st.markdown(
        """
        <div class="hireme-footer">
          Powered by Groq &bull; Adzuna API &bull; PyMuPDF &bull; python-docx &bull; Streamlit
        </div>
        """,
        unsafe_allow_html=True,
    )


# Alias for app.py
results_page = show_results_page
