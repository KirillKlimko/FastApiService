from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from dependencies import oauth2_sheme, get_db
from user import models, users
from . import schemas, crud


router = APIRouter(
    prefix='/meets',
    tags=['Meets'],
    responses={404: {'description': 'Not found'}},
)


@router.post('/create/')
def create_meet_for_user(
    meet: schemas.MeetCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(users.get_current_user),
):
    return crud.create_user_meet(db=db, meet=meet, user_id=current_user.id)


@router.post('/update/')
def update_meet_for_user(
    meet: schemas.MeetUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(users.get_current_user),
):
    return crud.update_meet(db=db, meet=meet, user_id=current_user.id)


@router.get('/', response_model=List[schemas.Meet])
def read_meets(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_sheme),
):
    return crud.get_meets(db, skip=skip, limit=limit)


@router.post('/delete/meet/{meet_title}/')
async def delete_meets(
    meet_title: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(users.get_current_user),
):
    return crud.delete_meet(db, title=meet_title, current_user=current_user)


@router.post('/delete/all/')
def delete_all_meets(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(users.get_current_user),
):
    return crud.delete_meet(db, current_user=current_user, all_meet=True)
