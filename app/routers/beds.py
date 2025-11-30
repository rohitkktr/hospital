from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models
from app.utils.database import get_db
from app.schemas.beds import BedCreate, BedUpdate, BedResponse, BedDetailsResponse

router = APIRouter(prefix="/beds", tags=["Beds"])



# -------------------- CREATE BED --------------------
@router.post("/", response_model=BedResponse)
def create_bed(bed: BedCreate, db: Session = Depends(get_db)):
    unit = db.query(models.Unit).filter(models.Unit.id == bed.unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")

    new_bed = models.Bed(
        unit_id=bed.unit_id,
        label=bed.label,
        is_active=True
    )
    db.add(new_bed)
    db.commit()
    db.refresh(new_bed)
    return new_bed


# # -------------------- GET ALL BEDS --------------------
@router.get("")
def get_all_beds(db: Session = Depends(get_db)):
    beds = db.query(models.Bed).filter(models.Bed.is_active == True).all()
    return beds

def get_beds():
    return {"msg": "beds working"}

# -------------------- GET BED BY ID --------------------
@router.get("/{bed_id}", response_model=BedDetailsResponse)
def get_bed(bed_id: int, db: Session = Depends(get_db)):
    bed = db.query(models.Bed).filter(models.Bed.id == bed_id).first()
    if not bed:
        raise HTTPException(status_code=404, detail="Bed not found")

    return bed


# -------------------- UPDATE BED --------------------
@router.put("/{bed_id}", response_model=BedResponse)
def update_bed(bed_id: int, bed_data: BedUpdate, db: Session = Depends(get_db)):
    bed = db.query(models.Bed).filter(models.Bed.id == bed_id).first()
    if not bed:
        raise HTTPException(status_code=404, detail="Bed not found")

    if bed_data.bed_number is not None:
        bed.bed_number = bed_data.bed_number
    if bed_data.unit_id is not None:
        bed.unit_id = bed_data.unit_id

    db.commit()
    db.refresh(bed)
    return bed


# -------------------- SOFT DELETE BED --------------------
@router.delete("/{bed_id}")
def delete_bed(bed_id: int, db: Session = Depends(get_db)):
    bed = db.query(models.Bed).filter(models.Bed.id == bed_id).first()
    if not bed:
        raise HTTPException(status_code=404, detail="Bed not found")

    bed.is_active = False
    db.commit()
    return {"message": f"Bed {bed_id} deactivated"}
