"""
FEATURE FREEZE COMPLETE - DEMO-ONLY MODE
Locked on: 2026-02-02
"""
import streamlit as st
import requests
import logging
from datetime import datetime

BACKEND_URL = "http://localhost:8000/api/v1/task"

st.set_page_config(
    page_title="Task Review AI (PROD)",
    page_icon="🛡️",
    layout="centered"
)

# Immutable Demo Data
DEMO_DATA = {
    "Live Editor": {"title": "", "desc": "", "demo": False, "type": None},
    "Good Submission": {
        "title": "Build a Secure Async API Gateway for User Authentication",
        "desc": "The objective is to implement a robust API gateway. Requirements include schema validation using Pydantic, security constraints for JWT, and async database connections. This task ensures production readiness by adding caching and frontend integration layers.",
        "demo": True, "type": "good"
    },
    "Partial Submission": {
        "title": "Setup basic API",
        "desc": "We need an API to handle some requests. The requirement is to make it work. It should connect to a database eventually.",
        "demo": True, "type": "partial"
    },
    "Poor Submission": {
        "title": "fix stuff",
        "desc": "fix the bugs in the code",
        "demo": True, "type": "poor"
    }
}

st.title("🛡️ Task Review AI")

# Locked Scenario Selection
scenario = st.selectbox("Select Scenario", options=list(DEMO_DATA.keys()))
current = DEMO_DATA[scenario]

with st.form("main_form"):
    t_title = st.text_input("Task Title", value=current["title"], disabled=current["demo"])
    t_desc = st.text_area("Task Description", value=current["desc"], disabled=current["demo"], height=200)
    submitted_by = st.text_input("Name", value="Demo Professional")
    run_btn = st.form_submit_button("Analyze Submission", type="primary")

if run_btn:
    if not t_title.strip() or not t_desc.strip():
        st.error("Validation Failure: Both title and description are strictly required.")
    else:
        try:
            # Phase 1: Storage
            with st.spinner("Processing..."):
                res = requests.post(f"{BACKEND_URL}/submit", json={
                    "task_title": t_title, "task_description": t_desc,
                    "submitted_by": submitted_by, "is_demo": current["demo"],
                    "demo_type": current["type"]
                }, timeout=5)
                if res.status_code != 200:
                    st.error("Submission Rejected. check input criteria.")
                    st.stop()
                tid = res.json()["task_id"]

            # Phase 2: Analysis
                res = requests.post(f"{BACKEND_URL}/review", json={"task_id": tid}, timeout=5)
                res.raise_for_status()
                review = res.json()

            # Phase 3: Transition
                res = requests.post(f"{BACKEND_URL}/generate-next", json=review, timeout=5)
                res.raise_for_status()
                next_t = res.json()
                
            # Render Frozen UI
            st.divider()
            c1, c2 = st.columns(2)
            c1.metric("Score", f"{review['score']}/100")
            c2.metric("Readiness", f"{review['readiness_percent']}%")
            
            st.info(f"**Analysis:** {review['reviewer_summary']}")
            
            with st.expander("Gaps Identified", expanded=True):
                if review['gaps']:
                    for gap in review['gaps']: st.write(f"🚩 {gap}")
                else: st.success("No structural gaps detected.")

            with st.expander("System Hints", expanded=True):
                if review['improvement_hints']:
                    for h in review['improvement_hints']: st.write(f"💡 {h}")
                else: st.write("Task quality is sufficient for the current phase.")
            
            st.success(f"**Recommended Next Step:** {next_t['next_task_title']}")
            st.caption(f"Rationale: {next_t['rationale']}")
            
        except Exception as e:
            st.error("System Error: Analysis could not be completed at this time.")

st.sidebar.markdown("**System: Production Locked**")
try:
    health = requests.get("http://localhost:8000/health", timeout=1).json()
    st.sidebar.success(f"Backend v{health['version']}")
except:
    st.sidebar.error("Backend Offline")

st.sidebar.caption("Deterministic Engine v2.0")
