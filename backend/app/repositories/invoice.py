from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.models.invoice import Invoice


class InvoiceRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, invoice: Invoice) -> Invoice:
        self.session.add(invoice)
        self.session.flush()
        return invoice

    def add_many(self, invoices: Sequence[Invoice]) -> list[Invoice]:
        self.session.add_all(invoices)
        self.session.flush()
        return list(invoices)

    def get_by_external_id(self, external_id: str) -> Invoice | None:
        statement = select(Invoice).where(Invoice.external_id == external_id)
        return self.session.scalar(statement)

    def get_by_invoice_number(self, invoice_number: str) -> Invoice | None:
        statement = select(Invoice).where(
            Invoice.invoice_number == invoice_number,
        )
        return self.session.scalar(statement)

    def list_all(self) -> list[Invoice]:
        statement = select(Invoice).order_by(Invoice.issue_date.desc())
        return list(self.session.scalars(statement).all())
