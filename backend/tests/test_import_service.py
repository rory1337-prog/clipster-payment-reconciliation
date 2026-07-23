from pathlib import Path

from backend.app.db.session import SessionLocal
from backend.app.db.unit_of_work import UnitOfWork
from backend.app.services.importers.import_service import ImportService


def test_import_all_is_idempotent() -> None:
    data_dir = Path("backend/mock_data")

    with UnitOfWork(SessionLocal()) as uow:
        service = ImportService(uow)
        service.import_all(data_dir)

        first_invoice_count = len(uow.invoices.list_all())
        first_payment_count = len(uow.payments.list_all())

    with UnitOfWork(SessionLocal()) as uow:
        service = ImportService(uow)
        service.import_all(data_dir)

        second_invoice_count = len(uow.invoices.list_all())
        second_payment_count = len(uow.payments.list_all())

    assert first_invoice_count > 0
    assert first_payment_count > 0
    assert second_invoice_count == first_invoice_count
    assert second_payment_count == first_payment_count