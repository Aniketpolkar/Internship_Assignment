from pydantic import BaseModel
from datetime import datetime
from typing import List


class UserContext(BaseModel):
    email: str


class CalendarEvent(BaseModel):
    subject: str
    start: datetime
    end: datetime


class ScheduleSummary(BaseModel):
    email: str
    events: List[CalendarEvent]
