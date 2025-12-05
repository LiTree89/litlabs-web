"""
Integration endpoints for external services (Stripe, Firebase, etc.)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional, List
import os

from database import get_db
from models import User, Subscription, Transaction
from schemas import (
    UserCreate, 
    UserResponse, 
    UserUpdate,
    SubscriptionCreate,
    SubscriptionResponse,
    TransactionCreate,
    TransactionResponse
)

router = APIRouter(prefix="/api/integrations", tags=["integrations"])


# User integration endpoints
@router.post("/users/sync", response_model=UserResponse)
async def sync_user_from_firebase(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Sync user data from Firebase Authentication.
    Creates a new user if not exists, updates if exists.
    """
    # Check if user already exists
    existing_user = db.query(User).filter(User.uid == user_data.uid).first()
    
    if existing_user:
        # Update existing user
        for key, value in user_data.model_dump(exclude_unset=True).items():
            setattr(existing_user, key, value)
        db.commit()
        db.refresh(existing_user)
        return existing_user
    
    # Create new user
    new_user = User(**user_data.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/users/{uid}", response_model=UserResponse)
async def get_user_by_uid(uid: str, db: Session = Depends(get_db)):
    """Get user by Firebase UID."""
    user = db.query(User).filter(User.uid == uid).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/users/{uid}", response_model=UserResponse)
async def update_user(
    uid: str,
    user_update: UserUpdate,
    db: Session = Depends(get_db)
):
    """Update user information."""
    user = db.query(User).filter(User.uid == uid).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)
    
    db.commit()
    db.refresh(user)
    return user


# Subscription integration endpoints
@router.post("/subscriptions", response_model=SubscriptionResponse)
async def create_subscription(
    subscription_data: SubscriptionCreate,
    db: Session = Depends(get_db)
):
    """Create a new subscription record."""
    new_subscription = Subscription(**subscription_data.model_dump())
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return new_subscription


@router.get("/subscriptions/user/{user_id}", response_model=List[SubscriptionResponse])
async def get_user_subscriptions(user_id: int, db: Session = Depends(get_db)):
    """Get all subscriptions for a user."""
    subscriptions = db.query(Subscription).filter(
        Subscription.user_id == user_id
    ).all()
    return subscriptions


@router.put("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
async def update_subscription(
    subscription_id: int,
    status: str,
    plan: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Update subscription status."""
    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()
    
    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subscription not found"
        )
    
    subscription.status = status
    if plan:
        subscription.plan = plan
    
    db.commit()
    db.refresh(subscription)
    return subscription


# Transaction integration endpoints
@router.post("/transactions", response_model=TransactionResponse)
async def create_transaction(
    transaction_data: TransactionCreate,
    db: Session = Depends(get_db)
):
    """Record a new transaction."""
    new_transaction = Transaction(**transaction_data.model_dump())
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction


@router.get("/transactions/user/{user_id}", response_model=List[TransactionResponse])
async def get_user_transactions(user_id: int, db: Session = Depends(get_db)):
    """Get all transactions for a user."""
    transactions = db.query(Transaction).filter(
        Transaction.user_id == user_id
    ).all()
    return transactions


# Stripe webhook endpoint
@router.post("/stripe/webhook")
async def stripe_webhook(db: Session = Depends(get_db)):
    """
    Handle Stripe webhook events.
    Note: In production, this should verify the webhook signature.
    """
    # Placeholder for Stripe webhook handling
    # In production, implement proper signature verification
    # and event handling logic
    return {"status": "received"}


# Health check for integrations
@router.get("/health")
async def integration_health_check():
    """Check health of integration services."""
    return {
        "status": "healthy",
        "services": {
            "database": "connected",
            "stripe": "configured" if os.getenv("STRIPE_SECRET_KEY") else "not_configured",
            "firebase": "configured" if os.getenv("FIREBASE_PROJECT_ID") else "not_configured"
        }
    }
