from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from backend.app.db.session import get_db_session
from backend.app.db.unit_of_work import UnitOfWork
from backend.app.models.invoice import Invoice, InvoiceStatus
from backend.app.models.payment import Payment, PaymentStatus
from backend.app.models.reconciliation_match import ReconciliationMatch
from backend.app.repositories.reconciliation import ReconciliationRepository
from backend.app.schemas.reconciliation import (
    FinanceOverviewResponse,
    ReconciliationMatchResponse,
    ReconciliationRunResponse,
)
from backend.app.services.reconciliation.reconciliation_service import (
    ReconciliationService,
)

router = APIRouter(tags=["reconciliation"])

DatabaseSession = Annotated[Session, Depends(get_db_session)]


@router.post(
    "/reconciliation/run",
    response_model=ReconciliationRunResponse,
)
def run_reconciliation(
    session: DatabaseSession,
) -> ReconciliationRunResponse:
    service = ReconciliationService(
        unit_of_work=UnitOfWork(session),
    )

    matched = service.reconcile()

    return ReconciliationRunResponse(matched=matched)


@router.get(
    "/reconciliation/matches",
    response_model=list[ReconciliationMatchResponse],
)
def list_reconciliation_matches(
    session: DatabaseSession,
) -> list[ReconciliationMatch]:
    repository = ReconciliationRepository(session)
    return repository.list_all()


@router.get(
    "/overview",
    response_model=FinanceOverviewResponse,
)
def get_finance_overview(
    session: DatabaseSession,
) -> FinanceOverviewResponse:
    total_invoices = session.scalar(
        select(func.count()).select_from(Invoice),
    )
    paid_invoices = session.scalar(
        select(func.count())
        .select_from(Invoice)
        .where(Invoice.status == InvoiceStatus.PAID),
    )
    open_invoices = session.scalar(
        select(func.count())
        .select_from(Invoice)
        .where(Invoice.status == InvoiceStatus.OPEN),
    )

    total_payments = session.scalar(
        select(func.count()).select_from(Payment),
    )
    matched_payments = session.scalar(
        select(func.count())
        .select_from(Payment)
        .where(Payment.status == PaymentStatus.MATCHED),
    )
    unmatched_payments = session.scalar(
        select(func.count())
        .select_from(Payment)
        .where(Payment.status == PaymentStatus.UNMATCHED),
    )
    needs_review_payments = session.scalar(
        select(func.count())
        .select_from(Payment)
        .where(Payment.status == PaymentStatus.NEEDS_REVIEW),
    )

    reconciliation_matches = session.scalar(
        select(func.count()).select_from(ReconciliationMatch),
    )

    return FinanceOverviewResponse(
        total_invoices=total_invoices or 0,
        paid_invoices=paid_invoices or 0,
        open_invoices=open_invoices or 0,
        total_payments=total_payments or 0,
        matched_payments=matched_payments or 0,
        unmatched_payments=unmatched_payments or 0,
        needs_review_payments=needs_review_payments or 0,
        reconciliation_matches=reconciliation_matches or 0,
    )