from pydantic import BaseModel
from datetime import datetime
from app.models.task import TaskStatus

# datos que el cliente manda para crear una tarea
class TaskCreate(BaseModel):
    title: str
    description: str | None = None
    status: TaskStatus = TaskStatus.pending

# datos que el cliente manda para actualizar, todo opcional
class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None

# datos que devolvemos al cliente
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
    owner_id: int

    model_config = {"from_attributes": True}