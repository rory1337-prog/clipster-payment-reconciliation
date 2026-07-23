from __future__ import annotations

from datetime import datetime
from decimal import Decimal
from enum import StrEnum
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.db.session import Base

if TYPE_CHECKING:
    from backend.app.models.invoice import Invoice
    from backend.app.models.payment import Payment


class MatchStatus(StrEnum):
    MATCHED = "matched"
    NEEDS_REVIEW = "needs_review"
    REJECTED = "rejected"


class MatchMethod(StrEnum):
    EXACT_REFERENCE = "exact_reference"
    EMAIL_AND_AMOUNT = "email_and_amount"
    NAME_AND_AMOUNT = "name_and_amount"
    AI_ASSISTED = "ai_assisted"
    MANUAL = "manual"


class ReconciliationMatch(Base):
    __tablename__ = "reconciliation_matches"
    __table_args__ = (
        UniqueConstraint(
            "payment_id",
            "invoice_id",
            name="uq_reconciliation_payment_invoice",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    payment_id: Mapped[int] = mapped_column(
        ForeignKey("payments.id", ondelete="CASCADE"),
        index=True,
    )
    invoice_id: Mapped[int] = mapped_column(
        ForeignKey("invoices.id", ondelete="CASCADE"),
        index=True,
    )

    status: Mapped[MatchStatus] = mapped_column(
        Enum(
            MatchStatus,
            name="match_status",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
        ),
        default=MatchStatus.NEEDS_REVIEW,
        index=True,
    )

    method: Mapped[MatchMethod] = mapped_column(
        Enum(
            MatchMethod,
            name="match_method",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
        ),
    )

    confidence_score: Mapped[Decimal] = mapped_column(
        Numeric(5, 4),
    )

    explanation: Mapped[str | None] = mapped_column(Text, nullable=True)
    reviewed_by: Mapped[str | None] = mapped_column(String(255), nullable=True)

    reviewed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    payment: Mapped[Payment] = relationship()
    invoice: Mapped[Invoice] = relationship()
