from sqlalchemy.orm import Session
from app.services import events
from app.models.goods import Goods

def low_stock_handler(event: str, goods_id: int, barcode: str, current_qty: int):
    """回调：当前库存 <= 安全库存就写日志/发通知"""
    if event != "stock_changed":
        return
    # 查安全库存
    from app.core.db import SessionLocal   # 避免循环 import
    db: Session = SessionLocal()
    goods = db.query(Goods).filter(Goods.id == goods_id).first()
    db.close()
    if goods and current_qty <= goods.min_qty:
        # 这里先打印，后期可改邮件/微信
        msg = f"[预警] {barcode} 库存={current_qty} <= 安全库存={goods.min_qty}"
        print(msg)          # 日志也能抓到
        # todo: 写 alert_log 表 / 发企业微信

# 启动时注册一次即可
def init_alert():
    events.subscribe(low_stock_handler)