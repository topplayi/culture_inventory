# tests/conftest.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.db import Base, get_session
from app.main import app
from fastapi.testclient import TestClient

TEST_DB_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DB_URL, pool_pre_ping=True, echo=False)
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

@pytest.fixture(scope="session", autouse=True)
def create_tables():
    """session开始前只建一次表"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db():
    """function级事务，回滚不污染别的用例"""
    conn = engine.connect()
    trans = conn.begin()
    sess = TestingSessionLocal(bind=conn)
    try:
        yield sess
    finally:
        sess.close()
        trans.rollback()
        conn.close()

@pytest.fixture(scope="function")
def client(db) -> TestClient:
    """复写依赖，返回FastAPI测试客户端"""
    app.dependency_overrides[get_session] = lambda: db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()