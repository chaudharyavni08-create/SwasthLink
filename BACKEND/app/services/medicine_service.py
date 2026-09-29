from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.medicine import Medicine


def get_all_medicines(db: Session) -> list[Medicine]:
    result = db.execute(
        select(Medicine).order_by(Medicine.medicine_id)
    )

    return list(result.scalars().all())


def get_medicine_by_id(
    db: Session,
    medicine_id: int,
) -> Medicine:
    result = db.execute(
        select(Medicine).where(
            Medicine.medicine_id == medicine_id
        )
    )

    medicine = result.scalar_one_or_none()

    if medicine is None:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found",
        )

    return medicine