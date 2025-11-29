from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
from utils.database import get_db
from schemas.units import UnitCreate, UnitUpdate, UnitResponse

router = APIRouter(prefix="/units", tags=["Units"])


# -------------------- CREATE UNIT --------------------
@router.post("/", response_model=UnitResponse)
def create_unit(data: UnitCreate, db: Session = Depends(get_db)):
    new_unit = models.Unit(**data.dict())
    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)
    return new_unit


# -------------------- GET ALL UNITS --------------------
@router.get("/", response_model=List[UnitResponse])
def get_all_units(db: Session = Depends(get_db)):
    return db.query(models.Unit).all()


# -------------------- GET UNIT BY ID --------------------
@router.get("/{unit_id}", response_model=UnitResponse)
def get_unit(unit_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Unit).filter(models.Unit.id == unit_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Unit not found")
    return obj


# -------------------- UPDATE UNIT --------------------
@router.put("/{unit_id}", response_model=UnitResponse)
def update_unit(unit_id: int, data: UnitUpdate, db: Session = Depends(get_db)):
    obj = db.query(models.Unit).filter(models.Unit.id == unit_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Unit not found")

    for k, v in data.dict(exclude_unset=True).items():
        setattr(obj, k, v)

    db.commit()
    db.refresh(obj)
    return obj


# -------------------- DELETE UNIT --------------------
@router.delete("/{unit_id}")
def delete_unit(unit_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Unit).filter(models.Unit.id == unit_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Unit not found")

    db.delete(obj)
    db.commit()
    return {"message": f"Unit {unit_id} deleted"}
