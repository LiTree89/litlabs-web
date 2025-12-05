# GLAMFLOW AI Backend

This is the FastAPI backend for the GLAMFLOW AI application. It provides REST API endpoints for user management, subscriptions, transactions, and chatbot functionality.

## Quick Start

### Prerequisites
- Python 3.9+
- pip

### Installation

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the environment file and configure:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the application:
```bash
python -m uvicorn app:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app.py                 # Main FastAPI application
├── database.py            # Database configuration and session management
├── models.py              # SQLAlchemy ORM models
├── schemas.py             # Pydantic schemas for validation
├── integration_endpoints.py # Integration endpoints for external services
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment variables
└── README.md             # This file
```

## API Endpoints

### Health Check
- `GET /` - Root health check
- `GET /health` - Detailed health check

### Users
- `POST /api/users` - Create a new user
- `GET /api/users/{uid}` - Get user by Firebase UID

### Chat
- `POST /api/chat` - Send a chat message and get a response

### Dashboard
- `GET /api/dashboard/stats/{uid}` - Get dashboard statistics for a user

### Integrations
- `POST /api/integrations/users/sync` - Sync user from Firebase
- `GET /api/integrations/users/{uid}` - Get user by UID
- `PUT /api/integrations/users/{uid}` - Update user
- `POST /api/integrations/subscriptions` - Create subscription
- `GET /api/integrations/subscriptions/user/{user_id}` - Get user subscriptions
- `POST /api/integrations/transactions` - Create transaction
- `GET /api/integrations/transactions/user/{user_id}` - Get user transactions
- `POST /api/integrations/stripe/webhook` - Stripe webhook handler
- `GET /api/integrations/health` - Integration services health check

## Database

The application uses SQLAlchemy with SQLite by default. For production, configure PostgreSQL using the `DATABASE_URL` environment variable.

### Models
- **User**: User account information
- **Subscription**: User subscription details
- **Transaction**: Payment transaction records
- **ChatbotConversation**: Chat session tracking
- **ChatbotMessage**: Individual chat messages

## Integration with Frontend

The backend is designed to work with the Firebase-based frontend. The frontend can make API calls to these endpoints to:
1. Sync user data from Firebase Authentication
2. Get chatbot responses
3. Track subscriptions and transactions
4. Get dashboard statistics

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | Database connection string | sqlite:///./glamflow.db |
| STRIPE_SECRET_KEY | Stripe secret key | None |
| STRIPE_WEBHOOK_SECRET | Stripe webhook secret | None |
| FIREBASE_PROJECT_ID | Firebase project ID | None |
| ALLOWED_ORIGINS | Comma-separated CORS origins | None |
| PORT | Server port | 8000 |
