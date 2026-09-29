from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Medicine(Base):
    __tablename__ = "medicines"

    medicine_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    manufacturer_id: Mapped[int] = mapped_column(
        ForeignKey("manufacturers.manufacturer_id", ondelete="RESTRICT"),
        nullable=False,
    )

    medicine_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    generic_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    dosage_form: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    strength: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )