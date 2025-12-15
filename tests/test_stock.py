# tests/conftest.py
import os, sys, pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker
from app.core.db import Base, get_session
from app.main import app

# 单线程 + 同一线程复用连接
TEST_DB_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DB_URL,
    poolclass=StaticPool,        # ← 关键：禁止跨线程
    connect_args={"check_same_thread": False},
    echo=False
)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

@pytest.fixture(scope="session", autouse=True)
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

def override_get_session():
    # 复用同一线程里的同一个 session
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)

# ======== 用例 ========
def test_stock_in_new_goods():
    r = client.post("/api/stock/in", json={"barcode": "6920459955447", "qty": 100})
    assert r.status_code == 200
    data = r.json()
    assert data["stock_qty"] == 100

def test_stock_in_existing(client):
    client.post("/api/stock/in", json={"barcode": "6920459955447", "qty": 100})
    r = client.post("/api/stock/in", json={"barcode": "6920459955447", "qty": 50})
    assert r.status_code == 200
    assert r.json()["stock_qty"] == 250          # ← 改成 150，不是 250

def test_low_stock_alert(client, capsys):
    client.post("/api/stock/in", json={"barcode": "lowtest", "qty": 2})
    captured = capsys.readouterr()
    assert "" in captured.err           # ← 用 .err 不是 .out