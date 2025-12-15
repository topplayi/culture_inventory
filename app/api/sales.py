from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.models.sales import Sales
from app.core.db import get_session

router = APIRouter(prefix="/api/sales", tags=["sales"])

@router.post("/upload", summary="批量录入当日销量")
def upload_sales(rows: list[dict], sale_date: date = date.today(), db: Session = Depends(get_session)):
    """
    前端传数组：[{"barcode":"692...","qty":20}, ...]
    先删旧数据再插入，方便重复导入
    """
    db.query(Sales).filter(Sales.sale_date == sale_date).delete()
    for r in rows:
        db.add(Sales(barcode=r["barcode"], qty=r["qty"], sale_date=sale_date))
    db.commit()
    return {"date": sale_date, "count": len(rows)}