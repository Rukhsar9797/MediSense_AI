"""
MediSense AI - Healthcare Medication Adherence Dashboard & Risk Engine
========================================================================
Architecture: Minimalist Two-Panel Clinical SaaS Dashboard
Capacity: 50 Real Patient Records (p101 - p150)
Integrates Teammate's Real Backend Modules:
- src.adherence (calculate_adherence)
- src.risk_engine (calculate_risk)
- src.ai_advisor (generate_report, get_recommendations)
- src.pdf_generator (individual patient PDF report export)
"""

import os
import sys

# Ensure project root is in sys.path regardless of execution CWD
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from datetime import datetime
import streamlit as st
import pandas as pd

from src.backend_adapter import (
    load_all_patients,
    load_all_doses,
    get_patient_doses,
    compute_patient_adherence,
    compute_patient_risk,
    simulate_patient_dose,
    reset_patient_doses,
    get_ai_companion_response,
)
from src.pdf_generator import generate_patient_pdf
from src.ui_components import (
    apply_minimalist_styles,
    render_brand_header,
    render_patient_profile_card,
    render_kpi_tiles,
    render_adherence_trend,
    render_risk_reasons,
    render_active_alerts,
    render_dose_history_table,
)

# -----------------------------------------------------------------------------
# 1. Page Configuration & Custom Healthcare SaaS Styling
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="MediSense AI | Clinical Adherence & Risk Engine",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

apply_minimalist_styles()

# -----------------------------------------------------------------------------
# 2. Session State Initialization (All 50 Patients & Real Dose Records)
# -----------------------------------------------------------------------------
if "patients_df" not in st.session_state:
    st.session_state.patients_df = load_all_patients()

if "original_doses_df" not in st.session_state:
    orig_doses = load_all_doses()
    st.session_state.original_doses_df = orig_doses
    st.session_state.doses_df = orig_doses.copy()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = {}

if "reminder_prefs" not in st.session_state:
    st.session_state.reminder_prefs = {}

if "selected_patient_id" not in st.session_state:
    st.session_state.selected_patient_id = "p101"

patients_df = st.session_state.patients_df

# -----------------------------------------------------------------------------
# 3. Top Branding Header & Medical Disclaimer Notice
# -----------------------------------------------------------------------------
render_brand_header()

