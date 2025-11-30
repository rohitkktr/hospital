from pydantic import BaseModel
from typing import Optional

class PatientCreate(BaseModel):
    patient_id: Optional[int]= None
    fName: str
    lName: Optional[str]= None
    Gender: Optional[str]
    Address1: Optional[str]
    Address2: Optional[str]= None
    Address3: Optional[str]= None
    Email: Optional[str]= None
    Emergencey_Contact1: Optional[str]
    Emergencey_Contact2: Optional[str]= None
    Emergencey_family_member_name: Optional[str]
    city: Optional[str]
    state: Optional[str]

class PatientUpdate(BaseModel):
    fName: Optional[str]
    lName: Optional[str]
    Gender: Optional[str]
    Address1: Optional[str]
    Address2: Optional[str]
    Address3: Optional[str]
    Email: Optional[str]
    Emergencey_Contact1: Optional[str]
    Emergencey_Contact2: Optional[str]
    city: Optional[str]
    state: Optional[str]    


class PatientResponse(BaseModel):
    patient_id: int
    fName: str
    lName: Optional[str]
    Gender: Optional[str]
    Address1: Optional[str]
    Address2: Optional[str]
    Address3: Optional[str]
    Email: Optional[str]
    Emergencey_Contact1: Optional[str]
    Emergencey_Contact2: Optional[str]
    Emergencey_family_member_name: Optional[str]
    city: Optional[str]
    state: Optional[str]

    class Config:
        orm_mode = True
