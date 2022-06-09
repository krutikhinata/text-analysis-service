from typing import Dict, Optional, Union

from pydantic import BaseModel


class TaskCreated(BaseModel):
    task_id: str


class TaskTrigger(BaseModel):
    task_name: str
    parameters: Optional[Dict[str, Union[str, int, float]]] = {}
