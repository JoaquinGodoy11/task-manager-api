from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # datos de conexion a la base
    DATABASE_URL: str
    # clave secreta para firmar los tokens
    SECRET_KEY: str
    # algoritmo de encriptacion del token
    ALGORITHM: str = "HS256"
    # cuanto dura el token en minutos
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"

# instancia global que usan todos los modulos
settings = Settings()