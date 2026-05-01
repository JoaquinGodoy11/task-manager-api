import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import Base, get_db

# base de datos en memoria solo para tests, no toca la de desarrollo
SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(autouse=True)
def setup_db():
    # crea las tablas antes de cada test y las borra al terminar
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def client(db):
    # reemplaza la db real por la de test en cada request
    def override_get_db():
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def usuario_registrado(client):
    # crea un usuario de prueba y devuelve sus datos
    client.post("/auth/register", json={
        "email": "test@test.com",
        "username": "testuser",
        "password": "password123"
    })
    return {"email": "test@test.com", "password": "password123"}

@pytest.fixture
def token(client, usuario_registrado):
    # hace login y devuelve el token listo para usar
    res = client.post("/auth/login", json=usuario_registrado)
    return res.json()["access_token"]

@pytest.fixture
def auth_headers(token):
    # headers con el token para los endpoints protegidos
    return {"Authorization": f"Bearer {token}"}