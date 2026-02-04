"""
FEATURE FREEZE COMPLETE - DEMO-ONLY MODE
Locked on: 2026-02-02
Logic: Score-Tiered Transitions
"""
from ..models.schemas import ReviewOutput, NextTask

class NextTaskEngine:
    @staticmethod
    def generate_next_task(review: ReviewOutput) -> NextTask:
        """
        Deterministic transition logic based on Review result.
        """
        if review.score < 50:
            return NextTask(
                next_task_title="Task Refinement Phase",
                next_task_description="Deepen description with specific requirements and success criteria.",
                difficulty_level="easy",
                rationale="Low score requires building foundational clarity."
            )
        elif review.score < 85:
            return NextTask(
                next_task_title="Technical Architecture Design",
                next_task_description="Draft a high-level architecture diagram and component interaction map.",
                difficulty_level="medium",
                rationale="Foundation is adequate. Moving to implementation planning."
            )
        else:
            return NextTask(
                next_task_title="Production Implementation",
                next_task_description="Execute implementation with comprehensive unit and integration tests.",
                difficulty_level="hard",
                rationale="High readiness justifies proceeding to production."
            )
