from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_download_slow_goods():
    r = client.get("/api/report/slow.xlsx")
    assert r.status_code == 200
    assert r.headers["content-type"] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert len(r.content) > 0
    assert b"PK" in r.content   # Excel 文件头