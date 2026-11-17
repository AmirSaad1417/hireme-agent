"""
Comprehensive modern SaaS design system for HireMe Agent.
Defines design tokens (colors, gradients, typography, radius, layered shadows)
and rich interactive component styles with full Light and Dark mode support.
"""

import streamlit as st

CSS_STYLES = """
<style>
/* ==========================================================================
   Design Tokens & CSS Variables
   ========================================================================== */
:root {
  /* Brand Palette - Modern Blue / Teal SaaS Focus */
  --primary: #2563EB;
  --primary-hover: #1D4ED8;
  --primary-light: #EFF6FF;
  --primary-border: #BFDBFE;

  --teal-accent: #0D9488;
  --teal-hover: #0F766E;
  --teal-light: #F0FDFA;
  --teal-border: #99F6E4;

  /* Refined Blue -> Teal Gradients (strictly limited to Hero & Primary CTAs) */
  --grad-hero: linear-gradient(135deg, #1E40AF 0%, #0D9488 100%);
  --grad-btn: linear-gradient(135deg, #2563EB 0%, #0D9488 100%);
  --grad-btn-hover: linear-gradient(135deg, #1D4ED8 0%, #0F766E 100%);

  /* Neutrals - Slate Scale (Light Mode Default) */
  --bg-app: #FFFFFF;
  --bg-surface: #F8FAFC;
  --bg-surface-elevated: #FFFFFF;
  --bg-surface-subtle: #F1F5F9;

  --border-subtle: #E2E8F0;
  --border-strong: #CBD5E1;

  --text-main: #0F172A;
  --text-muted: #475569;
  --text-dim: #64748B;
  --text-on-primary: #FFFFFF;

  /* Semantic Feedback */
  --success: #059669;
  --success-bg: #ECFDF5;
  --success-border: #A7F3D0;
  --success-text: #065F46;

  --warning: #D97706;
  --warning-bg: #FFFBEB;
  --warning-border: #FDE68A;
  --warning-text: #92400E;

  --danger: #DC2626;
  --danger-bg: #FEF2F2;
  --danger-border: #FECACA;
  --danger-text: #991B1B;

  /* Layered Shadows for Soft Depth */
  --shadow-sm: 0 1px 3px 0 rgba(15, 23, 42, 0.05);
  --shadow-card: 0 2px 6px -1px rgba(15, 23, 42, 0.06), 0 1px 4px -1px rgba(15, 23, 42, 0.04);
  --shadow-card-hover: 0 10px 20px -3px rgba(15, 23, 42, 0.09), 0 4px 8px -2px rgba(15, 23, 42, 0.04);
  --shadow-popover: 0 20px 25px -5px rgba(15, 23, 42, 0.1), 0 10px 10px -5px rgba(15, 23, 42, 0.04);

  /* Radius System */
  --radius-sm: 6px;
  --radius-md: 10px;
  --radius-card: 14px;
  --radius-pill: 9999px;

  /* Spacing */
  --space-2xs: 2px;
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;

  /* Transitions */
  --anim-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --anim-smooth: 220ms cubic-bezier(0.4, 0, 0.2, 1);
}

/* ==========================================================================
   Dark Mode Overrides
   ========================================================================== */
@media (prefers-color-scheme: dark) {
  :root {
    --bg-app: #0B0F19;
    --bg-surface: #111827;
    --bg-surface-elevated: #162032;
    --bg-surface-subtle: #1E293B;

    --border-subtle: #1E293B;
    --border-strong: #334155;

    --text-main: #F8FAFC;
    --text-muted: #94A3B8;
    --text-dim: #64748B;

    --primary-light: rgba(37, 99, 235, 0.18);
    --primary-border: rgba(37, 99, 235, 0.4);

    --teal-light: rgba(13, 148, 136, 0.18);
    --teal-border: rgba(13, 148, 136, 0.4);

    --success-bg: rgba(5, 150, 105, 0.18);
    --success-border: rgba(5, 150, 105, 0.4);
    --success-text: #34D399;

    --warning-bg: rgba(217, 119, 6, 0.18);
    --warning-border: rgba(217, 119, 6, 0.4);
    --warning-text: #FBBF24;

    --danger-bg: rgba(220, 38, 38, 0.18);
    --danger-border: rgba(220, 38, 38, 0.4);
    --danger-text: #F87171;

    --shadow-sm: 0 1px 3px 0 rgba(0, 0, 0, 0.4);
    --shadow-card: 0 4px 8px -1px rgba(0, 0, 0, 0.5), 0 2px 4px -2px rgba(0, 0, 0, 0.4);
    --shadow-card-hover: 0 12px 24px -4px rgba(0, 0, 0, 0.65), 0 6px 12px -3px rgba(0, 0, 0, 0.5);
    --shadow-popover: 0 20px 25px -5px rgba(0, 0, 0, 0.7);
  }
}

/* ==========================================================================
   Layout & Container Structure
   ========================================================================== */
.block-container {
  max-width: 880px !important;
  padding-top: 2rem !important;
  padding-bottom: 4rem !important;
}

*:focus-visible {
  outline: 2px solid var(--primary) !important;
  outline-offset: 2px !important;
}

/* Smooth fade-in animation for results */
@keyframes hireme-fade-in {
  from {
    opacity: 0;
    transform: translateY(6px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.hireme-fade-in {
  animation: hireme-fade-in var(--anim-smooth) forwards;
}

/* ==========================================================================
   Hero Header with Blue->Teal Gradient & Step Stepper
   ========================================================================== */
.hireme-hero {
  padding: var(--space-md) var(--space-lg);
  border-radius: var(--radius-card);
  margin-bottom: var(--space-lg);
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  box-shadow: var(--shadow-sm);
}

.hireme-hero-top {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-xs);
}

.hireme-hero-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: var(--radius-md);
  background: var(--grad-hero);
  color: #FFFFFF;
  box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3);
}

.hireme-hero-title {
  font-size: 1.7rem;
  font-weight: 700;
  letter-spacing: -0.025em;
  color: var(--text-main);
  margin: 0;
  line-height: 1.2;
}

.hireme-hero-tagline {
  font-size: 0.9375rem;
  color: var(--text-muted);
  line-height: 1.45;
  margin: var(--space-xs) 0 var(--space-md) 0;
}

/* 3-Step Progress Stepper */
.hireme-stepper {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-sm);
  padding: 10px 14px;
  border-radius: var(--radius-md);
  background: var(--bg-surface-subtle);
  border: 1px solid var(--border-subtle);
}

.hireme-step-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--text-dim);
}

.hireme-step-item.active {
  color: var(--primary);
}

.hireme-step-item.completed {
  color: var(--success-text);
}

.hireme-step-circle {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 22px;
  height: 22px;
  border-radius: var(--radius-full);
  background: var(--bg-surface-elevated);
  border: 1.5px solid var(--border-strong);
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--text-dim);
}

.hireme-step-item.active .hireme-step-circle {
  background: var(--primary);
  border-color: var(--primary);
  color: #FFFFFF;
  box-shadow: 0 0 0 3px var(--primary-light);
}

.hireme-step-item.completed .hireme-step-circle {
  background: var(--success);
  border-color: var(--success);
  color: #FFFFFF;
}

.hireme-stepper-divider {
  flex: 1;
  height: 2px;
  background: var(--border-subtle);
  border-radius: 1px;
}

.hireme-stepper-divider.completed {
  background: var(--success-border);
}

/* ==========================================================================
   Primary Button Gradient & Interactive States
   ========================================================================== */
button[kind="primary"] {
  background: var(--grad-btn) !important;
  color: #FFFFFF !important;
  border: none !important;
  border-radius: var(--radius-md) !important;
  font-weight: 600 !important;
  padding: 0.625rem 1.25rem !important;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.25) !important;
  transition: all var(--anim-fast) !important;
}

button[kind="primary"]:hover {
  background: var(--grad-btn-hover) !important;
  transform: translateY(-1px) !important;
  box-shadow: 0 6px 14px rgba(37, 99, 235, 0.35) !important;
}

button[kind="primary"]:active {
  transform: translateY(0) !important;
  box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2) !important;
}

button[kind="secondary"] {
  border-radius: var(--radius-md) !important;
  transition: all var(--anim-fast) !important;
}

button[kind="secondary"]:hover {
  border-color: var(--border-strong) !important;
}

/* ==========================================================================
   Cards & Elevated Surfaces (14px Radius + Soft Hover Lift)
   ========================================================================== */
.hireme-card {
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-card);
  padding: var(--space-lg);
  margin-bottom: var(--space-md);
  box-shadow: var(--shadow-card);
  transition: transform var(--anim-smooth), box-shadow var(--anim-smooth), border-color var(--anim-smooth);
}

.hireme-card:hover {
  border-color: var(--border-strong);
  box-shadow: var(--shadow-card-hover);
}

/* Results Job Card with Smooth Lift */
.hireme-job-card {
  background: var(--bg-surface-elevated);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-card);
  padding: var(--space-lg);
  margin-bottom: var(--space-lg);
  box-shadow: var(--shadow-card);
  transition: transform var(--anim-smooth), box-shadow var(--anim-smooth), border-color var(--anim-smooth);
}

.hireme-job-card:hover {
  transform: translateY(-2px);
  border-color: var(--primary-border);
  box-shadow: var(--shadow-card-hover);
}

.hireme-job-card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--space-md);
  margin-bottom: var(--space-sm);
}

.hireme-job-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--text-main);
  letter-spacing: -0.015em;
  line-height: 1.3;
  margin: 0;
}

.hireme-job-company {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--primary);
  margin-top: 3px;
  margin-bottom: var(--space-xs);
}

/* ==========================================================================
   Chips, Badges & Local Match % Indicator
   ========================================================================== */
.hireme-chip-container {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 6px 8px;
  margin: 10px 0 14px 0;
}

.hireme-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.8125rem;
  font-weight: 500;
  padding: 4px 10px;
  border-radius: var(--radius-pill);
  background: var(--bg-surface-subtle);
  color: var(--text-muted);
  border: 1px solid var(--border-subtle);
  line-height: 1.4;
  white-space: nowrap;
}

/* Local Skill Match Score Pill */
.hireme-match-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-size: 0.8125rem;
  font-weight: 700;
  padding: 4px 11px;
  border-radius: var(--radius-pill);
  background: var(--success-bg);
  color: var(--success-text);
  border: 1px solid var(--success-border);
  letter-spacing: 0.01em;
}

.hireme-chip-remote {
  background: var(--teal-light);
  color: var(--teal-hover);
  border-color: var(--teal-border);
  font-weight: 600;
}

.hireme-badge-tier {
  display: inline-flex;
  align-items: center;
  padding: 3px 9px;
  font-size: 0.75rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  border-radius: var(--radius-sm);
  background: var(--primary-light);
  color: var(--primary);
  border: 1px solid var(--primary-border);
}

/* ==========================================================================
   Alert Banners & Notice Boxes
   ========================================================================== */
.hireme-alert {
  display: flex;
  align-items: flex-start;
  gap: var(--space-sm);
  padding: 12px 16px;
  border-radius: var(--radius-md);
  font-size: 0.875rem;
  line-height: 1.5;
  margin-bottom: var(--space-md);
  border: 1px solid transparent;
}

.hireme-alert-info {
  background: var(--primary-light);
  border-color: var(--primary-border);
  color: var(--text-main);
}

.hireme-alert-warning {
  background: var(--warning-bg);
  border-color: var(--warning-border);
  color: var(--warning-text);
}

.hireme-alert-danger {
  background: var(--danger-bg);
  border-color: var(--danger-border);
  color: var(--danger-text);
}

.hireme-alert-icon {
  flex-shrink: 0;
  width: 18px;
  height: 18px;
  margin-top: 1px;
}

/* ==========================================================================
   Step Header Component
   ========================================================================== */
.hireme-step-header {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-top: var(--space-lg);
  margin-bottom: var(--space-xs);
}

.hireme-step-num {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  border-radius: var(--radius-full);
  background: var(--grad-btn);
  color: #FFFFFF;
  font-size: 0.8125rem;
  font-weight: 700;
}

.hireme-step-title {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--text-main);
  margin: 0;
  letter-spacing: -0.015em;
}

.hireme-step-desc {
  font-size: 0.875rem;
  color: var(--text-muted);
  margin-top: 2px;
  margin-bottom: var(--space-sm);
  line-height: 1.45;
}

/* ==========================================================================
   Footer Component
   ========================================================================== */
.hireme-footer {
  text-align: center;
  padding-top: var(--space-xl);
  padding-bottom: var(--space-md);
  color: var(--text-dim);
  font-size: 0.8125rem;
  border-top: 1px solid var(--border-subtle);
  margin-top: var(--space-xl);
}

/* ==========================================================================
   Reduced Motion
   ========================================================================== */
@media (prefers-reduced-motion: reduce) {
  *, ::before, ::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* ==========================================================================
   Mobile Responsiveness (375px - 768px)
   ========================================================================== */
@media (max-width: 640px) {
  .block-container {
    padding-left: 0.875rem !important;
    padding-right: 0.875rem !important;
  }

  .hireme-hero {
    padding: var(--space-md);
  }

  .hireme-hero-title {
    font-size: 1.4rem;
  }

  .hireme-job-card {
    padding: var(--space-md);
  }

  .hireme-stepper {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .hireme-stepper-divider {
    display: none;
  }
}
</style>
"""


def inject_styles() -> None:
    """Inject the global HireMe SaaS design system CSS into the Streamlit app."""
    st.markdown(CSS_STYLES, unsafe_allow_html=True)
