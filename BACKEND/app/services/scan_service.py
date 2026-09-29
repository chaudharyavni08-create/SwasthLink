from datetime import date

from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.medicine import Medicine
from app.models.medicine_batch import MedicineBatch
from app.models.medicine_verification import MedicineVerification
from app.models.manufacturer import Manufacturer
from app.models.trust_score import TrustScore
from app.models.user import User
from app.models.verification_result import VerificationResult


def calculate_confidence(
    batch_exists: bool,
    manufacturer_valid: bool,
    expiry_valid: bool,
    batch_valid: bool,
    code_valid: bool,
) -> int:
    score = 0

    if batch_exists:
        score += 40

    if manufacturer_valid:
        score += 15

    if expiry_valid:
        score += 20

    if batch_valid:
        score += 20

    if code_valid:
        score += 5

    return score


def get_confidence_category(score: int) -> str:
    if score >= 90:
        return "VERY_HIGH"
    if score >= 75:
        return "HIGH"
    if score >= 50:
        return "MEDIUM"
    if score >= 25:
        return "LOW"

    return "VERY_LOW"


def _create_verification(
    db: Session,
    user_id: int,
    verification_method: str,
    batch: MedicineBatch | None,
    entered_code: str | None,
) -> dict:

    verification = MedicineVerification(
        user_id=user_id,
        batch_id=batch.batch_id if batch else None,
        verification_method=verification_method,
        scanned_code=entered_code,
        status="PENDING",
    )

    db.add(verification)
    db.flush()

    if batch is None:
        result = VerificationResult(
            verification_id=verification.verification_id,
            batch_exists=False,
            manufacturer_valid=False,
            expiry_valid=False,
            batch_valid=False,
            code_valid=False,
            result="FAKE",
            reason="No registered medicine batch matched the provided information.",
        )

        trust_score = TrustScore(
            verification_id=verification.verification_id,
            score=0,
            score_category="VERY_LOW",
        )

        verification.status = "FAILED"

        db.add(result)
        db.add(trust_score)
        db.commit()

        return {
            "verification_id": verification.verification_id,
            "medicine_id": None,
            "medicine_name": None,
            "manufacturer_name": None,
            "batch_number": None,
            "verification_code": entered_code,
            "manufacturing_date": None,
            "expiry_date": None,
            "batch_status": None,
            "batch_exists": False,
            "manufacturer_valid": False,
            "expiry_valid": False,
            "batch_valid": False,
            "code_valid": False,
            "result": "FAKE",
            "confidence_score": 0,
            "confidence_category": "VERY_LOW",
            "reason": "No registered medicine batch matched the provided information.",
        }

    medicine_result = db.execute(
        select(Medicine).where(
            Medicine.medicine_id == batch.medicine_id
        )
    )

    medicine = medicine_result.scalar_one_or_none()

    manufacturer = None

    if medicine:
        manufacturer_result = db.execute(
            select(Manufacturer).where(
                Manufacturer.manufacturer_id
                == medicine.manufacturer_id
            )
        )

        manufacturer = manufacturer_result.scalar_one_or_none()

    batch_exists = True

    if entered_code is not None:
        code_valid = batch.verification_code == entered_code
    else:
        code_valid = False

    manufacturer_valid = bool(
        manufacturer and manufacturer.is_verified
    )

    expiry_valid = date.today() <= batch.expiry_date

    batch_valid = batch.status == "ACTIVE"

    score = calculate_confidence(
        batch_exists=batch_exists,
        manufacturer_valid=manufacturer_valid,
        expiry_valid=expiry_valid,
        batch_valid=batch_valid,
        code_valid=code_valid,
    )

    if not expiry_valid:
        final_result = "EXPIRED"
        reason = "The medicine batch has passed its expiry date."

    elif batch.status in {"RECALLED", "SUSPENDED"}:
        final_result = "SUSPICIOUS"
        reason = f"The batch status is {batch.status}."

    elif not manufacturer_valid:
        final_result = "SUSPICIOUS"
        reason = "The manufacturer could not be validated."

    elif not medicine or not medicine.is_active:
        final_result = "SUSPICIOUS"
        reason = "The medicine record is inactive."

    elif score >= 75:
        final_result = "GENUINE"
        reason = "All available verification checks passed."

    else:
        final_result = "SUSPICIOUS"
        reason = "Some verification checks require further review."

    confidence_category = get_confidence_category(score)

    verification.status = "COMPLETED"

    verification_result = VerificationResult(
        verification_id=verification.verification_id,
        batch_exists=batch_exists,
        manufacturer_valid=manufacturer_valid,
        expiry_valid=expiry_valid,
        batch_valid=batch_valid,
        code_valid=code_valid,
        result=final_result,
        reason=reason,
    )

    trust_score = TrustScore(
        verification_id=verification.verification_id,
        score=score,
        score_category=confidence_category,
    )

    db.add(verification_result)
    db.add(trust_score)

    db.commit()
    db.refresh(verification)

    return {
        "verification_id": verification.verification_id,
        "medicine_id": medicine.medicine_id if medicine else None,
        "medicine_name": medicine.medicine_name if medicine else None,
        "manufacturer_name": (
            manufacturer.manufacturer_name
            if manufacturer
            else None
        ),
        "batch_number": batch.batch_number,
        "verification_code": batch.verification_code,
        "manufacturing_date": str(batch.manufacturing_date),
        "expiry_date": str(batch.expiry_date),
        "batch_status": batch.status,
        "batch_exists": batch_exists,
        "manufacturer_valid": manufacturer_valid,
        "expiry_valid": expiry_valid,
        "batch_valid": batch_valid,
        "code_valid": code_valid,
        "result": final_result,
        "confidence_score": score,
        "confidence_category": confidence_category,
        "reason": reason,
    }


def verify_qr_code(
    db: Session,
    user_id: int,
    verification_code: str,
) -> dict:

    user_result = db.execute(
        select(User).where(User.user_id == user_id)
    )

    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    batch_result = db.execute(
        select(MedicineBatch).where(
            MedicineBatch.verification_code == verification_code
        )
    )

    batch = batch_result.scalar_one_or_none()

    return _create_verification(
        db=db,
        user_id=user_id,
        verification_method="QR",
        batch=batch,
        entered_code=verification_code,
    )


def verify_manual(
    db: Session,
    user_id: int,
    batch_number: str | None,
    verification_code: str | None,
) -> dict:

    user_result = db.execute(
        select(User).where(User.user_id == user_id)
    )

    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    batch = None

    if batch_number:
        batch_result = db.execute(
            select(MedicineBatch).where(
                MedicineBatch.batch_number == batch_number
            )
        )

        batch = batch_result.scalar_one_or_none()

    elif verification_code:
        batch_result = db.execute(
            select(MedicineBatch).where(
                MedicineBatch.verification_code
                == verification_code
            )
        )

        batch = batch_result.scalar_one_or_none()

    return _create_verification(
        db=db,
        user_id=user_id,
        verification_method="MANUAL",
        batch=batch,
        entered_code=verification_code,
    )


def get_verification_history(
    db: Session,
    user_id: int,
) -> list[dict]:

    user_result = db.execute(
        select(User).where(User.user_id == user_id)
    )

    user = user_result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found",
        )

    statement = (
        select(
            MedicineVerification,
            MedicineBatch,
            Medicine,
            VerificationResult,
            TrustScore,
        )
        .outerjoin(
            MedicineBatch,
            MedicineVerification.batch_id
            == MedicineBatch.batch_id,
        )
        .outerjoin(
            Medicine,
            MedicineBatch.medicine_id
            == Medicine.medicine_id,
        )
        .outerjoin(
            VerificationResult,
            VerificationResult.verification_id
            == MedicineVerification.verification_id,
        )
        .outerjoin(
            TrustScore,
            TrustScore.verification_id
            == MedicineVerification.verification_id,
        )
        .where(
            MedicineVerification.user_id == user_id
        )
        .order_by(
            MedicineVerification.verification_time.desc()
        )
    )

    rows = db.execute(statement).all()

    history = []

    for (
        verification,
        batch,
        medicine,
        verification_result,
        trust_score,
    ) in rows:

        history.append(
            {
                "verification_id": verification.verification_id,
                "verification_method": verification.verification_method,
                "verification_time": verification.verification_time,
                "verification_status": verification.status,

                "medicine_id": (
                    medicine.medicine_id
                    if medicine
                    else None
                ),

                "medicine_name": (
                    medicine.medicine_name
                    if medicine
                    else None
                ),

                "batch_number": (
                    batch.batch_number
                    if batch
                    else None
                ),

                "result": (
                    verification_result.result
                    if verification_result
                    else None
                ),

                "confidence_score": (
                    trust_score.score
                    if trust_score
                    else None
                ),

                "confidence_category": (
                    trust_score.score_category
                    if trust_score
                    else None
                ),

                "reason": (
                    verification_result.reason
                    if verification_result
                    else None
                ),
            }
        )

    return history