from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from .database import SessionLocal
from .models import User, Event
from .auth import get_current_user
from .schemas import AdminUpdate, User as UserSchema

router = APIRouter(prefix="/admin", tags=["admin"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_admin(current_user=Depends(get_current_user)):
    if not getattr(current_user, 'is_admin', False):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin privileges required")
    return current_user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete events created by this user first (if any)
    db.query(Event).filter(Event.created_by == user_id).delete(synchronize_session=False)
    db.delete(user)
    db.commit()
    return {}


@router.get("/users", response_model=List[UserSchema])
def list_users(admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.created_at.desc()).all()
    result = []
    for u in users:
        user_schema = UserSchema.model_validate(u)
        result.append(user_schema.model_dump())
    return result


@router.put("/users/{user_id}/admin", response_model=UserSchema)
def set_user_admin(user_id: int, payload: AdminUpdate, admin=Depends(get_current_admin), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_admin = payload.is_admin
    db.commit()
    db.refresh(user)
    user_schema = UserSchema.model_validate(user)
    return user_schema.model_dump()
