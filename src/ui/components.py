"""
Reusable UI components for HireMe Agent.
Designed with soft, accessible UI patterns and clean SVG iconography.
"""

from typing import Any, Dict, Optional
import streamlit as st

# Clean SVG Icons (no emojis, cross-platform consistent vector rendering)
ICON_BRIEFCASE = """<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="14" x="2" y="7" rx="2" ry="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>"""
ICON_MAP_PIN = """<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 4.993-5.539 10.193-7.399 11.799a1 1 0 0 1-1.202 0C9.539 20.193 4 10.993 4 10a8 8 0 0 1 16 0"/><circle cx="12" cy="10" r="3"/></svg>"""
ICON_BUILDING = """<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="16" height="20" x="4" y="2" rx="2" ry="2"/><path d="M9 22v-4h6v4"/><path d="M8 6h.01"/><path d="M16 6h.01"/><path d="M8 10h.01"/><path d="M16 10h.01"/><path d="M8 14h.01"/><path d="M16 14h.01"/></svg>"""
ICON_SALARY = """<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" x2="12" y1="2" y2="22"/><path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>"""
ICON_GLOBE = """<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>"""
ICON_ALERT = """<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" x2="12" y1="8" y2="12"/><line x1="12" x2="12.01" y1="16" y2="16"/></svg>"""
ICON_CHECK = """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/></svg>"""
ICON_STAR = """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>"""
ICON_DOWNLOAD = """<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" x2="12" y1="15" y2="3"/></svg>"""
ICON_SPARKLES = """<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.912 5.813a2 2 0 0 1-1.275 1.275L3 12l5.813 1.912a2 2 0 0 1 1.275 1.275L12 21l1.912-5.813a2 2 0 0 1 1.275-1.275L21 12l-5.813-1.912a2 2 0 0 1-1.275-1.275L12 3Z"/></svg>"""


def show_header(current_step: int = 1) -> None:
    """
    Display the SaaS hero header with brand icon, calm tagline, and
    an interactive 3-step progress stepper (Upload -> Verify -> Results).

    Args:
        current_step: Current active step (1 = Upload, 2 = Verify, 3 = Results).
    """
    step1_class = "completed" if current_step > 1 else ("active" if current_step == 1 else "")
    step2_class = "completed" if current_step > 2 else ("active" if current_step == 2 else "")
    step3_class = "active" if current_step == 3 else ""

    div1_class = "completed" if current_step > 1 else ""
    div2_class = "completed" if current_step > 2 else ""

    s1_icon = ICON_CHECK if current_step > 1 else "1"
    s2_icon = ICON_CHECK if current_step > 2 else "2"
    s3_icon = "3"

    hero_html = f"""
    <div class="hireme-hero">
      <div class="hireme-hero-top">
        <span class="hireme-hero-badge">{ICON_BRIEFCASE}</span>
        <h1 class="hireme-hero-title">HireMe Agent</h1>
      </div>
      <p class="hireme-hero-tagline">
        Intelligent career companion: match your experience level with live vacancies
        and craft tailored, high-converting cover letters.
      </p>

      <!-- 3-Step Progress Stepper -->
      <div class="hireme-stepper" role="navigation" aria-label="Workflow Steps">
        <div class="hireme-step-item {step1_class}">
          <span class="hireme-step-circle">{s1_icon}</span>
          <span>Upload CV</span>
        </div>
        <div class="hireme-stepper-divider {div1_class}"></div>
        <div class="hireme-step-item {step2_class}">
          <span class="hireme-step-circle">{s2_icon}</span>
          <span>Verify Profile</span>
        </div>
        <div class="hireme-stepper-divider {div2_class}"></div>
        <div class="hireme-step-item {step3_class}">
          <span class="hireme-step-circle">{s3_icon}</span>
          <span>Match & Apply</span>
        </div>
      </div>
    </div>
    """
    st.markdown(hero_html, unsafe_allow_html=True)


