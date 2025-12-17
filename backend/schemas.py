from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional

from .utils import ensure_utc, utcnow

class UserBase(BaseModel):
    email: EmailStr
    # Accept `displayName` from frontend but use `display_name` internally
    display_name: str = Field(..., alias='displayName')

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_admin: bool
    created_at: datetime = Field(default_factory=utcnow)

    class Config:
        from_attributes = True
        populate_by_name = True

    @field_validator('created_at', mode='before')
    def _created_at_default(cls, v):
        return ensure_utc(v)

class EventBase(BaseModel):
    title: str
    description: str
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None

    @field_validator('start_time', 'end_time', mode='before')
    def _ensure_start_end_utc(cls, v):
        return ensure_utc(v)

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int
    created_by: int
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
    creator_name: Optional[str] = None

    class Config:
        from_attributes = True

    @field_validator('created_at', 'updated_at', mode='before')
    def _created_updated_default(cls, v):
        return ensure_utc(v)

class EventWithCreator(Event):
    creator: User


class AdminUpdate(BaseModel):
    is_admin: bool

    class Config:
        from_attributes = True
