import os, sys, pytest
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool
from sqlalchemy.orm import sessionmaker, scoped_session
from app.core.db import Base, get_session
from app.main import app

engine = create_engine(
    "sqlite:///:memory:",
    poolclass=StaticPool,
    connect_args={"check_same_thread": False},
    echo=False
)
Base.metadata.create_all(bind=engine)
TestingSessionLocal = scoped_session(sessionmaker(bind=engine, autoflush=False, expire_on_commit=False))

def override_get_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_session] = override_get_session

# 关键：声明 fixture
@pytest.fixture(scope="function")
def client() -> TestClient:
    return TestClient(app)