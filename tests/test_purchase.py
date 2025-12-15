from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_purchase_suggest():
    r = client.get("/api/purchase/suggest", params={"barcode": "6920459955447"})
    assert r.status_code == 200
    data = r.json()
    assert data["suggest_qty"] == 15