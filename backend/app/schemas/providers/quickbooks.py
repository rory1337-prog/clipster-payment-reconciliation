from datetime import date

from pydantic import BaseModel


class QBCustomer(BaseModel):
    name: str
    email: str


class QBInvoice(BaseModel):
    id: str
    invoice_number: str

    customer: QBCustomer

    amount: str
    currency: str

    issue_date: date
    due_date: date

    status: str