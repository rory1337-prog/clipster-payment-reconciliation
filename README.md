![Python](https://img.shields.io/badge/Python-3.14-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.116-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red)
![Pytest](https://img.shields.io/badge/Tests-Passing-success)

# Clipster Payment & Invoice Reconciliation

Backend service for importing financial data from multiple payment providers, normalizing records, and automatically reconciling incoming payments with invoices.

The project was built as a technical assignment for **Clipster**.

---

## Overview

Finance teams often receive payments through multiple providers while invoices are generated in a separate accounting system.

This project demonstrates how such data can be consolidated into a single system that:

- imports invoices and payments from multiple providers
- normalizes provider-specific data into a common format
- automatically matches payments to invoices
- identifies ambiguous and unmatched transactions
- provides a finance overview through a REST API

The application follows a layered architecture and is designed to be easily extended with new payment providers or reconciliation strategies.

---

## Features

### Data Import

Supports importing mocked data from:

- QuickBooks (Invoices)
- Stripe
- PayPal
- Mercury
- Cryptocurrency payments

Provider-specific payloads are normalized into unified domain models before being stored in PostgreSQL.

---

### Automatic Reconciliation

Payments are matched to invoices using deterministic business rules.

Matching priority:

1. Exact invoice reference
2. Customer email + amount + currency
3. Customer name + amount + currency

Every successful reconciliation includes:

- matching method
- confidence score
- explanation

---

### Finance Dashboard

Provides aggregated information including:

- total invoices
- paid invoices
- open invoices
- total payments
- matched payments
- unmatched payments
- payments requiring manual review

---

## Tech Stack

| Category | Technologies |
|-----------|--------------|
| Language | Python 3.14 |
| API | FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.0 |
| Validation | Pydantic v2 |
| Database Migrations | Alembic |
| Testing | Pytest |
| Linting | Ruff |
| Containerization | Docker & Docker Compose |

---

## Architecture

```
                 +-------------------+
                 |   Payment Files   |
                 +-------------------+
                           |
                           v
                 +-------------------+
                 |     Importers     |
                 +-------------------+
                           |
                           v
                 +-------------------+
                 |    Normalizers    |
                 +-------------------+
                           |
                           v
                 +-------------------+
                 |    PostgreSQL     |
                 +-------------------+
                           |
                           v
                 +-------------------+
                 | Reconciliation    |
                 |     Service       |
                 +-------------------+
                           |
                           v
                 +-------------------+
                 |    FastAPI API    |
                 +-------------------+
```

The project follows a layered architecture:

```
API
 ↓
Services
 ↓
Repositories
 ↓
SQLAlchemy
 ↓
PostgreSQL
```

Business logic is isolated inside the service layer while repositories are responsible only for data access.

---

## Project Structure

```
backend/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   │   ├── importers/
│   │   └── reconciliation/
│   └── main.py
│
├── mock_data/
│
└── tests/
```

---

## Reconciliation Strategy

| Rule | Confidence |
|------|-----------:|
| Exact invoice reference | 1.00 |
| Email + Amount + Currency | 0.98 |
| Name + Amount + Currency | 0.90 |

Transactions that cannot be matched remain **UNMATCHED**.

Ambiguous transactions can be marked as **NEEDS_REVIEW**.

---

# REST API

Interactive API documentation:

```
http://localhost:8000/docs
```

---

## Health Check

```
GET /health
```

```
GET /health/db
```

---

## Run Reconciliation

```
POST /reconciliation/run
```

Example response:

```json
{
  "matched": 3
}
```

---

## Reconciliation Matches

```
GET /reconciliation/matches
```

Example:

```json
[
  {
    "payment_id": 1,
    "invoice_id": 1,
    "method": "exact_reference",
    "confidence_score": 1.0
  }
]
```

---

## Finance Overview

```
GET /overview
```

Example response:

```json
{
  "total_invoices": 5,
  "paid_invoices": 3,
  "open_invoices": 2,
  "total_payments": 7,
  "matched_payments": 3,
  "unmatched_payments": 4,
  "needs_review_payments": 0,
  "reconciliation_matches": 3
}
```

---

# Getting Started

## Clone repository

```bash
git clone https://github.com/rory1337-prog/clipster-payment-reconciliation.git

cd clipster-payment-reconciliation
```

---

## Configure environment

```bash
cp .env.example .env
```

Update database settings if necessary.

---

## Start PostgreSQL

```bash
docker compose up -d
```

---

## Apply migrations

```bash
alembic upgrade head
```

---

## Run API

```bash
uvicorn backend.app.main:app --reload
```

Open:

```
http://localhost:8000/docs
```

---

# Running Tests

```bash
pytest
```

---

# Code Quality

```bash
ruff check backend
```

---

# Example Workflow

```
Mock Provider Data
        │
        ▼
 Import Service
        │
        ▼
 Normalization
        │
        ▼
 PostgreSQL
        │
        ▼
 Reconciliation
        │
        ▼
 Finance Overview
```

---

# Future Improvements

- AI-assisted reconciliation
- Fuzzy string matching
- Background reconciliation jobs
- Audit trail
- Manual reconciliation endpoint
- CSV export
- Webhooks for payment providers

---

# Author

**Rostyslav Ryzhkov**

Python Backend Developer | AI Automation Engineer

- GitHub: https://github.com/rory1337-prog
- LinkedIn: https://linkedin.com/in/rostyslavryzhkov