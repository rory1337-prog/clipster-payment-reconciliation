from datetime import UTC, datetime
from decimal import Decimal

from backend.app.models.invoice import Invoice, InvoiceStatus
from backend.app.models.payment import Payment, PaymentProvider, PaymentStatus
from backend.app.services.reconciliation.matcher import PaymentMatcher


def make_invoice(
    *,
    invoice_number: str = "INV-001",
    customer_name: str = "Acme Ltd",
    customer_email: str | None = "billing@acme.com",
    amount: str = "100.00",
    currency: str = "USD",
) -> Invoice:
    return Invoice(
        external_id=f"qb-{invoice_number}",
        invoice_number=invoice_number,
        customer_name=customer_name,
        customer_email=customer_email,
        amount=Decimal(amount),
        currency=currency,
        issue_date=datetime(2026, 7, 1, tzinfo=UTC).date(),
        due_date=datetime(2026, 7, 31, tzinfo=UTC).date(),
        status=InvoiceStatus.OPEN,
        source="quickbooks",
    )


def make_payment(
    *,
    reference: str | None = None,
    payer_name: str | None = "Acme Ltd",
    payer_email: str | None = "billing@acme.com",
    amount: str = "100.00",
    currency: str = "USD",
) -> Payment:
    return Payment(
        provider=PaymentProvider.STRIPE,
        external_id="pay-001",
        reference=reference,
        payer_name=payer_name,
        payer_email=payer_email,
        amount=Decimal(amount),
        fee_amount=Decimal("0.00"),
        currency=currency,
        description=None,
        paid_at=datetime(2026, 7, 10, tzinfo=UTC),
        status=PaymentStatus.UNMATCHED,
        raw_payload=None,
    )


def test_match_by_exact_reference() -> None:
    matcher = PaymentMatcher()
    invoice = make_invoice(invoice_number="INV-1001")
    payment = make_payment(reference="INV-1001")

    result = matcher.match(payment, [invoice])

    assert result.invoice is invoice
    assert result.rule == "exact_reference"
    assert result.confidence == Decimal("1.00")


def test_reference_match_is_case_insensitive() -> None:
    matcher = PaymentMatcher()
    invoice = make_invoice(invoice_number="INV-1001")
    payment = make_payment(reference="  inv-1001  ")

    result = matcher.match(payment, [invoice])

    assert result.invoice is invoice
    assert result.rule == "exact_reference"


def test_match_by_email_amount_currency() -> None:
    matcher = PaymentMatcher()
    invoice = make_invoice()
    payment = make_payment(reference=None)

    result = matcher.match(payment, [invoice])

    assert result.invoice is invoice
    assert result.rule == "email_amount_currency"
    assert result.confidence == Decimal("0.98")


def test_match_by_normalized_name_amount_currency() -> None:
    matcher = PaymentMatcher()
    invoice = make_invoice(
        customer_name="Acme   Ltd",
        customer_email=None,
    )
    payment = make_payment(
        reference=None,
        payer_name="  ACME ltd  ",
        payer_email=None,
    )

    result = matcher.match(payment, [invoice])

    assert result.invoice is invoice
    assert result.rule == "name_amount_currency"
    assert result.confidence == Decimal("0.90")


def test_does_not_match_when_amount_is_different() -> None:
    matcher = PaymentMatcher()
    invoice = make_invoice(amount="100.00")
    payment = make_payment(reference=None, amount="99.00")

    result = matcher.match(payment, [invoice])

    assert result.invoice is None
    assert result.rule is None
    assert result.confidence == Decimal("0.00")


def test_does_not_match_when_currency_is_different() -> None:
    matcher = PaymentMatcher()
    invoice = make_invoice(currency="USD")
    payment = make_payment(reference=None, currency="EUR")

    result = matcher.match(payment, [invoice])

    assert result.invoice is None
    assert result.rule is None
    assert result.confidence == Decimal("0.00")


def test_returns_no_match_when_there_are_no_candidates() -> None:
    matcher = PaymentMatcher()
    invoice = make_invoice(
        customer_name="Other Company",
        customer_email="other@example.com",
    )
    payment = make_payment(reference=None)

    result = matcher.match(payment, [invoice])

    assert result.invoice is None
    assert result.rule is None
    assert result.confidence == Decimal("0.00")


def test_does_not_match_when_email_candidates_are_ambiguous() -> None:
    matcher = PaymentMatcher()
    invoices = [
        make_invoice(invoice_number="INV-001"),
        make_invoice(invoice_number="INV-002"),
    ]
    payment = make_payment(reference=None)

    result = matcher.match(payment, invoices)

    assert result.invoice is None
    assert result.rule is None


def test_does_not_match_when_name_candidates_are_ambiguous() -> None:
    matcher = PaymentMatcher()
    invoices = [
        make_invoice(
            invoice_number="INV-001",
            customer_email=None,
        ),
        make_invoice(
            invoice_number="INV-002",
            customer_email=None,
        ),
    ]
    payment = make_payment(
        reference=None,
        payer_email=None,
    )

    result = matcher.match(payment, invoices)

    assert result.invoice is None
    assert result.rule is None