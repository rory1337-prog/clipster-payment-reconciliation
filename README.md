# Clipster Payment Reconciliation

A prototype payment and invoice reconciliation system built for the Clipster Automation / AI Agent Operator challenge.

## Problem

Clipster receives payments through multiple channels, while invoices and financial records are managed separately. Matching payments with the correct invoices currently requires manual work.

## Planned solution

The system will:

- collect payments from multiple mocked providers;
- normalize provider-specific data;
- match payments with invoices;
- calculate a confidence score;
- identify unclear and unmatched transactions;
- provide a finance review interface;
- use AI only for ambiguous cases.

## Tech stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- OpenAI API
- React
- TypeScript
- Docker
- Pytest

## Development

```bash
python3.14 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements-dev.txt
uvicorn backend.app.main:app --reload
