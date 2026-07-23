from datetime import datetime

from pydantic import BaseModel


class CryptoTransaction(BaseModel):
    tx_hash: str

    amount_usd: str
    network_fee_usd: str

    currency: str

    sender_label: str | None

    memo: str | None

    confirmed_at: datetime

    confirmations: int