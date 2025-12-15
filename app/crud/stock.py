from sqlalchemy.orm import Session
from app.models.goods import Goods

def increase_stock(db: Session, barcode: str, qty: int) -> Goods:
    """返回更新后的 Goods 对象；若条码不存在则自动创建（库存=qty，其余默认）"""
    goods = db.query(Goods).filter(Goods.barcode == barcode).first()
    if not goods:
        goods = Goods(barcode=barcode, stock_qty=qty)
        db.add(goods)
    else:
        goods.stock_qty += qty
    db.commit()
    db.refresh(goods)
    return goods

def increase_stock(db: Session, barcode: str, qty: int) -> Goods:
    goods = db.query(Goods).filter(Goods.barcode == barcode).first()
    if not goods:
        # 新建时把 name 先填成 barcode 本身，后续可再人工改
        goods = Goods(barcode=barcode, name=barcode, stock_qty=qty)
        db.add(goods)
    else:
        goods.stock_qty += qty
    db.commit()
    db.refresh(goods)
    return goods