# Prototype safety notice banner
st.markdown(
    """
    <div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-left: 3px solid #0D9488; padding: 10px 16px; border-radius: 6px; font-size: 12px; color: #475569; margin-bottom: 20px;">
        <strong>Clinical Prototype Disclaimer:</strong> MediSense AI monitors medication adherence patterns and calculates heuristic adherence-risk scores. It is not a diagnostic device and does not modify clinical treatments. Always consult your healthcare provider.
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# 4. Interactive Two-Panel Layout (Left ~35%, Right ~65%)
# -----------------------------------------------------------------------------
left_col, right_col = st.columns([35, 65], gap="large")

# =============================================================================
# LEFT PANEL: PATIENT INFORMATION & CONTROLS (~35% width)
# =============================================================================
with left_col:
    st.markdown("#### 👤 Patient Directory & Profile")
    
    # Searchable Patient Filter across all 50 patients
    search_query = st.text_input(
        "Search 50 Patients (ID, Name, or Condition):",
        "",
        placeholder="e.g. Eleanor, p105, Hypertension...",
    ).strip().lower()

    if search_query:
        filtered_df = patients_df[
            patients_df["patient_id"].str.contains(search_query, na=False) |
            patients_df["name"].str.lower().str.contains(search_query, na=False) |
            patients_df["primary_condition"].str.lower().str.contains(search_query, na=False)
        ]
        if filtered_df.empty:
            st.warning("No matching patient records found. Showing all patients.")
            filtered_df = patients_df
    else:
        filtered_df = patients_df

    # Patient Selector dropdown
    patient_id_list = filtered_df["patient_id"].tolist()
    patient_display_names = {
        row["patient_id"]: f"{row['patient_id'].upper()} - {row['name']} ({row['primary_condition'][:25]}...)"
        for _, row in filtered_df.iterrows()
    }

    # Ensure selected patient is in the list
    curr_id = st.session_state.selected_patient_id
    default_idx = patient_id_list.index(curr_id) if curr_id in patient_id_list else 0

    new_selected_id = st.selectbox(
        "Select Active Patient Profile:",
        options=patient_id_list,
        format_func=lambda pid: patient_display_names.get(pid, pid.upper()),
        index=default_idx,
        help="Switch patient to recalculate backend metrics, risk evaluation, and report export.",
    )

    if new_selected_id != st.session_state.selected_patient_id:
        st.session_state.selected_patient_id = new_selected_id
        st.rerun()

    selected_id = st.session_state.selected_patient_id
    patient_row = patients_df[patients_df["patient_id"] == selected_id].iloc[0].to_dict()

    # Initialize chat & prefs if not yet populated
    if selected_id not in st.session_state.chat_history:
        st.session_state.chat_history[selected_id] = [
            {
                "role": "assistant",
                "content": f"**[AI Advisor Active]**\n\nHello {patient_row['name']}. I am monitoring your medication adherence records for {patient_row['primary_condition']}. How can I assist with your routine today?",
            }
        ]

    if selected_id not in st.session_state.reminder_prefs:
        st.session_state.reminder_prefs[selected_id] = {
            "preferred_window": patient_row.get("preferred_window", "08:30 AM"),
            "routine_anchor": patient_row.get("routine_anchor", "Morning Routine"),
        }

    # Render Patient Profile Card
    render_patient_profile_card(patient_row)

    # -------------------------------------------------------------------------
    # Dose Event Simulation Functional Controls
    # -------------------------------------------------------------------------
    st.markdown("##### 🧪 Dose Simulation Controls")
    st.caption("Update in-memory session records to test real-time backend recalculations.")

    sim_c1, sim_c2 = st.columns(2)
    with sim_c1:
        if st.button("➕ Log Taken Dose", use_container_width=True, type="primary"):
            st.session_state.doses_df = simulate_patient_dose(
                st.session_state.doses_df,
                patient_id=selected_id,
                status="taken",
            )
            st.success(f"Simulated taken dose logged for {selected_id.upper()}!")
            st.rerun()

    with sim_c2:
        if st.button("⚠️ Log Missed Dose", use_container_width=True):
            st.session_state.doses_df = simulate_patient_dose(
                st.session_state.doses_df,
                patient_id=selected_id,
                status="missed",
            )
            st.warning(f"Simulated missed dose logged for {selected_id.upper()}!")
            st.rerun()

    if st.button("🔄 Reset Patient Scenario", use_container_width=True):
        st.session_state.doses_df = reset_patient_doses(
            current_doses_df=st.session_state.doses_df,
            original_doses_df=st.session_state.original_doses_df,
            patient_id=selected_id,
        )
        st.session_state.chat_history[selected_id] = [
            {
                "role": "assistant",
                "content": f"**[AI Advisor Active]**\n\nScenario reset to baseline records for {patient_row['name']}.",
            }
        ]
        st.info("Original dose records restored.")
        st.rerun()

    st.markdown("---")

    # -------------------------------------------------------------------------
    # Download Patient Report Feature (PDF)
    # -------------------------------------------------------------------------
    st.markdown("##### 📄 Export Individual Patient Report")
    st.caption("Generate a downloadable, comprehensive clinical PDF report for the active patient.")

    # Compute latest stats for PDF generation
    cur_adh = compute_patient_adherence(st.session_state.doses_df, patient_id=selected_id)
    cur_risk = compute_patient_risk(st.session_state.doses_df, patient_id=selected_id)
    cur_doses = get_patient_doses(st.session_state.doses_df, selected_id)
    
    # Generate contextual recommendations text for PDF
    pref_summary = st.session_state.reminder_prefs[selected_id]
    cur_recs = get_ai_companion_response(
        patient=patient_row,
        adherence_stats=cur_adh,
        risk_summary=cur_risk,
        question="Provide a structured summary of routine habit suggestions.",
        preferences=pref_summary,
    )

    pdf_bytes = generate_patient_pdf(
        patient=patient_row,
        adherence_stats=cur_adh,
        risk_summary=cur_risk,
        dose_records=cur_doses,
        recommendations_text=cur_recs,
    )

    today_file_date = datetime.now().strftime("%Y-%m-%d")
    report_filename = f"MediSense_Report_{selected_id}_{today_file_date}.pdf"

    st.download_button(
        label="⬇️ Download Patient Report (PDF)",
        data=pdf_bytes,
        file_name=report_filename,
        mime="application/pdf",
        use_container_width=True,
    )


# =============================================================================
# RIGHT PANEL: ANALYSIS, RISK & AI INSIGHTS (~65% width)
# =============================================================================
with right_col:
    st.markdown(f"#### 📊 Adherence Analytics & Clinical Insights — {patient_row['name']}")
    
    # Recalculate dynamic metrics from active session state
    adherence_stats = compute_patient_adherence(st.session_state.doses_df, patient_id=selected_id)
    risk_summary = compute_patient_risk(st.session_state.doses_df, patient_id=selected_id)
    patient_doses = get_patient_doses(st.session_state.doses_df, selected_id)

    # 1. 4 Primary Executive KPI Cards
    render_kpi_tiles(adherence_stats, risk_summary)
    st.write("")

    # 2. Adherence Trajectory Trend Chart
    render_adherence_trend(patient_doses)
    st.write("")

    # 3. Two sub-panels: Risk Evaluation & Clinical Alerts
    c_risk, c_alert = st.columns(2)
    with c_risk:
        st.markdown("##### 🔍 Evaluated Risk Factors (Backend Engine)")
        render_risk_reasons(risk_summary)

    with c_alert:
        st.markdown("##### ⚠️ Active Clinical Alerts")
        render_active_alerts(risk_summary)

    st.markdown("---")

    # 4. Personalized AI Companion & Habit Support
    st.markdown("##### 💬 Personalized AI Companion & Habit Advisor")
    st.caption("Powered by backend habit-building intelligence. Context-aware and isolated per patient.")

    # Suggested Question Buttons
    sq_col1, sq_col2, sq_col3 = st.columns(3)
    user_prompt = None

    with sq_col1:
        if st.button("📉 Why is my adherence score falling?", use_container_width=True):
            user_prompt = "Why is my adherence score falling?"
    with sq_col2:
        if st.button("⏰ Help me build a reminder routine", use_container_width=True):
            user_prompt = "Help me build a reminder routine"
    with sq_col3:
        if st.button("📋 Summarize my recent progress", use_container_width=True):
            user_prompt = "Summarize my recent progress"

    # Chat history container
    chat_box = st.container(height=260)
    with chat_box:
        for msg in st.session_state.chat_history[selected_id]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Chat input
    chat_in = st.chat_input("Ask about routine anchors, adherence patterns, or dose management...")
    if chat_in:
        user_prompt = chat_in

    if user_prompt:
        # Append user message
        st.session_state.chat_history[selected_id].append({
            "role": "user",
            "content": user_prompt,
        })

        # Generate response using backend advisor
        resp = get_ai_companion_response(
            patient=patient_row,
            adherence_stats=adherence_stats,
            risk_summary=risk_summary,
            question=user_prompt,
            preferences=st.session_state.reminder_prefs[selected_id],
        )

        st.session_state.chat_history[selected_id].append({
            "role": "assistant",
            "content": resp,
        })
        st.rerun()

    st.markdown("---")

    # 5. Comprehensive Medication Dose-Event Audit Table
    st.markdown("##### 📋 Medication Dose-Event History (Audit Trail)")
    render_dose_history_table(patient_doses)

# -----------------------------------------------------------------------------
# 5. Footer
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div style="text-align: center; color: #94A3B8; font-size: 11px; margin-top: 30px; padding: 16px 0; border-top: 1px solid #E2E8F0;">
        MediSense AI • Integrated Full-Stack Healthcare Analytics Dashboard • 50-Patient Roster • Streamlit, Pandas & FPDF2
    </div>
    """,
    unsafe_allow_html=True,
)
