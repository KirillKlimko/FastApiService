from celery import Celery
from fastapi import Depends
from sqlalchemy.orm import Session

from db import engine
from dependencies import get_db
from config import settings
from user.crud import get_user_by_email
from notification import send_mail
from meet import models


celery = Celery(__name__)
celery.conf.broker_url = settings.CELERY_BROKER_URL
celery.conf.result_backend = settings.CELERY_RESULT_BACKEND

session = Session(bind=engine)


@celery.task(name='send_mail')
def send_mail_task(
    to_gmail: str,
    meet_hour: float,
    time_until_meeting: int,
    first_name: str,
    last_name: str,
    meet_title: str,
):

    meet = (
        session.query(models.Meet)
        .filter(models.Meet.title == meet_title)
        .first()
    )
    if meet:
        send_mail(
            settings.GMAIL,
            to_gmail,
            settings.GMAIL_PASSWORD,
            meet_hour,
            time_until_meeting,
            first_name,
            last_name,
        )
        return True
    return False
