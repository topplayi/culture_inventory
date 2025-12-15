from sqlalchemy.orm import Session
from app.models.goods import Goods

def suggest(db: Session, goods_id: int) -> int:
    """
    假销量 0.5 盒/天，提前期 30 天，写死 15 盒
    后续换成真实统计/EOQ 公式即可
    """
    goods = db.get(Goods, goods_id)
    if not goods:
        return 0
    # 写死建议量
    return 15