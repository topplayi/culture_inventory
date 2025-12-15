from datetime import date, timedelta
from sqlalchemy import func, and_
from sqlalchemy.orm import Session
from app.models.goods import Goods
from app.models.sales import Sales

def list_slow_goods(db: Session, days: int = 30):
    """返回滞销 SKU 列表（连续 days 天无销量且库存>0）"""
    cutoff_date = date.today() - timedelta(days=days)
    # 最近 days 天有销量的条码
    recent = (
        db.query(Sales.barcode)
        .filter(Sales.sale_date >= cutoff_date)
        .group_by(Sales.barcode)
        .subquery()
    )
    # 滞销 = 库存>0 且 不在 recent 里
    slow = (
        db.query(Goods)
        .filter(
            and_(
                Goods.stock_qty > 0,
                Goods.barcode.not_in(recent)
            )
        )
        .all()
    )
    return slow