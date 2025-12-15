from sqlalchemy.orm import Session
from app.models.goods import Goods
from app.services import events


def increase_stock(db: Session, barcode: str, qty: int) -> Goods:
    goods = db.query(Goods).filter(Goods.barcode == barcode).first()
    if not goods:
        goods = Goods(barcode=barcode, name=barcode, stock_qty=qty)
        db.add(goods)
    else:
        goods.stock_qty += qty
    db.commit()
    db.refresh(goods)

    # ===== 发布事件（旧代码逻辑零变化） =====
    events.publish("stock_changed", goods.id, goods.barcode, goods.stock_qty)
    return goods
