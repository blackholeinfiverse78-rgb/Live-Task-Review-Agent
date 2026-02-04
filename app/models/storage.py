from typing import Dict
from .schemas import Task

# Simple in-memory storage for Day-1
task_storage: Dict[str, Task] = {}
