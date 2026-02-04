"""
FEATURE FREEZE COMPLETE - DEMO-ONLY MODE
Locked on: 2026-02-02
Version: 1.1.0 (PROD-LOCKED)
"""
from pydantic import BaseModel, Field, field_validator
from datetime import datetime
from typing import List, Optional

class TaskBase(BaseModel):
    task_title: str = Field(..., min_length=5, max_length=100)
    task_description: str = Field(..., min_length=10, max_length=2000)
    submitted_by: str = Field(..., min_length=2, max_length=50)

    @field_validator('task_title', 'task_description', 'submitted_by')
    @classmethod
    def prevent_empty_whitespace(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Field cannot be empty or just whitespace")
        return v.strip()

class TaskCreate(TaskBase):
    is_demo: bool = Field(default=False)
    demo_type: Optional[str] = Field(default=None)

class Task(TaskBase):
    task_id: str
    timestamp: datetime

class ReviewOutput(BaseModel):
    score: int = Field(..., ge=0, le=100)
    readiness_percent: int = Field(..., ge=0, le=100)
    gaps: List[str] = Field(default_factory=list)
    improvement_hints: List[str] = Field(default_factory=list)
    reviewer_summary: str

class NextTask(BaseModel):
    next_task_title: str
    next_task_description: str
    difficulty_level: str
    rationale: str
