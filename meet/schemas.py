from datetime import date, time
from typing import List, Optional, Union

from pydantic import BaseModel


class MeetingUsersBase(BaseModel):
    user_id: int

    class Config:
        orm_mode = True


class MeetBase(BaseModel):
    title: str


class MeetCreate(MeetBase):
    date: date
    hour: int
    minute: Optional[int] = 0
    users_add: List[Union[int, str]] = []

    @property
    def get_time(self):
        return time(self.hour, self.minute)


class MeetUpdate(MeetCreate):
    update_date: Optional[bool] = False
    update_time: Optional[bool] = False
    new_title: Optional[str] = None
    users_delete: List[Union[int, str]] = []


class Meet(MeetBase):
    id: int
    owner_id: int
    users: List[MeetingUsersBase] = []

    class Config:
        orm_mode = True
