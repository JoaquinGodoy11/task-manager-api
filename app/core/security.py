from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

# contexto para hashear passwords con bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # convierte password plano en hash seguro
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    # compara password plano contra el hash guardado
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict) -> str:
    # copia los datos y agrega fecha de expiracion
    payload = data.copy()
    expira = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({"exp": expira})
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict | None:
    # decodifica el token, devuelve None si es invalido o expiro
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None