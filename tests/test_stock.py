from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_stock_in_new_goods():
    """新条码首次入库"""
    r = client.post("/api/stock/in", json={"barcode": "6920459955447", "qty": 100})
    assert r.status_code == 200
    data = r.json()
    assert data["barcode"] == "6920459955447"
    assert data["stock_qty"] == 100

def test_stock_in_existing():
    """同条码再次入库"""
    r = client.post("/api/stock/in", json={"barcode": "6920459955447", "qty": 50})
    assert r.status_code == 200
    assert r.json()["stock_qty"] == 150      # 100+50