# 报表导出
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.services.report_service import export_inventory
from app.services.report_service import export_inventory, export_slow_goods
from app.core.db import get_session

router = APIRouter(prefix="/api/report", tags=["report"])

@router.get("/inventory.xlsx", summary="库存台账导出")
def download_inventory(db: Session = Depends(get_session)):
    content = export_inventory(db)
    return StreamingResponse(
        iter([content]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=inventory.xlsx"}
    )

@router.get("/slow.xlsx", summary="滞销品导出")
def download_slow_goods(db: Session = Depends(get_session)):
    content = export_slow_goods(db)
    return StreamingResponse(
        iter([content]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=slow_goods.xlsx"}
    )