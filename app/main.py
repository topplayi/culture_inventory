# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.db import engine, Base
from app.api import stock  # 新增：引入路由模块
from app.services.alert_service import init_alert
from app.api import stock, purchase
from app.models import goods  # 确保模型被导入


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时建表
    Base.metadata.create_all(bind=engine)
    init_alert()
    yield
    engine.dispose()


app = FastAPI(lifespan=lifespan)

# 注册路由
app.include_router(stock.router)
app.include_router(purchase.router)

@app.get("/ping")
def ping():
    return "xxx"


# 本地调试入口
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")