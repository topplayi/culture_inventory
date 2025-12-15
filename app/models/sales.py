from sqlalchemy import Column, Integer, String, Date, func
from app.core.db import Base


class Sales(Base):
    __tablename__ = "sales"
    id = Column(Integer, primary_key=True)
    barcode = Column(String(32), nullable=False, index=True)
    qty = Column(Integer, nullable=False)  # 当日销量
    sale_date = Column(Date, nullable=False, default=func.current_date(), index=True)
