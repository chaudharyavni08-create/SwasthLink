from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.medicine import Medicine
from app.models.medicine_batch import MedicineBatch
from app.models.report import Report


def create_alert(
    db: Session,
    medicine_id: int | None,
    batch_id: int | None,
    report_id: int | None,
    title: str,
    message: str,
    severity: str,
    priority: str,
    latitude: float | None,
    longitude: float | None,
    report_count: int,
) -> Alert:

    severity = severity.upper()
    priority = priority.upper()

    if severity not in {"LOW", "MEDIUM", "HIGH"}:
        raise HTTPException(
            status_code=400,
            detail="Severity must be LOW, MEDIUM, or HIGH",
        )

    if priority not in {"LOW", "MEDIUM", "HIGH"}:
        raise HTTPException(
            status_code=400,
            detail="Priority must be LOW, MEDIUM, or HIGH",
        )

    if report_count < 1:
        raise HTTPException(
            status_code=400,
            detail="Report count must be at least 1",
        )

    if medicine_id is not None:
        medicine = db.execute(
            select(Medicine).where(
                Medicine.medicine_id == medicine_id
            )
        ).scalar_one_or_none()

        if medicine is None:
            raise HTTPException(
                status_code=404,
                detail="Medicine not found",
            )

    if batch_id is not None:
        batch = db.execute(
            select(MedicineBatch).where(
                MedicineBatch.batch_id == batch_id
            )
        ).scalar_one_or_none()

        if batch is None:
            raise HTTPException(
                status_code=404,
                detail="Batch not found",
            )

    if report_id is not None:
        report = db.execute(
            select(Report).where(
                Report.report_id == report_id
            )
        ).scalar_one_or_none()

        if report is None:
            raise HTTPException(
                status_code=404,
                detail="Report not found",
            )

    alert = Alert(
        medicine_id=medicine_id,
        batch_id=batch_id,
        report_id=report_id,
        title=title,
        message=message,
        severity=severity,
        priority=priority,
        latitude=latitude,
        longitude=longitude,
        report_count=report_count,
        status="ACTIVE",
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


def get_all_alerts(
    db: Session,
) -> list[Alert]:

    result = db.execute(
        select(Alert).order_by(
            Alert.created_at.desc()
        )
    )

    return list(result.scalars().all())


def get_alert_by_id(
    db: Session,
    alert_id: int,
) -> Alert:

    alert = db.execute(
        select(Alert).where(
            Alert.alert_id == alert_id
        )
    ).scalar_one_or_none()

    if alert is None:
        raise HTTPException(
            status_code=404,
            detail="Alert not found",
        )

    return alert


def update_alert_status(
    db: Session,
    alert_id: int,
    status: str,
) -> Alert:

    status = status.upper()

    if status not in {
        "ACTIVE",
        "RESOLVED",
        "DISMISSED",
    }:
        raise HTTPException(
            status_code=400,
            detail="Status must be ACTIVE, RESOLVED, or DISMISSED",
        )

    alert = get_alert_by_id(
        db=db,
        alert_id=alert_id,
    )

    alert.status = status

    db.commit()
    db.refresh(alert)

    return alert