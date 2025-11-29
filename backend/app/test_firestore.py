from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_case():
    payload = {
        "user_id": "98765",
        "channel": "web",
        "status": "aberto",
        "email": "test@youvisa.com"
    }
    response = client.post("/cases", data=payload)
    assert response.status_code == 200
    result = response.json()
    assert "id" in result

# Pruebas de otros endpoints pueden agregarse siguiendo el mismo patrón
