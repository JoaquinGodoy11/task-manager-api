from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings

# motor de conexion a postgres
engine = create_engine(settings.DATABASE_URL)

# fabrica de sesiones, cada request obtiene la suya
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

# dependencia de fastapi, da una sesion y la cierra al terminar
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()