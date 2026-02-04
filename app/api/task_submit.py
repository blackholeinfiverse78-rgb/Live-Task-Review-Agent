from fastapi import APIRouter, HTTPException
from datetime import datetime
import uuid
import logging
from ..models.schemas import TaskCreate, Task
from ..models.storage import task_storage

router = APIRouter()
logger = logging.getLogger("task_review_system")

@router.post("/submit", response_model=Task)
async def submit_task(payload: TaskCreate):
    try:
        logger.info(f"Received task submission from '{payload.submitted_by}'. Demo: {payload.is_demo}")
        
        task_id = str(uuid.uuid4())
        new_task = Task(
            task_id=task_id,
            task_title=payload.task_title,
            task_description=payload.task_description,
            submitted_by=payload.submitted_by,
            timestamp=datetime.now()
        )
        
        # Store demo metadata in task if provided (simplified for Day-2)
        # In a real system, this would be a separate field or a prefix in ID
        task_storage[task_id] = {
            "task": new_task,
            "is_demo": payload.is_demo,
            "demo_type": payload.demo_type
        }
        
        logger.info(f"Task stored successfully. ID: {task_id}")
        return new_task
    except Exception as e:
        logger.error(f"Failed to submit task: {str(e)}")
        raise HTTPException(status_code=500, detail="Submission failed. Please check input parameters.")
