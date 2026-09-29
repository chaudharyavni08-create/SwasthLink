from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.audit_log import AuditLog
from app.models.medicine import Medicine
from app.models.medicine_batch import MedicineBatch
from app.models.medicine_verification import MedicineVerification
from app.models.notification import Notification
from app.models.report import Report
from app.models.user import User


VALID_REPORT_STATUSES = {
    "OPEN",
    "UNDER_REVIEW",
    "RESOLVED",
    "REJECTED",
}

VALID_SEVERITIES = {
    "LOW",
    "MEDIUM",
    "HIGH",
}


def create_report(
    db: Session,
    user_id: int,
    medicine_id: int | None,
    batch_id: int | None,
    verification_id: int | None,
    reason: str,
    evidence_image_url: str | None,
    latitude: float | None,
    longitude: float | None,
    severity: str | None,
) -> Report:

    user = db.execute(
        select(User).where(User.user_id == user_id)
    ).scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
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

    if verification_id is not None:
        verification = db.execute(
            select(MedicineVerification).where(
                MedicineVerification.verification_id == verification_id
            )
        ).scalar_one_or_none()

        if verification is None:
            raise HTTPException(
                status_code=404,
                detail="Verification not found",
            )

    if severity is not None:
        severity = severity.upper()

        if severity not in VALID_SEVERITIES:
            raise HTTPException(
                status_code=400,
                detail="Severity must be LOW, MEDIUM, or HIGH",
            )

    reason = reason.strip()

    if not reason:
        raise HTTPException(
            status_code=400,
            detail="Reason cannot be empty",
        )

    report = Report(
        user_id=user_id,
        medicine_id=medicine_id,
        batch_id=batch_id,
        verification_id=verification_id,
        reason=reason,
        status="OPEN",
        evidence_image_url=evidence_image_url,
        latitude=latitude,
        longitude=longitude,
        severity=severity,
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report


def get_user_reports(
    db: Session,
    user_id: int,
) -> list[Report]:

    user = db.execute(
        select(User).where(User.user_id == user_id)
    ).scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    result = db.execute(
        select(Report)
        .where(Report.user_id == user_id)
        .order_by(Report.created_at.desc())
    )

    return list(result.scalars().all())


def get_report_by_id(
    db: Session,
    report_id: int,
) -> Report:

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

    return report


def update_report_status(
    db: Session,
    report_id: int,
    new_status: str,
    admin_user_id: int,
) -> Report:

    # -----------------------------------
    # 1. Verify admin user
    # -----------------------------------
    admin = db.execute(
        select(User).where(
            User.user_id == admin_user_id,
            User.is_active.is_(True),
        )
    ).scalar_one_or_none()

    if admin is None:
        raise HTTPException(
            status_code=404,
            detail="Admin user not found or inactive",
        )

    if admin.role_id != 2:
        raise HTTPException(
            status_code=403,
            detail="Only admins can update report status",
        )

    # -----------------------------------
    # 2. Validate status
    # -----------------------------------
    new_status = new_status.upper()

    if new_status not in VALID_REPORT_STATUSES:
        raise HTTPException(
            status_code=400,
            detail="Status must be OPEN, UNDER_REVIEW, RESOLVED, or REJECTED",
        )

    # -----------------------------------
    # 3. Get report
    # -----------------------------------
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

    old_status = report.status

    # -----------------------------------
    # 4. Update report
    # -----------------------------------
    report.status = new_status

    # -----------------------------------
    # 5. Update linked alert
    # -----------------------------------
    alert = db.execute(
        select(Alert).where(
            Alert.report_id == report.report_id
        )
    ).scalar_one_or_none()

    if alert is not None:

        if new_status == "RESOLVED":
            alert.status = "RESOLVED"

        elif new_status == "REJECTED":
            alert.status = "DISMISSED"

        else:
            alert.status = "ACTIVE"

    # -----------------------------------
    # 6. Create user notification
    # -----------------------------------
    notification_title = "Report Status Updated"

    notification_message = (
        f"Your medicine report #{report.report_id} "
        f"status changed from {old_status} to {new_status}."
    )

    notification = Notification(
        user_id=report.user_id,
        title=notification_title,
        message=notification_message,
        is_read=False,
    )

    db.add(notification)

    # -----------------------------------
    # 7. Create audit log
    # -----------------------------------
    audit_log = AuditLog(
        user_id=admin_user_id,
        action="REPORT_STATUS_UPDATED",
        entity_type="REPORT",
        entity_id=report.report_id,
    )

    db.add(audit_log)

    # -----------------------------------
    # 8. Save everything together
    # -----------------------------------
    db.commit()
    db.refresh(report)

    return report