from fastapi import FastAPI

app = FastAPI(
    title="Clipster Payment Reconciliation",
    description="Payment and invoice reconciliation prototype.",
    version="0.1.0",
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
