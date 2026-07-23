from datetime import datetime

from pydantic import BaseModel, ConfigDict

from backend.app.models.reconciliation_match import MatchMethod, MatchStatus


class ReconciliationRunResponse(BaseModel):
    matched: int


class ReconciliationMatchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    payment_id: int
    invoice_id: int
    status: MatchStatus
    method: MatchMethod
    confidence_score: float
    explanation: str | None
    created_at: datetime


class FinanceOverviewResponse(BaseModel):
    total_invoices: int
    paid_invoices: int
    open_invoices: int

    total_payments: int
    matched_payments: int
    unmatched_payments: int
    needs_review_payments: int

    reconciliation_matches: int