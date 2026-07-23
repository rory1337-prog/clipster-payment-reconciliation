from datetime import datetime

from pydantic import BaseModel


class StripePayment(BaseModel):
    id: str

    amount: str
    fee: str

    currency: str

    customer_email: str | None
    customer_name: str | None

    description: str | None

    metadata: dict

    created_at: datetime

    status: str