from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.payment import Payment, PaymentStatus


class PaymentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, payment: Payment) -> Payment:
        self.session.add(payment)
        self.session.flush()
        return payment

    def add_many(self, payments: Sequence[Payment]) -> list[Payment]:
        self.session.add_all(payments)
        self.session.flush()
        return list(payments)

    def get_by_external_id(self, external_id: str) -> Payment | None:
        statement = select(Payment).where(Payment.external_id == external_id)
        return self.session.scalar(statement)

    def list_all(self) -> list[Payment]:
        statement = select(Payment).order_by(Payment.paid_at.desc())
        return list(self.session.scalars(statement).all())

    def list_unmatched(self) -> list[Payment]:
        statement = (
            select(Payment)
            .where(
                Payment.status.in_(
                    [
                        PaymentStatus.UNMATCHED,
                        PaymentStatus.NEEDS_REVIEW,
                    ],
                ),
            )
            .order_by(Payment.paid_at.asc())
        )
        return list(self.session.scalars(statement).all())
