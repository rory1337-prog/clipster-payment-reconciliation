from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from backend.app.models.reconciliation_match import (
    MatchStatus,
    ReconciliationMatch,
)


class ReconciliationRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, match: ReconciliationMatch) -> ReconciliationMatch:
        self.session.add(match)
        self.session.flush()
        return match

    def get_by_payment_and_invoice(
        self,
        payment_id: int,
        invoice_id: int,
    ) -> ReconciliationMatch | None:
        statement = select(ReconciliationMatch).where(
            ReconciliationMatch.payment_id == payment_id,
            ReconciliationMatch.invoice_id == invoice_id,
        )
        return self.session.scalar(statement)

    def list_all(self) -> list[ReconciliationMatch]:
        statement = (
            select(ReconciliationMatch)
            .options(
                selectinload(ReconciliationMatch.payment),
                selectinload(ReconciliationMatch.invoice),
            )
            .order_by(ReconciliationMatch.created_at.desc())
        )
        return list(self.session.scalars(statement).all())

    def list_needs_review(self) -> list[ReconciliationMatch]:
        statement = (
            select(ReconciliationMatch)
            .where(ReconciliationMatch.status == MatchStatus.NEEDS_REVIEW)
            .options(
                selectinload(ReconciliationMatch.payment),
                selectinload(ReconciliationMatch.invoice),
            )
            .order_by(ReconciliationMatch.created_at.desc())
        )
        return list(self.session.scalars(statement).all())
