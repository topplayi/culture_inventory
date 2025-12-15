# 采购建议、生单
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.eoq_service import suggest
from app.core.db import get_session
from app.models.goods import Goods

router = APIRouter(prefix="/api/purchase", tags=["purchase"])

@router.get("/suggest", summary="采购建议（假数据版）")
def purchase_suggest(barcode: str, db: Session = Depends(get_session)):
    goods = db.query(Goods).filter(Goods.barcode == barcode).first()
    if not goods:
        raise HTTPException(status_code=404, detail="条码不存在")
    qty = suggest(db, goods.id)
    return {"barcode": goods.barcode,
            "name": goods.name,
            "current_stock": goods.stock_qty,
            "suggest_qty": qty}