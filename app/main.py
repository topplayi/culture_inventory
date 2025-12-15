# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.db import engine, Base
from app.models import goods  # 确保模型被 import


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时建表
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.get("/ping")
def ping():
    return "pong"


# === 关键：显式拉起 uvicorn ===
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
