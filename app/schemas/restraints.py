from pydantic import BaseModel
from datetime import datetime


class RestraintBase(BaseModel):
    bed_id: int
    start_time: datetime | None = None
    end_time: datetime | None = None
    reason: str | None = None


class RestraintCreate(RestraintBase):
    pass


class RestraintUpdate(BaseModel):
    start_time: datetime | None = None
    end_time: datetime | None = None
    reason: str | None = None


class RestraintResponse(RestraintBase):
    id: int


class Config:
    orm_mode = True