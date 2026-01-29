from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from pydantic import BaseModel
import os

from .database import SessionLocal
from .models import User
from .schemas import UserCreate, User as UserSchema

from sqlalchemy.orm import Session

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')
ALGORITHM = os.getenv('ALGORITHM', 'HS256')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except ValueError:
        # bcrypt raises ValueError when the provided password is longer
        # than 72 bytes. Return a clear HTTP error so callers can handle it.
        raise HTTPException(
            status_code=400,
            detail=(
                "Password too long for bcrypt (72 bytes). "
                "Please reset your password or use a shorter one."
            ),
        )


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/register", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    # check existing
    existing = db.query(User).filter((User.email == user.email) | (User.display_name == user.display_name)).first()
    if existing:
        raise HTTPException(status_code=400, detail="User with that email or display name already exists")

    db_user = User(
        email=user.email,
        display_name=user.display_name,
        hashed_password=get_password_hash(user.password),
        is_admin=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # Return the Pydantic schema dump using aliases (camelCase) so the API
    # consistently returns keys like `displayName` for the frontend.
    user_schema = UserSchema.model_validate(db_user)
    return user_schema.model_dump(by_alias=True)


@router.post("/login", response_model=Token)
def login(form_data: dict, db: Session = Depends(get_db)):
    # form_data expected to contain 'email' and 'password'
    email = form_data.get('email')
    password = form_data.get('password')
    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password required")

    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.id == int(sub)).first()
    if user is None:
        raise credentials_exception
    return user


@router.get("/me", response_model=UserSchema)
def read_me(current_user: User = Depends(get_current_user)):
    user_schema = UserSchema.model_validate(current_user)
    return user_schema.model_dump(by_alias=True)
