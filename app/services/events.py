# 简单发布-订阅，同步模式
_subscribers = []

def subscribe(callback):
    _subscribers.append(callback)

def publish(event: str, goods_id: int, barcode: str, current_qty: int):
    for cb in _subscribers:
        cb(event, goods_id, barcode, current_qty)