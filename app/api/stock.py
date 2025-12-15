# 出入库、盘点
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.goods import StockInReq
from app.crud.stock import increase_stock
from app.core.db import get_session

router = APIRouter(prefix="/api/stock", tags=["stock"])

@router.post("/in", summary="扫码入库")
def stock_in(req: StockInReq, db: Session = Depends(get_session)):
    goods = increase_stock(db, req.barcode, req.qty)
    return {"barcode": goods.barcode, "name": goods.name, "stock_qty": goods.stock_qty}