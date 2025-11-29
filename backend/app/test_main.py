from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}

def test_upload_document():
    file_content = b"pdf content"
    data = {
        "user_id": "test1",
        "email": "demo@youvisa.com"
    }
    files = {
        "file": ("passaporte.pdf", file_content, "application/pdf")
    }
    resp = client.post("/upload", data=data, files=files)
    assert resp.status_code == 200
    data_ret = resp.json()
    assert "case_id" in data_ret
    assert data_ret["status"] in ["Validado", "Recebido"]

def test_get_cases():
    resp = client.get("/cases")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)
