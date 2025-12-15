from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_download_inventory():
    r = client.get("/api/report/inventory.xlsx")
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert len(r.content) > 0        # 有字节即可
    assert b"PK" in r.content        # Excel 文件头