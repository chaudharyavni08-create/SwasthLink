from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class TrustScore(Base):
    __tablename__ = "trust_scores"

    trust_score_id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    verification_id: Mapped[int] = mapped_column(
        ForeignKey("medicine_verifications.verification_id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
    )

    score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    score_category: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    calculated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )