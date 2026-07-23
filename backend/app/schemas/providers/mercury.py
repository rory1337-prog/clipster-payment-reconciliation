from datetime import datetime

from pydantic import BaseModel


class MercuryTransaction(BaseModel):
    id: str

    amount: str
    currency: str

    counterparty_name: str | None
    counterparty_email: str | None

    bank_description: str | None
    reference: str | None

    posted_at: datetime

    status: str