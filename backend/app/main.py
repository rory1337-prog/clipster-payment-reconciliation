from fastapi import FastAPI
from sqlalchemy import text

from backend.app.api.reconciliation import router as reconciliation_router
from backend.app.db.session import engine

app = FastAPI(
    title="Clipster Payment Reconciliation",
    description="Payment and invoice reconciliation prototype.",
    version="0.1.0",
)

app.include_router(reconciliation_router)

@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/health/db")
def database_health_check() -> dict[str, str]:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }
