from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from backend.app.models.invoice import Invoice
from backend.app.models.payment import Payment


@dataclass(frozen=True)
class MatchResult:
    invoice: Invoice | None
    rule: str | None
    confidence: Decimal


class PaymentMatcher:
    def match(
        self,
        payment: Payment,
        invoices: list[Invoice],
    ) -> MatchResult:
        reference_match = self._match_by_reference(payment, invoices)
        if reference_match is not None:
            return MatchResult(
                invoice=reference_match,
                rule="exact_reference",
                confidence=Decimal("1.00"),
            )

        email_match = self._match_by_email_amount_currency(payment, invoices)
        if email_match is not None:
            return MatchResult(
                invoice=email_match,
                rule="email_amount_currency",
                confidence=Decimal("0.98"),
            )

        name_match = self._match_by_name_amount_currency(payment, invoices)
        if name_match is not None:
            return MatchResult(
                invoice=name_match,
                rule="name_amount_currency",
                confidence=Decimal("0.90"),
            )

        return MatchResult(
            invoice=None,
            rule=None,
            confidence=Decimal("0.00"),
        )

    def _match_by_reference(
        self,
        payment: Payment,
        invoices: list[Invoice],
    ) -> Invoice | None:
        if not payment.reference:
            return None

        payment_reference = payment.reference.strip().casefold()

        for invoice in invoices:
            if invoice.invoice_number.strip().casefold() == payment_reference:
                return invoice

        return None

    def _match_by_email_amount_currency(
        self,
        payment: Payment,
        invoices: list[Invoice],
    ) -> Invoice | None:
        if not payment.payer_email:
            return None

        payment_email = payment.payer_email.strip().casefold()

        candidates = [
            invoice
            for invoice in invoices
            if invoice.customer_email
            and invoice.customer_email.strip().casefold() == payment_email
            and self._same_amount_and_currency(payment, invoice)
        ]

        if len(candidates) == 1:
            return candidates[0]

        return None

    def _match_by_name_amount_currency(
        self,
        payment: Payment,
        invoices: list[Invoice],
    ) -> Invoice | None:
        if not payment.payer_name:
            return None

        payment_name = self._normalize_name(payment.payer_name)

        candidates = [
            invoice
            for invoice in invoices
            if self._normalize_name(invoice.customer_name) == payment_name
            and self._same_amount_and_currency(payment, invoice)
        ]

        if len(candidates) == 1:
            return candidates[0]

        return None

    @staticmethod
    def _same_amount_and_currency(
        payment: Payment,
        invoice: Invoice,
    ) -> bool:
        return (
            payment.amount == invoice.amount
            and payment.currency.casefold() == invoice.currency.casefold()
        )

    @staticmethod
    def _normalize_name(value: str) -> str:
        return " ".join(value.strip().casefold().split())