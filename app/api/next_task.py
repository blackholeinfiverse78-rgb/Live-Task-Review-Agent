from fastapi import APIRouter, HTTPException
from ..models.schemas import ReviewOutput, NextTask
from ..services.next_task_engine import NextTaskEngine

router = APIRouter()

@router.post("/generate-next", response_model=NextTask)
async def generate_next_task(review: ReviewOutput):
    try:
        return NextTaskEngine.generate_next_task(review)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
