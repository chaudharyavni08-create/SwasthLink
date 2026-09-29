from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertCreate(BaseModel):
    medicine_id: int | None = None
    batch_id: int | None = None
    report_id: int | None = None

    title: str
    message: str

    severity: str
    priority: str

    latitude: float | None = None
    longitude: float | None = None

    report_count: int = 1


class AlertUpdate(BaseModel):
    status: str


class AlertResponse(BaseModel):
    alert_id: int

    medicine_id: int | None
    batch_id: int | None
    report_id: int | None

    title: str
    message: str

    severity: str
    priority: str

    latitude: float | None
    longitude: float | None

    report_count: int
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)