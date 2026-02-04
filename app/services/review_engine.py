"""
FEATURE FREEZE COMPLETE - DEMO-ONLY MODE
Locked on: 2026-02-02
Logic: Rule-Based Deterministic v2
"""
from ..models.schemas import Task, ReviewOutput
import logging

logger = logging.getLogger("task_review_system")

class ReviewEngine:
    # Locked Demo Scenarios - Permanent and Immutable
    DEMO_SCENARIOS = {
        "good": ReviewOutput(
            score=95,
            readiness_percent=90,
            gaps=[],
            improvement_hints=["Maintain current documentation standards."],
            reviewer_summary="EXCELLENT: Highly detailed task with clear technical constraints and success criteria."
        ),
        "partial": ReviewOutput(
            score=65,
            readiness_percent=60,
            gaps=["Missing success criteria", "Vague technical stack"],
            improvement_hints=["Explicitly list the technologies involved.", "Define what 'done' looks like."],
            reviewer_summary="ADEQUATE: The task is understood but lacks the depth required for immediate implementation."
        ),
        "poor": ReviewOutput(
            score=30,
            readiness_percent=25,
            gaps=["Extremely brief description", "No context provided", "Missing objective"],
            improvement_hints=["Restart the requirement gathering phase.", "Provide at least 3 paragraphs of context."],
            reviewer_summary="INSUFFICIENT: Task is too under-specified to be actionable by any engineering team."
        )
    }

    @staticmethod
    def review_task(task: Task, is_demo: bool = False, demo_type: str = None) -> ReviewOutput:
        """
        Pure deterministic review processor. Same Input -> Same Output.
        """
        if is_demo and demo_type in ReviewEngine.DEMO_SCENARIOS:
            return ReviewEngine.DEMO_SCENARIOS[demo_type]

        gaps = []
        hints = []
        score = 0
        
        # Rule 1: Title Depth
        t_len = len(task.task_title)
        if t_len > 40: score += 15
        elif t_len > 20: score += 10
        else:
            score += 5
            gaps.append("Brief title reduces context.")
            hints.append("Expand title to 40+ characters.")

        # Rule 2: Description Detail
        d_len = len(task.task_description)
        if d_len > 500: score += 30
        elif d_len > 200: score += 20
        elif d_len > 50: score += 10
        else:
            gaps.append("Minimal description substance.")
            hints.append("Provide detailed technical context.")

        # Rule 3: Structural Markers
        for marker in ["requirement", "objective", "constraint"]:
            if marker in task.task_description.lower():
                score += 10
            else:
                gaps.append(f"Missing logical marker: '{marker}'")
                hints.append(f"Define task {marker}s.")

        # Rule 4: Technical Keywords
        tech = ["api", "database", "schema", "validation", "security", "async", "cache", "frontend"]
        found = [k for k in tech if k in task.task_description.lower()]
        score += min(25, len(found) * 5)
        
        if len(found) < 2:
            gaps.append("Low technical specificity.")
            hints.append("Include technical implementation details.")

        final_score = min(100, score)
        readiness = int(final_score * 0.85) if final_score < 90 else final_score
        
        summary = f"Analysis complete (Score: {final_score}). "
        if final_score >= 85: summary += "Production ready."
        elif final_score >= 60: summary += "Minor refinement required."
        else: summary += "Major overhaul required."

        return ReviewOutput(
            score=final_score,
            readiness_percent=readiness,
            gaps=gaps,
            improvement_hints=hints,
            reviewer_summary=summary
        )
