from __future__ import annotations

from decimal import Decimal

from backend.app.schemas.normalized import (
    NormalizedInvoice,
    NormalizedPayment,
)
from backend.app.schemas.providers.crypto import CryptoTransaction
from backend.app.schemas.providers.mercury import MercuryTransaction
from backend.app.schemas.providers.paypal import PaypalPayment
from backend.app.schemas.providers.quickbooks import QBInvoice
from backend.app.schemas.providers.stripe import StripePayment


class Normalizer:
    @staticmethod
    def invoice(invoice: QBInvoice) -> NormalizedInvoice:
        return NormalizedInvoice(
            external_id=invoice.id,
            invoice_number=invoice.invoice_number,
            customer_name=invoice.customer.name,
            customer_email=invoice.customer.email,
            amount=Decimal(invoice.amount),
            currency=invoice.currency,
            issue_date=invoice.issue_date,
            due_date=invoice.due_date,
            status=invoice.status,
            source="quickbooks",
        )

    @staticmethod
    def stripe(payment: StripePayment) -> NormalizedPayment:
        return NormalizedPayment(
            external_id=payment.id,
            provider="stripe",
            amount=Decimal(payment.amount),
            fee_amount=Decimal(payment.fee),
            currency=payment.currency,
            payer_name=payment.customer_name,
            payer_email=payment.customer_email,
            reference=payment.metadata.get("invoice_number"),
            description=payment.description,
            paid_at=payment.created_at,
            raw_payload=payment.model_dump(),
        )

    @staticmethod
    def paypal(payment: PaypalPayment) -> NormalizedPayment:
        return NormalizedPayment(
            external_id=payment.transaction_id,
            provider="paypal",
            amount=Decimal(payment.gross_amount),
            fee_amount=Decimal(payment.fee_amount),
            currency=payment.currency_code,
            payer_name=payment.payer.name,
            payer_email=payment.payer.email,
            reference=None,
            description=payment.note,
            paid_at=payment.transaction_time,
            raw_payload=payment.model_dump(),
        )

    @staticmethod
    def mercury(payment: MercuryTransaction) -> NormalizedPayment:
        return NormalizedPayment(
            external_id=payment.id,
            provider="mercury",
            amount=Decimal(payment.amount),
            fee_amount=Decimal("0"),
            currency=payment.currency,
            payer_name=payment.counterparty_name,
            payer_email=payment.counterparty_email,
            reference=payment.reference,
            description=payment.bank_description,
            paid_at=payment.posted_at,
            raw_payload=payment.model_dump(),
        )

    @staticmethod
    def crypto(payment: CryptoTransaction) -> NormalizedPayment:
        return NormalizedPayment(
            external_id=payment.tx_hash,
            provider="crypto",
            amount=Decimal(payment.amount_usd),
            fee_amount=Decimal(payment.network_fee_usd),
            currency=payment.currency,
            payer_name=payment.sender_label,
            payer_email=None,
            reference=payment.memo,
            description=None,
            paid_at=payment.confirmed_at,
            raw_payload=payment.model_dump(),
        )