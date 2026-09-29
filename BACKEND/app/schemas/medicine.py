from pydantic import BaseModel, ConfigDict


class MedicineResponse(BaseModel):
    medicine_id: int
    manufacturer_id: int
    medicine_name: str
    generic_name: str
    dosage_form: str
    strength: str
    description: str | None = None
    is_active: bool

    model_config = ConfigDict(from_attributes=True)