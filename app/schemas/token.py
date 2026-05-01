from pydantic import BaseModel

# lo que devolvemos cuando el login es exitoso
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"