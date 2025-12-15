from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.goods import Goods
from io import BytesIO
import pandas as pd
from app.services.slow_service import list_slow_goods

def export_inventory(db: Session) -> bytes:
    """返回字节流：库存台账 Excel"""
    stmt = select(Goods.barcode, Goods.name, Goods.stock_qty, Goods.price)
    rows = db.execute(stmt).all()

    df = pd.DataFrame(rows, columns=["条码", "名称", "库存数量", "单价"])
    df["库存金额"] = df["库存数量"] * df["单价"]

    bio = BytesIO()
    with pd.ExcelWriter(bio, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="库存台账", index=False)
    bio.seek(0)
    return bio.read()


def export_slow_goods(db) -> bytes:
    goods = list_slow_goods(db)
    df = pd.DataFrame(
        [(g.barcode, g.name, g.stock_qty, g.price, g.stock_qty * g.price) for g in goods],
        columns=["条码", "名称", "库存数量", "单价", "库存金额"]
    )
    bio = BytesIO()
    with pd.ExcelWriter(bio, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="滞销品", index=False)
    bio.seek(0)
    return bio.read()