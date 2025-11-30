from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# -------------------- BASE --------------------
class BedBase(BaseModel):
    label: str
    unit_id: int
    is_active: Optional[bool] = True
    

    
# -------------------- CREATE --------------------
class BedCreate(BedBase):
    pass

# -------------------- UPDATE --------------------
class BedUpdate(BaseModel):
    bed_number: Optional[str]
    unit_id: Optional[int]

# -------------------- RESPONSE --------------------
class BedResponse(BedBase):
    id: int

    class Config:
        orm_mode = True

# -------------------- DETAILS (WITH restraint start_time) --------------------
class BedDetailsResponse(BedResponse):
    class Config:
        orm_mode = True

# Note: start_time is included in BedDetailsResponse to show the latest restraint start time for the bed.
# It is optional and will be None if there are no restraints associated with the bed.
# This field is populated in the router when fetching bed details.