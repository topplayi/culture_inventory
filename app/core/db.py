# 创建引擎、Session
# app/core/db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from .config import settings

engine = create_engine(
    settings.database_url,
    echo=False,          # 调 SQL 时改成 True
    pool_pre_ping=True
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, future=True)
Base = declarative_base()

# 依赖注入用（FastAPI 的 Depends 会调它）
def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()