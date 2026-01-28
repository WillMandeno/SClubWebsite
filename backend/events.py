from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .database import SessionLocal
from .models import Event, User
from .schemas import EventCreate, Event as EventSchema, EventWithCreator
from .auth import get_current_user
from .utils import ensure_utc, utcnow
from datetime import datetime
from datetime import timezone

router = APIRouter(prefix="/events", tags=["events"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def ensure_z(dt: datetime) -> str:
    """Convert naive or aware datetime to ISO string with Z"""
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    else:
        dt = dt.astimezone(timezone.utc)
    return dt.isoformat().replace('+00:00', 'Z')

@router.get("/", response_model=List[EventSchema])
def list_events(db: Session = Depends(get_db)):
    events = db.query(Event).join(User, Event.created_by == User.id).add_columns(User.display_name.label('creator_name')).order_by(Event.start_time).all()
    result = []
    for e in events:
        event_dict = e[0].__dict__.copy()
        event_dict['creator_name'] = e[1]
        event_dict['start_time'] = ensure_z(event_dict['start_time'])
        event_dict['end_time'] = ensure_z(event_dict['end_time'])
        result.append(EventSchema.model_validate(event_dict).model_dump())
    return result


@router.post("/", response_model=EventSchema, status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    ev = Event(
        title=event.title,
        description=event.description,
        start_time=ensure_utc(event.start_time),
        end_time=ensure_utc(event.end_time),
        location=event.location,
        created_by=current_user.id,
        pending=event.pending,
    )
    # Ensure created_at/updated_at are set in Python as a fallback
    ev.created_at = utcnow()
    ev.updated_at = utcnow()
    db.add(ev)
    db.commit()
    db.refresh(ev)
    # Send ISO string with Z to frontend
    ev_dict = EventSchema.model_validate(ev).model_dump()
    ev_dict['start_time'] = ensure_z(ev.start_time)
    ev_dict['end_time'] = ensure_z(ev.end_time)
    return ev_dict


@router.put("/{event_id}", response_model=EventSchema)
def update_event(event_id: int, payload: EventCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    ev = db.query(Event).filter(Event.id == event_id).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found")
    if ev.created_by != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not allowed")
    ev.title = payload.title
    ev.description = payload.description
    ev.start_time = payload.start_time
    ev.end_time = payload.end_time
    ev.location = payload.location
    ev.pending = payload.pending
    ev.updated_at = utcnow()
    db.commit()
    db.refresh(ev)
    ev_dict = EventSchema.model_validate(ev).model_dump()
    ev_dict['start_time'] = ensure_z(ev.start_time)
    ev_dict['end_time'] = ensure_z(ev.end_time)
    return ev_dict


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    ev = db.query(Event).filter(Event.id == event_id).first()
    if not ev:
        raise HTTPException(status_code=404, detail="Event not found")
    if ev.created_by != current_user.id and not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Not allowed")
    db.delete(ev)
    db.commit()
    return {}
