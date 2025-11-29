from sqlalchemy.orm import Session
from app.models.users import User
from app.schemas.users import UserCreate, UserUpdate
from app.utils.security import get_password_hash


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user_in: UserCreate):
    hashed = get_password_hash(user_in.password)
    db_user = User(name=user_in.name, email=user_in.email, hashed_password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: User, user_in: UserUpdate):
    if user_in.name is not None:
      user.name = user_in.name
    if user_in.email is not None:
      user.email = user_in.email
    if user_in.is_active is not None:
      user.is_active = user_in.is_active
    db.add(user)
    db.commit()
    db.refresh(user)
    return user