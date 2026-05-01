from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_token
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from app.services import task_service
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(prefix="/tasks", tags=["tasks"])

# le dice a fastapi donde esta el endpoint de login para el swagger
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    # decodifica el token y devuelve el id del usuario
    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalido o expirado"
        )
    return int(payload["sub"])

@router.get("/", response_model=list[TaskResponse])
def list_tasks(
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    # devuelve todas las tareas activas del usuario autenticado
    return task_service.get_tasks(db, user_id)

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    data: TaskCreate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    return task_service.create_task(db, data, user_id)

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    task = task_service.update_task(db, task_id, data, user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(get_current_user_id)
):
    ok = task_service.delete_task(db, task_id, user_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")