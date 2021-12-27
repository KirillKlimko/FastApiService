import re

from fastapi import HTTPException


def validate_user(
    password: str, email: str, username: str, first_name: str, last_name: str
):
    if not re.match(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\da-zA-Z]).{6,}$', password
    ):
        raise HTTPException(status_code=400, detail='Incorrect password')

    if not re.match(
        r'^([a-z0-9_-]+\.)*[a-z0-9_-]+@[a-z0-9_-]+(\.[a-z0-9_-]+)*\.[a-z]{2,6}$',
        email,
    ):
        raise HTTPException(status_code=400, detail='Incorrect email')

    if not re.match(r'^(\w+){3,32}$', username):
        raise HTTPException(status_code=400, detail='Incorrect username')

    if not re.match(
        r'^([А-Я]{1}[а-яё]{1,23}|[A-Z]{1}[a-z]{1,23})$', first_name
    ):
        raise HTTPException(status_code=400, detail='Incorrect first name')

    if not re.match(
        r'^([А-Я]{1}[а-яё]{1,23}|[A-Z]{1}[a-z]{1,23})$', last_name
    ):
        raise HTTPException(status_code=400, detail='Incorrect last name')

    user = {
        'password': password,
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
    }
    return user
