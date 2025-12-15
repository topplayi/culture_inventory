from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_real_eoq(client):
    # 1. 先插商品
    client.post("/api/stock/in", json={"barcode": "REAL123", "qty": 1})
    # 2. 灌销量
    rows = [{"barcode": "REAL123", "qty": 3}] * 30
    r = client.post("/api/sales/upload", json=rows)
    assert r.status_code == 200
    # 3. 查建议
    r = client.get("/api/purchase/suggest", params={"barcode": "REAL123"})
    assert r.status_code == 200
    data = r.json()
    assert data["daily_sale"] == 3.0
    assert data["suggest_qty"] == 30