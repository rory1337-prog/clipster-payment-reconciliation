from __future__ import annotations

from backend.app.db.unit_of_work import UnitOfWork
from backend.app.models.invoice import InvoiceStatus
from backend.app.models.payment import PaymentStatus
from backend.app.models.reconciliation_match import (
    MatchMethod,
    MatchStatus,
    ReconciliationMatch,
)
from backend.app.services.reconciliation.matcher import PaymentMatcher


class ReconciliationService:
    def __init__(
        self,
        unit_of_work: UnitOfWork,
        matcher: PaymentMatcher | None = None,
    ) -> None:
        self.unit_of_work = unit_of_work
        self.matcher = matcher or PaymentMatcher()

    def reconcile(self) -> int:
        matched_count = 0

        with self.unit_of_work as uow:
            payments = uow.payments.list_unmatched()
            available_invoices = uow.invoices.list_open()

            for payment in payments:
                result = self.matcher.match(
                    payment=payment,
                    invoices=available_invoices,
                )

                if result.invoice is None or result.rule is None:
                    payment.status = PaymentStatus.UNMATCHED
                    continue

                invoice = result.invoice

                existing_match = uow.reconciliations.get_by_payment_and_invoice(
                    payment_id=payment.id,
                    invoice_id=invoice.id,
                )

                if existing_match is not None:
                    continue

                reconciliation_match = ReconciliationMatch(
                    payment_id=payment.id,
                    invoice_id=invoice.id,
                    status=MatchStatus.MATCHED,
                    method=self._resolve_match_method(result.rule),
                    confidence_score=result.confidence,
                    explanation=self._build_explanation(result.rule),
                )

                uow.reconciliations.add(reconciliation_match)

                payment.status = PaymentStatus.MATCHED
                invoice.status = InvoiceStatus.PAID

                available_invoices.remove(invoice)
                matched_count += 1

        return matched_count

    @staticmethod
    def _resolve_match_method(rule: str) -> MatchMethod:
        mapping = {
            "exact_reference": MatchMethod.EXACT_REFERENCE,
            "email_amount_currency": MatchMethod.EMAIL_AND_AMOUNT,
            "name_amount_currency": MatchMethod.NAME_AND_AMOUNT,
        }

        try:
            return mapping[rule]
        except KeyError as error:
            raise ValueError(f"Unsupported matching rule: {rule}") from error

    @staticmethod
    def _build_explanation(rule: str) -> str:
        explanations = {
            "exact_reference": (
                "Payment reference exactly matches the invoice number."
            ),
            "email_amount_currency": (
                "Payer email, payment amount, and currency match the invoice."
            ),
            "name_amount_currency": (
                "Normalized payer name, payment amount, and currency match the invoice."
            ),
        }

        return explanations[rule]