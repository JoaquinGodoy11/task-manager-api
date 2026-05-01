from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password

def get_user_by_email(db: Session, email: str) -> User | None:
    # busca usuario por email, devuelve None si no existe
    return db.query(User).filter(User.email == email).first()

def get_user_by_username(db: Session, username: str) -> User | None:
    # busca usuario por username
    return db.query(User).filter(User.username == username).first()

def create_user(db: Session, data: UserCreate) -> User:
    # verifica que email y username no esten ocupados
    if get_user_by_email(db, data.email):
        raise ValueError("Email ya registrado")
    if get_user_by_username(db, data.username):
        raise ValueError("Username ya registrado")

    # crea el usuario con el password hasheado
    user = User(
        email=data.email,
        username=data.username,
        hashed_password=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> User | None:
    # busca el usuario y verifica el password
    user = get_user_by_email(db, email)
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user