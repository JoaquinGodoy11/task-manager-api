from pydantic import BaseModel, EmailStr
from datetime import datetime

# datos que el cliente manda para registrarse
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

# datos que devolvemos al cliente, nunca el password
class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    is_active: bool
    created_at: datetime

    model_config = {"from_attributes": True}

# datos para el login
class UserLogin(BaseModel):
    email: EmailStr
    password: str