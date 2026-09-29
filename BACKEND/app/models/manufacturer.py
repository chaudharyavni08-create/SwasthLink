from datetime import datetime

from sqlalchemy import Boolean, DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Manufacturer(Base):
    __tablename__ = "manufacturers"

    manufacturer_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    manufacturer_name: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    license_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    address: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    contact_email: Mapped[str | None] = mapped_column(
        String(150),
        unique=True,
        nullable=True,
    )

    phone: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )