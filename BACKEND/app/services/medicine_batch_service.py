from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.medicine import Medicine
from app.models.medicine_batch import MedicineBatch


def get_batches_by_medicine_id(
    db: Session,
    medicine_id: int,
) -> list[MedicineBatch]:

    medicine_result = db.execute(
        select(Medicine).where(
            Medicine.medicine_id == medicine_id
        )
    )

    medicine = medicine_result.scalar_one_or_none()

    if medicine is None:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found",
        )

    result = db.execute(
        select(MedicineBatch)
        .where(
            MedicineBatch.medicine_id == medicine_id
        )
        .order_by(MedicineBatch.batch_id)
    )

    return list(result.scalars().all())