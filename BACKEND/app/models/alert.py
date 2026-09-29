from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    alert_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    medicine_id: Mapped[int | None] = mapped_column(
        ForeignKey("medicines.medicine_id", ondelete="SET NULL"),
        nullable=True,
    )

    batch_id: Mapped[int | None] = mapped_column(
        ForeignKey("medicine_batches.batch_id", ondelete="SET NULL"),
        nullable=True,
    )

    report_id: Mapped[int | None] = mapped_column(
        ForeignKey("reports.report_id", ondelete="SET NULL"),
        nullable=True,
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    severity: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    latitude: Mapped[Decimal | None] = mapped_column(
        Numeric(9, 6),
        nullable=True,
    )

    longitude: Mapped[Decimal | None] = mapped_column(
        Numeric(9, 6),
        nullable=True,
    )

    report_count: Mapped[int] = mapped_column(
        Integer,
        default=1,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="ACTIVE",
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )