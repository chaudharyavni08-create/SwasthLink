from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.notification import (
    NotificationCreate,
    NotificationResponse,
)
from app.services.notification_service import (
    create_notification,
    get_user_notifications,
    mark_notification_as_read,
)


router = APIRouter(
    prefix="/api/notifications",
    tags=["Notifications"],
)


@router.post(
    "",
    response_model=NotificationResponse,
    status_code=201,
)
def create_new_notification(
    request: NotificationCreate,
    db: Session = Depends(get_db),
):
    return create_notification(
        db=db,
        user_id=request.user_id,
        title=request.title,
        message=request.message,
    )


@router.get(
    "/user/{user_id}",
    response_model=list[NotificationResponse],
)
def read_user_notifications(
    user_id: int,
    db: Session = Depends(get_db),
):
    return get_user_notifications(
        db=db,
        user_id=user_id,
    )


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
)
def read_notification(
    notification_id: int,
    db: Session = Depends(get_db),
):
    return mark_notification_as_read(
        db=db,
        notification_id=notification_id,
    )