def show_error() -> None:
    """Display any error in session state as an accessible styled alert with a dismiss action."""
    error_msg: Optional[str] = st.session_state.get("error")
    if error_msg:
        alert_html = f"""
        <div class="hireme-alert hireme-alert-danger" role="alert">
          <span class="hireme-alert-icon">{ICON_ALERT}</span>
          <div>
            <strong>Notice:</strong> {error_msg}
          </div>
        </div>
        """
        st.markdown(alert_html, unsafe_allow_html=True)
        if st.button("Dismiss Message", key="btn_dismiss_error", type="secondary"):
            st.session_state.error = None
            st.rerun()


def show_step_header(step_number: int, title: str, description: str = "") -> None:
    """Render a structured step header for the guided workflow."""
    step_html = f"""
    <div class="hireme-step-header">
      <span class="hireme-step-num">{step_number}</span>
      <h2 class="hireme-step-title">{title}</h2>
    </div>
    """
    if description:
        step_html += f'<p class="hireme-step-desc">{description}</p>'
    st.markdown(step_html, unsafe_allow_html=True)


def show_cv_summary(cv_data: Dict[str, Any]) -> None:
    """
    Display a polished CV summary card showing extracted candidate information,
    detected seniority tier, and skill chips that expands on click.

    Args:
        cv_data: Parsed CV dictionary.
    """
    if not cv_data:
        return

    name = cv_data.get("name", "Candidate")
    exp_level = cv_data.get("experience_level", "Auto-detected")
    skills = cv_data.get("skills", [])
    preferred_roles = cv_data.get("preferred_roles", [])
    industries = cv_data.get("preferred_industries", [])
    summary = cv_data.get("summary", "")

    # Top skill chips preview
    skill_chips = "".join([f'<span class="hireme-chip">{s}</span>' for s in skills[:6]])

    card_header_html = f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
      <span style="font-size: 0.95rem; font-weight: 700; color: var(--text-main);">{name}</span>
      <span class="hireme-badge-tier">{exp_level}</span>
    </div>
    <div class="hireme-chip-container" style="margin-top: 4px; margin-bottom: 8px;">
      {skill_chips}
    </div>
    """
    st.markdown(card_header_html, unsafe_allow_html=True)

    with st.expander("Inspect Full Extracted Details", expanded=False):
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"**Full Name:** {cv_data.get('name', 'N/A')}")
            st.markdown(f"**Email:** {cv_data.get('email', 'N/A')}")
            st.markdown(f"**Phone:** {cv_data.get('phone', 'N/A')}")
            st.markdown(f"**Location:** {cv_data.get('location', 'N/A')}")
            st.markdown(f"**Detected Level:** `{exp_level}`")

        with col2:
            skills_all = ", ".join(skills) if skills else "N/A"
            st.markdown(f"**All Skills:** {skills_all}")

            roles_all = ", ".join(preferred_roles) if preferred_roles else "N/A"
            st.markdown(f"**Target Roles:** {roles_all}")

            ind_all = ", ".join(industries) if industries else "N/A"
            st.markdown(f"**Industries:** {ind_all}")

        if summary:
            st.markdown(f"**Summary:** _{summary}_")


def compute_match_score(cv_data: Optional[Dict[str, Any]], job: Dict[str, Any]) -> int:
    """
    Compute a deterministic local match score (68% - 98%) based on keyword overlap
    between candidate skills/roles and the job requirements without extra LLM/API calls.

    Args:
        cv_data: Parsed CV dictionary.
        job: Job listing dictionary.

    Returns:
        int: Match percentage score.
    """
    if not cv_data or not job:
        return 82

    skills = cv_data.get("skills", [])
    roles = cv_data.get("preferred_roles", [])
    job_text = (
        (job.get("title") or "")
        + " "
        + (job.get("description") or "")
        + " "
        + (job.get("job_title") or "")
    ).lower()

    if not skills:
        return 80

    matched = sum(1 for s in skills if s.strip() and s.strip().lower() in job_text)
    ratio = matched / max(len(skills), 1)

    role_matched = False
    for r in roles:
        words = [w.lower() for w in r.split() if len(w) > 2]
        if any(w in job_text for w in words):
            role_matched = True
            break

    base = 75 if role_matched else 70
    score = int(base + (ratio * 24))
    return min(max(score, 68), 98)
