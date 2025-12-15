from pydantic import BaseModel, Field

class StockInReq(BaseModel):
    barcode: str = Field(..., min_length=1, max_length=32, description="商品条码")
    qty: int = Field(..., gt=0, description="入库数量")