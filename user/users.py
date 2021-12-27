from typing import List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from starlette import status
from jose import JWTError, jwt


from config import settings
from dependencies import oauth2_sheme, get_db
from . import schemas, crud, models

router = APIRouter(
    prefix='/users',
    tags=['Users'],
    responses={404: {'description': 'Not found'}},
)


async def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_sheme)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


@router.post('/registration', response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user_email = crud.get_user_by_email(db, email=user.email)
    db_user_username = crud.get_user_by_username(db, user.username)
    if db_user_email:
        raise HTTPException(status_code=400, detail='Email already registered')
    if db_user_username:
        raise HTTPException(
            status_code=400, detail='Username already registered'
        )
    return crud.create_user(db=db, user=user)


@router.get('/', response_model=List[schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 100,
    token: str = Depends(oauth2_sheme),
    db: Session = Depends(get_db),
):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@router.get('/{username}', response_model=schemas.User)
def read_user(
    username: str,
    token: str = Depends(oauth2_sheme),
    db: Session = Depends(get_db),
):
    db_user = crud.get_user_by_username(db, username=username)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return db_user


@router.get("/me/", response_model=schemas.User)
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    print(current_user.username)
    return current_user
