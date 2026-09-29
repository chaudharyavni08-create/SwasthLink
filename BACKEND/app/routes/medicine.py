from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.medicine import MedicineResponse
from app.schemas.medicine_batch import MedicineBatchResponse
from app.services.medicine_service import (
    get_all_medicines,
    get_medicine_by_id,
)
from app.services.medicine_batch_service import (
    get_batches_by_medicine_id,
)


router = APIRouter(
    prefix="/api/medicines",
    tags=["Medicines"],
)


@router.get(
    "",
    response_model=list[MedicineResponse],
)
def read_medicines(
    db: Session = Depends(get_db),
):
    return get_all_medicines(db)


@router.get(
    "/{medicine_id}",
    response_model=MedicineResponse,
)
def read_medicine(
    medicine_id: int,
    db: Session = Depends(get_db),
):
    return get_medicine_by_id(
        db,
        medicine_id,
    )


@router.get(
    "/{medicine_id}/batches",
    response_model=list[MedicineBatchResponse],
)
def read_medicine_batches(
    medicine_id: int,
    db: Session = Depends(get_db),
):
    return get_batches_by_medicine_id(
        db,
        medicine_id,
    )