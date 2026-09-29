from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class MedicineVerification(Base):
    __tablename__ = "medicine_verifications"

    verification_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.user_id", ondelete="RESTRICT"),
        nullable=False,
    )

    batch_id: Mapped[int | None] = mapped_column(
        ForeignKey("medicine_batches.batch_id", ondelete="RESTRICT"),
        nullable=True,
    )

    verification_method: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
    )

    scanned_code: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    verification_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="PENDING",
        nullable=False,
    )