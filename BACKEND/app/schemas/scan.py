from datetime import datetime

from pydantic import BaseModel, model_validator


class QRVerificationRequest(BaseModel):
    user_id: int
    verification_code: str


class ManualVerificationRequest(BaseModel):
    user_id: int
    batch_number: str | None = None
    verification_code: str | None = None

    @model_validator(mode="after")
    def validate_input(self):
        if not self.batch_number and not self.verification_code:
            raise ValueError(
                "Provide batch_number or verification_code"
            )

        return self


class VerificationResponse(BaseModel):
    verification_id: int
    medicine_id: int | None
    medicine_name: str | None
    manufacturer_name: str | None
    batch_number: str | None
    verification_code: str | None
    manufacturing_date: str | None
    expiry_date: str | None
    batch_status: str | None

    batch_exists: bool
    manufacturer_valid: bool
    expiry_valid: bool
    batch_valid: bool
    code_valid: bool

    result: str
    confidence_score: int
    confidence_category: str
    reason: str


class VerificationHistoryResponse(BaseModel):
    verification_id: int
    verification_method: str
    verification_time: datetime
    verification_status: str

    medicine_id: int | None
    medicine_name: str | None
    batch_number: str | None

    result: str | None
    confidence_score: int | None
    confidence_category: str | None
    reason: str | None