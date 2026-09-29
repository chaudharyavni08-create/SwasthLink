from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class VerificationResult(Base):
    __tablename__ = "verification_results"

    result_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    verification_id: Mapped[int] = mapped_column(
        ForeignKey("medicine_verifications.verification_id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    batch_exists: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    manufacturer_valid: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    expiry_valid: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    batch_valid: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    code_valid: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
    )

    result: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    reason: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )