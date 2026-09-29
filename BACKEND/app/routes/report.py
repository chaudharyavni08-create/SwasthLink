from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.report import (
    ReportCreate,
    ReportResponse,
    ReportStatusUpdate,
)
from app.services.report_service import (
    create_report,
    get_report_by_id,
    get_user_reports,
    update_report_status,
)
from app.utils.dependencies import get_current_user


router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"],
)


@router.post(
    "",
    response_model=ReportResponse,
    status_code=201,
)
def create_new_report(
    request: ReportCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_report(
        db=db,
        user_id=current_user.user_id,
        medicine_id=request.medicine_id,
        batch_id=request.batch_id,
        verification_id=request.verification_id,
        reason=request.reason,
        evidence_image_url=request.evidence_image_url,
        latitude=request.latitude,
        longitude=request.longitude,
        severity=request.severity,
    )


@router.get(
    "/user/{user_id}",
    response_model=list[ReportResponse],
)
def read_user_reports(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Admin can view any user's reports
    if current_user.role_id != 2 and current_user.user_id != user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only access your own reports",
        )

    return get_user_reports(
        db=db,
        user_id=user_id,
    )


@router.get(
    "/{report_id}",
    response_model=ReportResponse,
)
def read_report(
    report_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    report = get_report_by_id(
        db=db,
        report_id=report_id,
    )

    # Admin can view any report
    if current_user.role_id != 2 and report.user_id != current_user.user_id:
        raise HTTPException(
            status_code=403,
            detail="You can only access your own report",
        )

    return report


@router.patch(
    "/{report_id}",
    response_model=ReportResponse,
)
def update_report(
    report_id: int,
    request: ReportStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_report_status(
        db=db,
        report_id=report_id,
        new_status=request.status,
        admin_user_id=current_user.user_id,
    )