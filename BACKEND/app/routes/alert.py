from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.alert import (
    AlertCreate,
    AlertResponse,
    AlertUpdate,
)
from app.services.alert_service import (
    create_alert,
    get_alert_by_id,
    get_all_alerts,
    update_alert_status,
)


router = APIRouter(
    prefix="/api/alerts",
    tags=["Alerts"],
)


@router.post(
    "",
    response_model=AlertResponse,
    status_code=201,
)
def create_new_alert(
    request: AlertCreate,
    db: Session = Depends(get_db),
):
    return create_alert(
        db=db,
        medicine_id=request.medicine_id,
        batch_id=request.batch_id,
        report_id=request.report_id,
        title=request.title,
        message=request.message,
        severity=request.severity,
        priority=request.priority,
        latitude=request.latitude,
        longitude=request.longitude,
        report_count=request.report_count,
    )


@router.get(
    "",
    response_model=list[AlertResponse],
)
def read_all_alerts(
    db: Session = Depends(get_db),
):
    return get_all_alerts(db)


@router.get(
    "/{alert_id}",
    response_model=AlertResponse,
)
def read_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):
    return get_alert_by_id(
        db=db,
        alert_id=alert_id,
    )


@router.patch(
    "/{alert_id}",
    response_model=AlertResponse,
)
def update_alert(
    alert_id: int,
    request: AlertUpdate,
    db: Session = Depends(get_db),
):
    return update_alert_status(
        db=db,
        alert_id=alert_id,
        status=request.status,
    )