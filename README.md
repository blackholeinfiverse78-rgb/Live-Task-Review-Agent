# Task Review AI System - Evolution & Maintenance (Day 5)

### System Purpose
The Task Review AI is a deterministic analysis system designed to evaluate engineering task definitions. It provides clear scoring, gap analysis, and recommended next steps based on a strictly rule-based engine. This system is purpose-built for zero-risk demonstrations.

### Features (Modular)
- **Deterministic Scoring**: Same input always yields the same result.
- **Zero-Crash Architecture**: Robust exception handling across the stack.
- **Predefined Scenarios**: Locked "Good", "Partial", and "Poor" paths for reliable demos.
- **Immediate Feedback**: Analysis of title depth, content detail, and technical specificity.

---

### How to Run

#### 1. Start the Backend
```bash
python -m app.main
```
Available at: `http://localhost:8000`

#### 2. Start the Frontend
```bash
python -m streamlit run frontend/streamlit_app.py
```
Available at: `http://localhost:8501`

---

### Demo Script (Locked Sequence)

1.  **Preparation**: Ensure both servers are running. Open the Frontend URL.
2.  **Scenario 1: The Ideal Path**:
    - Select **"Good Submission"** from the dropdown.
    - Click **"Analyze Submission"**.
    - Explain: "The system identifies correct logical markers and high technical depth, yielding a 95% score."
3.  **Scenario 2: The Actionable Gap**:
    - Select **"Partial Submission"**.
    - Click **"Analyze Submission"**.
    - Explain: "The system flags missing success criteria and suggests technical refinement milestones."
4.  **Scenario 3: The Safety Guard**:
    - Select **"Poor Submission"**.
    - Click **"Analyze Submission"**.
    - Explain: "Insufficient detail triggers a foundational refinement phase, preventing engineering waste."
5.  **Scenario 4: Live Resilience**:
    - Select **"Live Editor"**.
    - Enter a single word and try to submit.
    - Observe the graceful validation block.

---

### Demo Scenarios Detail
| Scenario | Score | Readiness | Rationale |
| :--- | :--- | :--- | :--- |
| **Good** | 95 | 90% | Comprehensive technical detail and objective markers. |
| **Partial** | 65 | 60% | Clear intent but lacks implementation constraints. |
| **Poor** | 30 | 25% | Actionable detail is missing; requires re-definition. |

---

### Deterministic Design Philosophy
To ensure no surprises during stakeholder presentations, this system utilizes a **deterministic decision matrix** instead of probabilistic models.
- **No Randomness**: No seeds, no temperatures, no external stochastic APIs.
- **Locked Transitions**: The mapping between a score and the "Next Task" is constant.

### Troubleshooting
- **Server Won't Start**: Check if port 8000 (backend) or 8501 (frontend) is already in use by another process.
- **Backend Offline**: Ensure `app/main.py` is running and the health check `http://localhost:8000/health` returns `healthy`.
- **Validation Error**: The system strictly enforces minimum lengths (Title > 5, Desc > 10).

---

---

### Changelog - 2026-02-05
- **Engine Refactor**: Modularized `ReviewEngine` into discrete rule evaluators.
- **Maintenance**: Lifted feature freeze to allow architectural improvements.
- **Cleanup**: Removed stale demo lockout headers.

**SYSTEM STATUS: MAINTENANCE & IMPROVEMENT MODE**
