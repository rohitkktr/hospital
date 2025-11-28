from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    JR = "JR"
    SR = "SR"
    Faculty = "Faculty"
    Nurse = "Nurse"

# UNIT
class UnitCreate(BaseModel):
    name: str

class UnitResponse(BaseModel):
    id: int
    name: str
    class Config:
        from_attributes = True

# BED
class BedCreate(BaseModel):
    unit_id: int
    label: str
    is_active: Optional[bool] = True

class BedResponse(BaseModel):
    id: int
    unit_id: int
    label: str
    is_active: bool
    class Config:
        from_attributes = True

# PATIENT
class PatientCreate(BaseModel):
    anonymized_id: str
    fName: Optional[str] = None
    lName: Optional[str] = None
    Gender: Optional[str] = None
    Address1: Optional[str] = None
    Address2: Optional[str] = None
    Address3: Optional[str] = None
    Email: Optional[str] = None
    Emergencey_Contact1: Optional[str] = None
    Emergencey_Contact2: Optional[str] = None
    Emergencey_family_member_name: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None

class PatientResponse(BaseModel):
    patient_id: int
    anonymized_id: str
    fName: Optional[str]
    lName: Optional[str]
    Gender: Optional[str] = None
    Address1: Optional[str] = None
    Address2: Optional[str] = None
    Address3: Optional[str] = None
    Email: Optional[str] = None
    Emergencey_Contact1: Optional[str] = None
    Emergencey_Contact2: Optional[str] = None
    Emergencey_family_member_name: Optional[str] = None
    city: Optional[str]
    state: Optional[str]
    class Config:
        from_attributes = True

# RESTRAINT
class RestraintCreate(BaseModel):
    patient_id: int
    Treatment_type: str
    Start_time: datetime
    End_time: Optional[datetime] = None

class RestraintResponse(BaseModel):
    restraint_id: int
    patient_id: int
    Treatment_type: str
    Start_time: datetime
    End_time: Optional[datetime] = None
    class Config:
        from_attributes = True

# ADMISSION
class AdmissionCreate(BaseModel):
    patient_id: int
    unit_id: int
    bed_id: int
    restraint_id: Optional[int] = None
    admitted_at: datetime
    discharged_at: Optional[datetime] = None

class AdmissionResponse(BaseModel):
    id: int
    patient_id: int
    unit_id: int
    bed_id: int
    restraint_id: Optional[int] = None
    admitted_at: datetime
    discharged_at: Optional[datetime]
    class Config:
        from_attributes = True

# USER
class UserCreate(BaseModel):
    name: str
    phone: Optional[str] = None
    email: EmailStr
    role: UserRole
    unit_id: Optional[int] = None
    is_active: Optional[bool] = True

class UserResponse(BaseModel):
    id: int
    name: str
    phone: Optional[str]
    email: EmailStr
    role: UserRole
    unit_id: Optional[int]
    is_active: bool
    class Config:
        from_attributes = True
