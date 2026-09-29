from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.models.user import User


def create_notification(
    db: Session,
    user_id: int,
    title: str,
    message: str,
) -> Notification:

    user = db.execute(
        select(User).where(User.user_id == user_id)
    ).scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        is_read=False,
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification


def get_user_notifications(
    db: Session,
    user_id: int,
) -> list[Notification]:

    user = db.execute(
        select(User).where(User.user_id == user_id)
    ).scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    result = db.execute(
        select(Notification)
        .where(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
    )

    return list(result.scalars().all())


def mark_notification_as_read(
    db: Session,
    notification_id: int,
) -> Notification:

    notification = db.execute(
        select(Notification).where(
            Notification.notification_id == notification_id
        )
    ).scalar_one_or_none()

    if notification is None:
        raise HTTPException(
            status_code=404,
            detail="Notification not found",
        )

    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification