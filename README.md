# Tea Store Backend

FastAPI backend for Tea Store e-commerce platform.

## Quick Start

```bash
# Setup
cp .env.example .env
pip install -r requirements.txt

# Database
python -m app.scripts.setup_atlas
python -m app.scripts.seed

# Run
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Docker

```bash
# From project root
make up
make seed
```

## API

- **Docs**: http://localhost:8000/docs
- **Active**: `/products/*`, `/ai/*`
- **Disabled**: auth, payments, orders, addresses, admin, webhooks

## Status

⚠️ **Migrating to MongoDB Atlas** - Many features temporarily disabled.

## Environment

```env
MONGODB_URL=mongodb+srv://...
DATABASE_NAME=tea_store
OPENAI_API_KEY=sk-...
```

## Structure

```
app/
├── main.py         # FastAPI app
├── core/           # Config, DB
├── models/         # MongoDB models
├── routers/        # API endpoints
├── services/       # Business logic
└── scripts/        # DB utilities
```