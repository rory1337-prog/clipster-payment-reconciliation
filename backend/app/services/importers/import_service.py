from __future__ import annotations

import json
from decimal import Decimal
from pathlib import Path

from backend.app.db.unit_of_work import UnitOfWork
from backend.app.models.invoice import Invoice, InvoiceStatus
from backend.app.models.payment import (
    Payment,
    PaymentProvider,
    PaymentStatus,
)
from backend.app.schemas.providers.crypto import CryptoTransaction
from backend.app.schemas.providers.mercury import MercuryTransaction
from backend.app.schemas.providers.paypal import PaypalPayment
from backend.app.schemas.providers.quickbooks import QBInvoice
from backend.app.schemas.providers.stripe import StripePayment
from backend.app.services.importers.file_loader import FileLoader
from backend.app.services.importers.normalizer import Normalizer


class ImportService:
    def __init__(self, uow: UnitOfWork) -> None:
        self.uow = uow

    def import_all(self, data_dir: Path) -> None:
        self.import_quickbooks(data_dir / "quickbooks_invoices.json")
        self.import_stripe(data_dir / "stripe_payments.json")
        self.import_paypal(data_dir / "paypal_payments.json")
        self.import_mercury(data_dir / "mercury_transactions.json")
        self.import_crypto(data_dir / "crypto_transactions.json")

    def import_quickbooks(self, path: Path) -> None:
        data = FileLoader.load(path)

        invoices = []

        for item in data:
            schema = QBInvoice.model_validate(item)
            normalized = Normalizer.invoice(schema)

            if self.uow.invoices.get_by_external_id(normalized.external_id):
                continue

            invoices.append(
                Invoice(
                    external_id=normalized.external_id,
                    invoice_number=normalized.invoice_number,
                    customer_name=normalized.customer_name,
                    customer_email=normalized.customer_email,
                    amount=Decimal(normalized.amount),
                    currency=normalized.currency,
                    issue_date=normalized.issue_date,
                    due_date=normalized.due_date,
                    status=InvoiceStatus(normalized.status),
                    source=normalized.source,
                )
            )

        self.uow.invoices.add_many(invoices)

    def import_stripe(self, path: Path) -> None:
        data = FileLoader.load(path)

        payments = []

        for item in data:
            schema = StripePayment.model_validate(item)
            normalized = Normalizer.stripe(schema)

            if self.uow.payments.get_by_external_id(normalized.external_id):
                continue

            payments.append(
                Payment(
                    provider=PaymentProvider(normalized.provider),
                    external_id=normalized.external_id,
                    reference=normalized.reference,
                    payer_name=normalized.payer_name,
                    payer_email=normalized.payer_email,
                    amount=normalized.amount,
                    fee_amount=normalized.fee_amount,
                    currency=normalized.currency,
                    description=normalized.description,
                    paid_at=normalized.paid_at,
                    status=PaymentStatus.UNMATCHED,
                    raw_payload=json.dumps(item, ensure_ascii=False, default=str),
                )
            )

        self.uow.payments.add_many(payments)

    def import_paypal(self, path: Path) -> None:
        data = FileLoader.load(path)
        payments: list[Payment] = []

        for item in data:
            schema = PaypalPayment.model_validate(item)
            normalized = Normalizer.paypal(schema)

            if self.uow.payments.get_by_external_id(normalized.external_id):
                continue

            payments.append(
                Payment(
                    provider=PaymentProvider(normalized.provider),
                    external_id=normalized.external_id,
                    reference=normalized.reference,
                    payer_name=normalized.payer_name,
                    payer_email=normalized.payer_email,
                    amount=normalized.amount,
                    fee_amount=normalized.fee_amount,
                    currency=normalized.currency,
                    description=normalized.description,
                    paid_at=normalized.paid_at,
                    status=PaymentStatus.UNMATCHED,
                    raw_payload=json.dumps(item, ensure_ascii=False, default=str),
                )
            )

        self.uow.payments.add_many(payments)

    def import_mercury(self, path: Path) -> None:
        data = FileLoader.load(path)
        payments: list[Payment] = []

        for item in data:
            schema = MercuryTransaction.model_validate(item)
            normalized = Normalizer.mercury(schema)

            if self.uow.payments.get_by_external_id(normalized.external_id):
                continue

            payments.append(
                Payment(
                    provider=PaymentProvider(normalized.provider),
                    external_id=normalized.external_id,
                    reference=normalized.reference,
                    payer_name=normalized.payer_name,
                    payer_email=normalized.payer_email,
                    amount=normalized.amount,
                    fee_amount=normalized.fee_amount,
                    currency=normalized.currency,
                    description=normalized.description,
                    paid_at=normalized.paid_at,
                    status=PaymentStatus.UNMATCHED,
                    raw_payload=json.dumps(item, ensure_ascii=False, default=str),
                )
            )

        self.uow.payments.add_many(payments)

    def import_crypto(self, path: Path) -> None:
        data = FileLoader.load(path)
        payments: list[Payment] = []

        for item in data:
            schema = CryptoTransaction.model_validate(item)
            normalized = Normalizer.crypto(schema)

            if self.uow.payments.get_by_external_id(normalized.external_id):
                continue

            payments.append(
                Payment(
                    provider=PaymentProvider(normalized.provider),
                    external_id=normalized.external_id,
                    reference=normalized.reference,
                    payer_name=normalized.payer_name,
                    payer_email=normalized.payer_email,
                    amount=normalized.amount,
                    fee_amount=normalized.fee_amount,
                    currency=normalized.currency,
                    description=normalized.description,
                    paid_at=normalized.paid_at,
                    status=PaymentStatus.UNMATCHED,
                    raw_payload=json.dumps(item, ensure_ascii=False, default=str),
                )
            )

        self.uow.payments.add_many(payments)