from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models
from app.utils.database import get_db
from app.schemas.restraints import RestraintCreate, RestraintUpdate, RestraintResponse

router = APIRouter(prefix="/restraints", tags=["Restraints"])


# -------------------- CREATE RESTRAINT --------------------
@router.post("/", response_model=RestraintResponse)
def create_restraint(data: RestraintCreate, db: Session = Depends(get_db)):
    new_obj = models.Restraint(**data.dict())
    db.add(new_obj)
    db.commit()
    db.refresh(new_obj)
    return new_obj


# -------------------- GET ALL RESTRAINTS --------------------
@router.get("/", response_model=List[RestraintResponse])
def get_restraints(db: Session = Depends(get_db)):
    return db.query(models.Restraint).all()


# -------------------- GET RESTRAINT BY ID --------------------
@router.get("/{restraint_id}", response_model=RestraintResponse)
def get_restraint(restraint_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Restraint).filter(models.Restraint.id == restraint_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Restraint not found")
    return obj


# -------------------- UPDATE RESTRAINT --------------------
@router.put("/{restraint_id}", response_model=RestraintResponse)
def update_restraint(restraint_id: int, data: RestraintUpdate, db: Session = Depends(get_db)):
    obj = db.query(models.Restraint).filter(models.Restraint.id == restraint_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Restraint not found")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


# -------------------- DELETE RESTRAINT --------------------
@router.delete("/{restraint_id}")
def delete_restraint(restraint_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.Restraint).filter(models.Restraint.id == restraint_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Restraint not found")

    db.delete(obj)
    db.commit()
    return {"message": f"Restraint {restraint_id} deleted"}
