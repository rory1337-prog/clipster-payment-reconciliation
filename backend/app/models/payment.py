from datetime import datetime
from decimal import Decimal
from enum import StrEnum

from sqlalchemy import DateTime, Enum, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from backend.app.db.session import Base


class PaymentProvider(StrEnum):
    STRIPE = "stripe"
    PAYPAL = "paypal"
    MERCURY = "mercury"
    CRYPTO = "crypto"


class PaymentStatus(StrEnum):
    PENDING = "pending"
    MATCHED = "matched"
    NEEDS_REVIEW = "needs_review"
    UNMATCHED = "unmatched"


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)

    provider: Mapped[PaymentProvider] = mapped_column(
        Enum(
            PaymentProvider,
            name="payment_provider",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
        ),
        index=True,
    )

    external_id: Mapped[str] = mapped_column(String(150), unique=True, index=True)
    reference: Mapped[str | None] = mapped_column(String(150), nullable=True, index=True)

    payer_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    payer_email: Mapped[str | None] = mapped_column(String(255), nullable=True)

    amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))
    fee_amount: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        default=Decimal("0.00"),
    )
    currency: Mapped[str] = mapped_column(String(3))

    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    paid_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    status: Mapped[PaymentStatus] = mapped_column(
        Enum(
            PaymentStatus,
            name="payment_status",
            values_callable=lambda enum_cls: [item.value for item in enum_cls],
        ),
        default=PaymentStatus.UNMATCHED,
        index=True,
    )

    raw_payload: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
