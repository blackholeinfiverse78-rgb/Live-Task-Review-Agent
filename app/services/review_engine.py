"""
Task Review AI - Modular Engine v2.1
Updated on: 2026-02-05
Logic: Modular Deterministic Rule Evaluators
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
    def _evaluate_title(title: str, gaps: list, hints: list) -> int:
        t_len = len(title)
        if t_len > 40:
            return 15
        if t_len > 20:
            return 10
        gaps.append("Brief title reduces context.")
        hints.append("Expand title to 40+ characters.")
        return 5

    @staticmethod
    def _evaluate_description(description: str, gaps: list, hints: list) -> int:
        d_len = len(description)
        if d_len > 500:
            return 30
        if d_len > 200:
            return 20
        if d_len > 50:
            return 10
        gaps.append("Minimal description substance.")
        hints.append("Provide detailed technical context.")
        return 0

    @staticmethod
    def _evaluate_markers(description: str, gaps: list, hints: list) -> int:
        score = 0
        description_lower = description.lower()
        for marker in ["requirement", "objective", "constraint"]:
            if marker in description_lower:
                score += 10
            else:
                gaps.append(f"Missing logical marker: '{marker}'")
                hints.append(f"Define task {marker}s.")
        return score

    @staticmethod
    def _evaluate_technical_keywords(description: str, gaps: list, hints: list) -> int:
        tech = ["api", "database", "schema", "validation", "security", "async", "cache", "frontend"]
        description_lower = description.lower()
        found = [k for k in tech if k in description_lower]
        score = min(25, len(found) * 5)
        
        if len(found) < 2:
            gaps.append("Low technical specificity.")
            hints.append("Include technical implementation details.")
        return score

    @classmethod
    def review_task(cls, task: Task, is_demo: bool = False, demo_type: str = None) -> ReviewOutput:
        """
        Pure deterministic review processor. Same Input -> Same Output.
        """
        if is_demo and demo_type in cls.DEMO_SCENARIOS:
            return cls.DEMO_SCENARIOS[demo_type]

        gaps = []
        hints = []
        score = 0
        
        score += cls._evaluate_title(task.task_title, gaps, hints)
        score += cls._evaluate_description(task.task_description, gaps, hints)
        score += cls._evaluate_markers(task.task_description, gaps, hints)
        score += cls._evaluate_technical_keywords(task.task_description, gaps, hints)

        final_score = min(100, score)
        readiness = int(final_score * 0.85) if final_score < 90 else final_score
        
        summary = f"Analysis complete (Score: {final_score}). "
        if final_score >= 85:
            summary += "Production ready."
        elif final_score >= 60:
            summary += "Minor refinement required."
        else:
            summary += "Major overhaul required."

        return ReviewOutput(
            score=final_score,
            readiness_percent=readiness,
            gaps=gaps,
            improvement_hints=hints,
            reviewer_summary=summary
        )
