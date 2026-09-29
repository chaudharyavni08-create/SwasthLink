from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class MedicineBatch(Base):
    __tablename__ = "medicine_batches"

    batch_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    medicine_id: Mapped[int] = mapped_column(
        ForeignKey("medicines.medicine_id", ondelete="RESTRICT"),
        nullable=False,
    )

    batch_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    manufacturing_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    expiry_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    mrp: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    verification_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
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