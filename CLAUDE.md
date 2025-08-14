# CLAUDE.md - Backend

This file provides guidance to Claude Code when working specifically with the FastAPI backend application.

## Backend Architecture

This is a FastAPI application serving as the backend for a Tea Store e-commerce platform.

### Current State: MongoDB Migration
**⚠️ CRITICAL**: The backend is currently migrating from SQLite/PostgreSQL to MongoDB Atlas:
- **Active Routers**: Only `mongo_products` and `ai` (enabled in `app/main.py:41-42`)
- **Disabled Routers**: auth, leads, payments, orders, addresses, admin_products, webhooks
- **Database**: MongoDB Atlas with Beanie ODM exclusively
- **Authentication**: Backend auth disabled during migration (frontend uses Clerk)

### Directory Structure
```
app/
├── core/           # Database connections, settings, admin guards
├── models/         # Both legacy SQLAlchemy and active MongoDB/Beanie models
├── routers/        # API endpoints (many disabled during migration)
├── services/       # Business logic (inventory, notifications, shipping)
├── scripts/        # Database setup and seeding utilities
└── main.py         # FastAPI application entry point
```

## Development Commands

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Database management
python -m app.scripts.setup_atlas  # Setup/reset MongoDB Atlas
python -m app.scripts.seed         # Seed with sample data
```

### Docker Development
```bash
# From project root
make up    # Start all services
make seed  # Seed database
```

## Key Files

### Core Configuration
- `app/main.py` - FastAPI app with enabled routers
- `app/core/db.py` - Database configuration
- `app/core/mongodb.py` - MongoDB Atlas connection
- `requirements.txt` - Python dependencies

### Active Models (MongoDB/Beanie)
- `app/models/mongo_models.py` - Primary MongoDB models
- `app/models/product.py` - Product model
- `app/models/user.py` - User model
- `app/models/cart_order.py` - Cart and order models

### Active Routers
- `app/routers/mongo_products.py` - Product CRUD operations
- `app/routers/ai.py` - AI chatbot integration

### Disabled During Migration
- `app/routers/auth.py` - Authentication (uses SQLAlchemy)
- `app/routers/payments.py` - Payment processing
- `app/routers/orders.py` - Order management
- `app/routers/addresses.py` - Address management
- `app/routers/admin_products.py` - Admin product operations
- `app/routers/webhooks.py` - Payment webhooks

## Database

### MongoDB Atlas Setup
- Use `python -m app.scripts.setup_atlas` to initialize database
- Connection configured in `app/core/mongodb.py`
- Models use Beanie ODM for async document operations

### Environment Variables
```bash
# Required in .env file
MONGODB_URL=mongodb+srv://...
DATABASE_NAME=tea_store
```

## API Documentation

- **Local**: http://localhost:8000/docs
- **Endpoints**: Only `/products/*` and `/ai/*` currently active
- **CORS**: Configured for frontend domains in main.py

## Integration Points

### External Services
- **AI**: OpenAI integration for chatbot (`app/routers/ai.py`)
- **Payments**: Razorpay (disabled during migration)
- **Shipping**: Shiprocket (stubbed in services)
- **Notifications**: WhatsApp integration planned

### TODO Blocks
- Razorpay webhook implementation
- Shiprocket API integration
- Auth system migration to MongoDB
- Payment processing restoration

## Development Notes

- No test framework currently configured
- Use async/await patterns throughout
- Follow FastAPI conventions for dependency injection
- MongoDB operations use Beanie ODM syntax
- Legacy SQLAlchemy code remains but is disabled
- All new development should use MongoDB/Beanie models