from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Report(Base):
    __tablename__ = "reports"

    report_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="RESTRICT"),
        nullable=False,
    )

    medicine_id: Mapped[int | None] = mapped_column(
        ForeignKey("medicines.medicine_id", ondelete="SET NULL"),
        nullable=True,
    )

    batch_id: Mapped[int | None] = mapped_column(
        ForeignKey("medicine_batches.batch_id", ondelete="SET NULL"),
        nullable=True,
    )

    verification_id: Mapped[int | None] = mapped_column(
        ForeignKey("medicine_verifications.verification_id", ondelete="SET NULL"),
        nullable=True,
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="OPEN",
        nullable=False,
    )

    evidence_image_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    latitude: Mapped[Decimal | None] = mapped_column(
        Numeric(9, 6),
        nullable=True,
    )

    longitude: Mapped[Decimal | None] = mapped_column(
        Numeric(9, 6),
        nullable=True,
    )

    severity: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )