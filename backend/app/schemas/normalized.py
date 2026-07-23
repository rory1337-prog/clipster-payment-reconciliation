from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel


class NormalizedInvoice(BaseModel):
    external_id: str
    invoice_number: str

    customer_name: str
    customer_email: str | None

    amount: Decimal
    currency: str

    issue_date: date
    due_date: date

    status: str
    source: str


class NormalizedPayment(BaseModel):
    external_id: str

    provider: str

    amount: Decimal
    fee_amount: Decimal

    currency: str

    payer_name: str | None
    payer_email: str | None

    reference: str | None
    description: str | None

    paid_at: datetime

    raw_payload: dict