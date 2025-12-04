"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# User Schemas
class UserBase(BaseModel):
    """Base schema for user data."""
    email: EmailStr
    display_name: Optional[str] = None


class UserCreate(UserBase):
    """Schema for creating a new user."""
    uid: str
    photo_url: Optional[str] = None


class UserUpdate(BaseModel):
    """Schema for updating user data."""
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
    tier: Optional[str] = None
    status: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response."""
    id: int
    uid: str
    tier: str
    status: str
    stripe_customer_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Subscription Schemas
class SubscriptionBase(BaseModel):
    """Base schema for subscription data."""
    plan: str = "free"
    status: str = "active"


class SubscriptionCreate(SubscriptionBase):
    """Schema for creating a subscription."""
    user_id: int
    stripe_subscription_id: Optional[str] = None


class SubscriptionResponse(SubscriptionBase):
    """Schema for subscription response."""
    id: int
    user_id: int
    created_at: datetime
    ends_at: Optional[datetime] = None
    next_billing_date: Optional[datetime] = None

    class Config:
        from_attributes = True


# Transaction Schemas
class TransactionBase(BaseModel):
    """Base schema for transaction data."""
    type: str
    amount: float
    currency: str = "USD"


class TransactionCreate(TransactionBase):
    """Schema for creating a transaction."""
    user_id: int
    stripe_session_id: Optional[str] = None
    stripe_invoice_id: Optional[str] = None


class TransactionResponse(TransactionBase):
    """Schema for transaction response."""
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


# Chatbot Schemas
class ChatMessageRequest(BaseModel):
    """Schema for incoming chat messages."""
    message: str
    session_id: Optional[str] = None


class ChatMessageResponse(BaseModel):
    """Schema for chat message response."""
    response: str
    session_id: str


# Auth Schemas
class TokenData(BaseModel):
    """Schema for token data."""
    uid: str
    email: Optional[str] = None


# Health Check
class HealthCheck(BaseModel):
    """Schema for health check response."""
    status: str
    message: str
