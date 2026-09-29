from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ReportStatus = Literal[
    "OPEN",
    "UNDER_REVIEW",
    "RESOLVED",
    "REJECTED",
]

Severity = Literal[
    "LOW",
    "MEDIUM",
    "HIGH",
]


class ReportCreate(BaseModel):
    user_id: int
    medicine_id: int | None = None
    batch_id: int | None = None
    verification_id: int | None = None

    reason: str = Field(
        min_length=5,
        max_length=1000,
    )

    evidence_image_url: str | None = None

    latitude: float | None = Field(
        default=None,
        ge=-90,
        le=90,
    )

    longitude: float | None = Field(
        default=None,
        ge=-180,
        le=180,
    )

    severity: Severity = "MEDIUM"


class ReportStatusUpdate(BaseModel):
    status: ReportStatus


class ReportResponse(BaseModel):
    report_id: int
    user_id: int

    medicine_id: int | None = None
    batch_id: int | None = None
    verification_id: int | None = None

    reason: str
    status: ReportStatus

    evidence_image_url: str | None = None

    latitude: float | None = None
    longitude: float | None = None

    severity: Severity | None = None

    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )