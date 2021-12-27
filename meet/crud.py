from datetime import datetime, time
from typing import Optional, Union

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from starlette import status

from user.models import User
from user.crud import get_user, get_user_by_email
from . import models, schemas


def add_users_for_meet(
    db: Session,
    meet: Optional[Union[schemas.MeetCreate, schemas.MeetUpdate]] = None,
    for_update: bool = False,
    current_meet: Optional[models.Meet] = None,
):
    if meet.users_add:
        for user in list(set(meet.users_add)):
            if isinstance(user, int):
                db_user = get_user(db, user_id=user)
                if db_user:
                    if for_update:
                        meeting_user_by_id = get_meeting_user(
                            db, current_meet_id=current_meet.id, user_id=user
                        )
                        if meeting_user_by_id:
                            continue
                        meeting_user = models.MeetingUsers(
                            meet_id=current_meet.id, user_id=user
                        )
                        db.add(meeting_user)
                    else:
                        meeting_users = models.MeetingUsers(
                            meet_id=current_meet.id, user_id=user
                        )
                        db.add(meeting_users)
            if isinstance(user, str):
                db_user = get_user_by_email(db, email=user)
                if db_user:
                    if for_update:
                        meeting_user_by_email = get_meeting_user(
                            db,
                            current_meet_id=current_meet.id,
                            user_id=db_user.id,
                        )
                        if meeting_user_by_email:
                            continue
                        meeting_user = models.MeetingUsers(
                            meet_id=current_meet.id, user_id=db_user.id
                        )
                        db.add(meeting_user)
                    else:
                        if db_user.id in meet.users_add:
                            continue
                        meeting_users = models.MeetingUsers(
                            meet_id=current_meet.id, user_id=db_user.id
                        )
                        db.add(meeting_users)
        if not for_update:
            db.commit()


def get_meeting_user(db: Session, current_meet_id: int, user_id: int):
    return (
        db.query(models.MeetingUsers)
        .filter(
            models.MeetingUsers.user_id == user_id,
            models.MeetingUsers.meet_id == current_meet_id,
        )
        .first()
    )


def get_current_meet(db: Session, title: str, user_id: int):
    return (
        db.query(models.Meet)
        .filter(models.Meet.title == title, models.Meet.owner_id == user_id)
        .first()
    )


def get_meets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Meet).offset(skip).limit(limit).all()


def create_user_meet(db: Session, meet: schemas.MeetCreate, user_id: int):
    current_meet = get_current_meet(db, title=meet.title, user_id=user_id)
    if current_meet:
        return HTTPException(
            status_code=status.HTTP_200_OK,
            detail='The meeting has already been created',
        )
    db_meet = models.Meet(
        title=meet.title,
        owner_id=user_id,
        created_at=datetime.now(),
        meeting_time=datetime.combine(meet.date, meet.get_time),
    )
    db.add(db_meet)
    db.commit()
    add_users_for_meet(db, meet=meet, current_meet=db_meet)
    return HTTPException(
        status_code=status.HTTP_201_CREATED, detail='Meeting created'
    )


def update_meet(db: Session, meet: schemas.MeetUpdate, user_id: int):
    current_meet = get_current_meet(db, title=meet.title, user_id=user_id)
    if current_meet is None:
        return HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Not Found'
        )
    if meet.new_title != 'string':
        current_meet.title = meet.new_title
    if meet.update_time and meet.update_date:
        current_meet.meeting_time = datetime.combine(meet.date, meet.get_time)
    else:
        if meet.update_time:
            meet_time = meet.get_time
            current_meet.meeting_time = datetime.combine(
                current_meet.meeting_time.date(), meet_time
            )
        if meet.update_date:
            meet_time = time(
                int(current_meet.meeting_time.hour),
                int(current_meet.meeting_time.minute),
            )
            current_meet.meeting_time = datetime.combine(meet.date, meet_time)
    add_users_for_meet(
        db, meet=meet, current_meet=current_meet, for_update=True
    )
    if meet.users_delete:
        for user in list(set(meet.users_delete)):
            if isinstance(user, int):
                db_user = get_user(db, user_id=user)
                if db_user:
                    meeting_user = get_meeting_user(
                        db, current_meet_id=current_meet.id, user_id=user
                    )
                    if meeting_user:
                        db.delete(meeting_user)
            if isinstance(user, str):
                db_user = get_user_by_email(db, email=user)
                if db_user:
                    meeting_user = get_meeting_user(
                        db, current_meet_id=current_meet.id, user_id=db_user.id
                    )
                    if meeting_user:
                        db.delete(meeting_user)

    db.commit()
    return HTTPException(
        status_code=status.HTTP_200_OK, detail='the meeting has been updated'
    )


def delete_meet(
    db: Session,
    title: Optional[str] = None,
    all_meet: Optional[bool] = False,
    current_user: Optional[User] = None,
):
    try:
        if all_meet:
            meets = (
                db.query(models.Meet)
                .filter(models.Meet.owner_id == current_user.id)
                .all()
            )
            for meet in meets:
                meeting_users = (
                    db.query(models.MeetingUsers)
                    .filter(models.MeetingUsers.meet_id == meet.id)
                    .all()
                )
                for meeting_user in meeting_users:
                    db.delete(meeting_user)
                db.delete(meet)

            db.commit()
            return HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f'All meets for {current_user.username} have been deleted',
            )
        else:
            meet = (
                db.query(models.Meet)
                .filter(
                    models.Meet.title == title,
                    models.Meet.owner_id == current_user.id,
                )
                .one()
            )
            meeting_users = (
                db.query(models.MeetingUsers)
                .filter(models.MeetingUsers.meet_id == meet.id)
                .all()
            )
            for meeting_user in meeting_users:
                db.delete(meeting_user)
            db.delete(meet)
            db.commit()
            return HTTPException(
                status_code=status.HTTP_200_OK,
                detail=f'Meet {title} for {current_user.username} have been deleted',
            )
    except NoResultFound:
        raise HTTPException(status_code=400, detail='Not found')
