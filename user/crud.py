from datetime import datetime

from sqlalchemy.orm import Session

import validators
from config import settings
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).get(user_id)


def get_user_by_username(db: Session, username: str):
    return (
        db.query(models.User).filter(models.User.username == username).first()
    )


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    user = validators.validate_user(
        password=user.password,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
    )
    hashed_password = settings.pwd_context.hash(user.get('password'))
    db_user = models.User(
        email=user.get('email'),
        password=hashed_password,
        username=user.get('username'),
        first_name=user.get('first_name'),
        last_name=user.get('last_name'),
        created_at=datetime.now(),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
