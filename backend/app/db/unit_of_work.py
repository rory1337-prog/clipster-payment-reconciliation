from __future__ import annotations

from types import TracebackType

from sqlalchemy.orm import Session

from backend.app.repositories.invoice import InvoiceRepository
from backend.app.repositories.payment import PaymentRepository
from backend.app.repositories.reconciliation import ReconciliationRepository


class UnitOfWork:
    def __init__(self, session: Session) -> None:
        self.session = session

        self.invoices = InvoiceRepository(session)
        self.payments = PaymentRepository(session)
        self.reconciliations = ReconciliationRepository(session)

    def __enter__(self) -> UnitOfWork:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            self.rollback()
        else:
            self.commit()

        self.session.close()

    def commit(self) -> None:
        self.session.commit()

    def rollback(self) -> None:
        self.session.rollback()
