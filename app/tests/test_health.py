from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_envelope():
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["code"] == 0
    assert body["data"]["status"] == "ok"
    assert "request_id" in body
    assert "timestamp" in body
