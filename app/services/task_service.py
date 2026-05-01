from sqlalchemy.orm import Session
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate

def get_tasks(db: Session, owner_id: int) -> list[Task]:
    # trae solo las tareas activas del usuario
    return db.query(Task).filter(
        Task.owner_id == owner_id,
        Task.is_active == True
    ).all()

def get_task(db: Session, task_id: int, owner_id: int) -> Task | None:
    # trae una tarea especifica verificando que sea del usuario
    return db.query(Task).filter(
        Task.id == task_id,
        Task.owner_id == owner_id,
        Task.is_active == True
    ).first()

def create_task(db: Session, data: TaskCreate, owner_id: int) -> Task:
    # crea la tarea asociada al usuario
    task = Task(**data.model_dump(), owner_id=owner_id)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def update_task(db: Session, task_id: int, data: TaskUpdate, owner_id: int) -> Task | None:
    # actualiza solo los campos que el cliente mando
    task = get_task(db, task_id, owner_id)
    if not task:
        return None
    for field, value in data.model_dump(exclude_none=True).items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, task_id: int, owner_id: int) -> bool:
    # borrado logico, no eliminamos el registro de la base
    task = get_task(db, task_id, owner_id)
    if not task:
        return False
    task.is_active = False
    db.commit()
    return True