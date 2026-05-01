def test_registro_exitoso(client):
    res = client.post("/auth/register", json={
        "email": "nuevo@test.com",
        "username": "nuevo",
        "password": "password123"
    })
    assert res.status_code == 201
    assert res.json()["email"] == "nuevo@test.com"

def test_registro_email_duplicado(client, usuario_registrado):
    res = client.post("/auth/register", json={
        "email": "test@test.com",
        "username": "otro",
        "password": "password123"
    })
    assert res.status_code == 400

def test_login_exitoso(client, usuario_registrado):
    res = client.post("/auth/login", json=usuario_registrado)
    assert res.status_code == 200
    assert "access_token" in res.json()

def test_login_credenciales_incorrectas(client):
    res = client.post("/auth/login", json={
        "email": "noexiste@test.com",
        "password": "mal"
    })
    assert res.status_code == 401

def test_crear_tarea(client, auth_headers):
    res = client.post("/tasks/", json={
        "title": "Tarea de prueba",
        "description": "Descripcion",
        "status": "pending"
    }, headers=auth_headers)
    assert res.status_code == 201
    assert res.json()["title"] == "Tarea de prueba"

def test_listar_tareas(client, auth_headers):
    client.post("/tasks/", json={"title": "Tarea 1"}, headers=auth_headers)
    client.post("/tasks/", json={"title": "Tarea 2"}, headers=auth_headers)
    res = client.get("/tasks/", headers=auth_headers)
    assert res.status_code == 200
    assert len(res.json()) == 2

def test_actualizar_tarea(client, auth_headers):
    tarea = client.post("/tasks/", json={"title": "Original"}, headers=auth_headers).json()
    res = client.put(f"/tasks/{tarea['id']}", json={"title": "Actualizada"}, headers=auth_headers)
    assert res.status_code == 200
    assert res.json()["title"] == "Actualizada"

def test_eliminar_tarea(client, auth_headers):
    tarea = client.post("/tasks/", json={"title": "A eliminar"}, headers=auth_headers).json()
    res = client.delete(f"/tasks/{tarea['id']}", headers=auth_headers)
    assert res.status_code == 204

def test_tarea_no_accesible_por_otro_usuario(client):
    # usuario 1 crea una tarea
    client.post("/auth/register", json={"email": "u1@test.com", "username": "u1", "password": "pass123"})
    token1 = client.post("/auth/login", json={"email": "u1@test.com", "password": "pass123"}).json()["access_token"]
    tarea = client.post("/tasks/", json={"title": "Privada"}, headers={"Authorization": f"Bearer {token1}"}).json()

    # usuario 2 intenta acceder a la tarea del usuario 1
    client.post("/auth/register", json={"email": "u2@test.com", "username": "u2", "password": "pass123"})
    token2 = client.post("/auth/login", json={"email": "u2@test.com", "password": "pass123"}).json()["access_token"]
    res = client.delete(f"/tasks/{tarea['id']}", headers={"Authorization": f"Bearer {token2}"})
    assert res.status_code == 404

def test_sin_token_retorna_401(client):
    res = client.get("/tasks/")
    assert res.status_code == 401

def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200