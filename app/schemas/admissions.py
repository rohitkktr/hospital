from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AdmissionCreate(BaseModel):
    patient_id: int
    bed_id: int
    admission_time: datetime
    reason: Optional[str]

class AdmissionUpdate(BaseModel):
    bed_id: Optional[int]
    reason: Optional[str]

class AdmissionResponse(BaseModel):
    id: int
    patient_id: int
    bed_id: int
    admission_time: datetime
    reason: Optional[str]
    is_active: bool

    class Config:
        orm_mode = True

class AdmissionDetailsResponse(BaseModel):
    id: int
    patient_id: int
    patient_name: Optional[str]
    bed_id: int
    bed_number: Optional[str]
    admission_time: datetime
    reason: Optional[str]
    is_active: bool

    class Config:
        orm_mode = True
