"""
GLAMFLOW AI - FastAPI Backend Application

This is the main entry point for the FastAPI backend that integrates
with the frontend and provides API endpoints for user management,
subscriptions, and chatbot functionality.
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import os

from database import get_db, init_db, Base, engine
from models import User, Subscription, Transaction
from schemas import (
    UserCreate,
    UserResponse,
    ChatMessageRequest,
    ChatMessageResponse,
    HealthCheck
)
from integration_endpoints import router as integration_router

# Create FastAPI application
app = FastAPI(
    title="GLAMFLOW AI API",
    description="Backend API for GLAMFLOW AI - Beauty Business Automation Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "https://studio-4627045237-a2fe9.web.app",
    "https://studio-4627045237-a2fe9.firebaseapp.com",
]

# Allow additional origins from environment
additional_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
origins.extend([o.strip() for o in additional_origins if o.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(integration_router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()


# Health check endpoint
@app.get("/", response_model=HealthCheck)
async def root():
    """Root endpoint - health check."""
    return HealthCheck(
        status="healthy",
        message="GLAMFLOW AI API is running"
    )


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    return HealthCheck(
        status="healthy",
        message="All systems operational"
    )


# User endpoints
@app.post("/api/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user."""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.uid == user.uid)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or UID already exists"
        )
    
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/api/users/{uid}", response_model=UserResponse)
async def get_user(uid: str, db: Session = Depends(get_db)):
    """Get user by Firebase UID."""
    user = db.query(User).filter(User.uid == uid).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


# Chatbot endpoint
@app.post("/api/chat", response_model=ChatMessageResponse)
async def chat(request: ChatMessageRequest, db: Session = Depends(get_db)):
    """
    Process a chat message and return a response.
    This is a simple rule-based chatbot for demonstration.
    """
    message = request.message.lower()
    session_id = request.session_id or "default"
    
    # Simple rule-based responses
    responses = {
        "greeting": {
            "keywords": ["hello", "hi", "hey"],
            "response": "Hey there! 👋 Welcome to GLAMFLOW AI. I can help you with content creation, client management, and business automation. What would you like to know?"
        },
        "content": {
            "keywords": ["content", "create", "post", "video"],
            "response": "I can help you generate social media content! 📱 Tell me what type (reels, posts, stories) and your beauty niche, and I'll create it for you in minutes!"
        },
        "pricing": {
            "keywords": ["price", "cost", "subscription", "premium"],
            "response": "GLAMFLOW AI offers:\n💰 FREE: 5 posts/month\n✨ PRO: $29/mo - Unlimited content\n🔥 ENTERPRISE: Custom pricing\n\nInterested in upgrading?"
        },
        "features": {
            "keywords": ["features", "what can", "capabilities"],
            "response": "✅ AI Content Generation\n✅ Community Chat\n✅ Manager Bot\n✅ Analytics\n✅ Client Management\n\nWhich would you like to learn about?"
        }
    }
    
    # Find matching response
    for category, data in responses.items():
        if any(keyword in message for keyword in data["keywords"]):
            return ChatMessageResponse(
                response=data["response"],
                session_id=session_id
            )
    
    # Default response
    return ChatMessageResponse(
        response="That's interesting! Tell me more. Are you interested in content creation, client management, or learning about our features?",
        session_id=session_id
    )


# Dashboard stats endpoint
@app.get("/api/dashboard/stats/{uid}")
async def get_dashboard_stats(uid: str, db: Session = Depends(get_db)):
    """Get dashboard statistics for a user."""
    user = db.query(User).filter(User.uid == uid).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Get subscription info
    subscription = db.query(Subscription).filter(
        Subscription.user_id == user.id
    ).order_by(Subscription.created_at.desc()).first()
    
    # Get transaction stats
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user.id
    ).all()
    
    total_revenue = sum(t.amount for t in transactions if t.type == "subscription_upgrade")
    
    return {
        "user": {
            "id": user.id,
            "uid": user.uid,
            "email": user.email,
            "display_name": user.display_name,
            "tier": user.tier,
            "status": user.status
        },
        "subscription": {
            "plan": subscription.plan if subscription else "free",
            "status": subscription.status if subscription else "active",
            "next_billing_date": subscription.next_billing_date if subscription else None
        },
        "stats": {
            "posts_created": 0,  # Would be tracked in a posts table
            "messages_used": 0,  # Would be tracked in messages table
            "total_revenue": total_revenue
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    )
