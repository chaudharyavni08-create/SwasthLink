from datetime import date

from pydantic import BaseModel, ConfigDict


class MedicineBatchResponse(BaseModel):
    batch_id: int
    medicine_id: int
    batch_number: str
    manufacturing_date: date
    expiry_date: date
    mrp: float
    quantity: int
    verification_code: str
    status: str

    model_config = ConfigDict(from_attributes=True)