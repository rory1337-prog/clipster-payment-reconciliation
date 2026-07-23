from datetime import datetime

from pydantic import BaseModel


class PaypalPayer(BaseModel):
    name: str
    email: str


class PaypalPayment(BaseModel):
    transaction_id: str

    gross_amount: str
    fee_amount: str

    currency_code: str

    payer: PaypalPayer

    note: str | None

    transaction_time: datetime

    state: str