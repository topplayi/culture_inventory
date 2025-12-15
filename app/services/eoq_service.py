from datetime import date, timedelta
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.models.sales import Sales
from app.models.goods import Goods

def suggest(db: Session, goods_id: int, lead_days: int = 7, safety_days: int = 3) -> dict:
    """
    真实 EOQ 建议：
    1. 30 天日均销量
    2. 建议量 = 日均 × (lead_days + safety_days)
    返回 dict 方便前端展示参数
    """
    goods = db.get(Goods, goods_id)
    if not goods:
        return {"suggest_qty": 0, "daily_sale": 0, "lead_days": lead_days, "safety_days": safety_days}

    start = date.today() - timedelta(days=30)
    total = (
        db.query(func.coalesce(func.sum(Sales.qty), 0))
        .filter(Sales.barcode == goods.barcode, Sales.sale_date >= start)
        .scalar()
    )
    daily_sale = total / 30 if total else 0
    suggest_qty = max(0, round(daily_sale * (lead_days + safety_days)))
    return {
        "suggest_qty": suggest_qty,
        "daily_sale": round(daily_sale, 2),
        "lead_days": lead_days,
        "safety_days": safety_days
    }