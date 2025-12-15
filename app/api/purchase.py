# 采购建议、生单
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.services.eoq_service import suggest
from app.core.db import get_session
from app.models.goods import Goods

router = APIRouter(prefix="/api/purchase", tags=["purchase"])

@router.get("/suggest", summary="采购建议（真实销量版）")
def purchase_suggest(
    barcode: str,
    lead_days: int = 7,
    safety_days: int = 3,
    db: Session = Depends(get_session)
):
    goods = db.query(Goods).filter(Goods.barcode == barcode).first()
    if not goods:
        raise HTTPException(status_code=404, detail="条码不存在")
    data = suggest(db, goods.id, lead_days, safety_days)   # ← 只改这一行
    return {
        "barcode": goods.barcode,
        "name": goods.name,
        "current_stock": goods.stock_qty,
        **data
    }