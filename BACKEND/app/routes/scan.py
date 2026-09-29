from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.scan import (
    ManualVerificationRequest,
    QRVerificationRequest,
    VerificationHistoryResponse,
    VerificationResponse,
)
from app.services.scan_service import (
    get_verification_history,
    verify_manual,
    verify_qr_code,
)


router = APIRouter(
    prefix="/api/verification",
    tags=["Verification"],
)


@router.post(
    "/qr",
    response_model=VerificationResponse,
)
def verify_qr(
    request: QRVerificationRequest,
    db: Session = Depends(get_db),
):
    return verify_qr_code(
        db=db,
        user_id=request.user_id,
        verification_code=request.verification_code,
    )


@router.post(
    "/manual",
    response_model=VerificationResponse,
)
def verify_manual_medicine(
    request: ManualVerificationRequest,
    db: Session = Depends(get_db),
):
    return verify_manual(
        db=db,
        user_id=request.user_id,
        batch_number=request.batch_number,
        verification_code=request.verification_code,
    )


@router.get(
    "/history/{user_id}",
    response_model=list[VerificationHistoryResponse],
)
def read_verification_history(
    user_id: int,
    db: Session = Depends(get_db),
):
    return get_verification_history(
        db=db,
        user_id=user_id,
    )