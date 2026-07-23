# Clipster Payment & Invoice Reconciliation

A backend service that imports invoices and payments from multiple providers, normalizes the data into a unified format, stores it in PostgreSQL, and automatically reconciles payments with invoices using configurable matching rules.

## Features

- Import invoices and payments from multiple providers
- Normalize provider-specific payloads into canonical models
- Store data in PostgreSQL
- Automatic payment reconciliation
- Repository Pattern + Unit of Work architecture
- REST API built with FastAPI
- Finance overview dashboard endpoint
- Docker support
- Pytest test suite
- Ruff linting

---

## Tech Stack

- Python 3.14
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Docker & Docker Compose
- Pydantic v2
- Pytest
- Ruff

---

## Project Structure

```
backend/
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
├── mock_data/
└── tests/
```

---

## Architecture

The application follows a layered architecture.

```
API
 │
 ▼
Services
 │
 ▼
Repositories
 │
 ▼
SQLAlchemy
 │
 ▼
PostgreSQL
```

Business logic is isolated inside the service layer, while repositories are responsible only for data access.

---

## Reconciliation Strategy

Payments are matched against invoices using deterministic rules.

Priority:

1. Exact invoice reference
2. Customer email + amount + currency
3. Customer name + amount + currency

Each successful match receives a confidence score.

| Rule | Confidence |
|------|-----------:|
| Exact reference | 1.00 |
| Email + amount + currency | 0.98 |
| Name + amount + currency | 0.90 |

If no rule matches, the payment remains unmatched.

---

## API

### Health

```
GET /health
```

```
GET /health/db
```

---

### Run reconciliation

```
POST /reconciliation/run
```

Example response

```json
{
  "matched": 3
}
```

---

### List matches

```
GET /reconciliation/matches
```

---

### Finance overview

```
GET /overview
```

Example response

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

## Running locally

Clone the repository.

```bash
git clone https://github.com/rory1337-prog/clipster-payment-reconciliation.git

cd clipster-payment-reconciliation
```

Create an environment file.

```bash
cp .env.example .env
```

Start PostgreSQL.

```bash
docker compose up -d
```

Run database migrations.

```bash
alembic upgrade head
```

Start the API.

```bash
uvicorn backend.app.main:app --reload
```

Open Swagger UI.

```
http://localhost:8000/docs
```

---

## Running tests

```bash
pytest
```

---

## Linting

```bash
ruff check backend
```

---

## Example Workflow

1. Import provider data
2. Store normalized records in PostgreSQL
3. Execute reconciliation
4. Inspect reconciliation matches
5. View finance overview

---

## Future Improvements

- AI-assisted matching
- Fuzzy name matching
- Background reconciliation jobs
- Audit logs
- Manual reconciliation endpoint
- Batch reconciliation scheduling

---

## Author

**Rostyslav Ryzhkov**

Python Backend Developer / AI Automation Engineer

- GitHub: https://github.com/rory1337-prog
- LinkedIn: https://linkedin.com/in/rostyslavryzhkov