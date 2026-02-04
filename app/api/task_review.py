from fastapi import APIRouter, HTTPException, Body
from typing import Optional
import logging
from ..models.schemas import Task, ReviewOutput, TaskCreate
from ..models.storage import task_storage
from ..services.review_engine import ReviewEngine
from datetime import datetime
import uuid

router = APIRouter()
logger = logging.getLogger("task_review_system")

@router.post("/review", response_model=ReviewOutput)
async def review_task(
    task_id: Optional[str] = Body(None),
    payload: Optional[TaskCreate] = Body(None)
):
    try:
        target_task = None
        is_demo = False
        demo_type = None
        
        if task_id:
            entry = task_storage.get(task_id)
            if not entry:
                logger.warning(f"Task review requested for non-existent ID: {task_id}")
                raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
            
            # Extract task and metadata
            if isinstance(entry, dict):
                target_task = entry["task"]
                is_demo = entry.get("is_demo", False)
                demo_type = entry.get("demo_type")
            else:
                target_task = entry
        elif payload:
            logger.info("Ad-hoc review requested with raw payload")
            target_task = Task(
                task_id="adhoc-" + str(uuid.uuid4())[:8],
                task_title=payload.task_title,
                task_description=payload.task_description,
                submitted_by=payload.submitted_by,
                timestamp=datetime.now()
            )
            is_demo = payload.is_demo
            demo_type = payload.demo_type
        else:
            raise HTTPException(status_code=400, detail="Must provide either task_id or payload")
            
        return ReviewEngine.review_task(target_task, is_demo=is_demo, demo_type=demo_type)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Review execution failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Review process failed. Please retry.")
