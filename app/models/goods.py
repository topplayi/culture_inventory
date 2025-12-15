# app/models/goods.py
from sqlalchemy import Column, Integer, String, Numeric, DateTime, func
from app.core.db import Base


class Goods(Base):
    __tablename__ = "goods"

    id = Column(Integer, primary_key=True, index=True)
    barcode = Column(String(32), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=False)
    unit = Column(String(10), default="个")
    price = Column(Numeric(10, 2), default=0)
    stock_qty = Column(Integer, default=0)
    min_qty = Column(Integer, default=10)  # 安全库存
    created_at = Column(DateTime, server_default=func.now())
