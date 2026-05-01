from fastapi import FastAPI
from app.routers import auth, tasks
from app.core.database import engine, Base

# crea las tablas si no existen, en produccion esto lo haria alembic
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Task Manager API",
    description="REST API con autenticacion JWT y gestion de tareas",
    version="1.0.0"
)

# registra los routers con sus prefijos
app.include_router(auth.router)
app.include_router(tasks.router)

@app.get("/health")
def health():
    # endpoint para verificar que la app esta viva
    return {"status": "ok"}