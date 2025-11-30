from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models
from app.utils.database import get_db
from app.schemas.patients import PatientCreate, PatientUpdate, PatientResponse

router = APIRouter(prefix="/patients", tags=["Patients"])


# -------------------- CREATE PATIENT --------------------
@router.post("/", response_model=PatientResponse)
def create_patient(data: PatientCreate, db: Session = Depends(get_db)):
    new_patient = models.Patient(**data.model_dump())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient


# -------------------- GET ALL PATIENTS --------------------
@router.get("", response_model=List[PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    p= db.query(models.Patient).all()
    return p


# -------------------- GET PATIENT BY ID --------------------
@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


# -------------------- UPDATE PATIENT --------------------
@router.put("/{patient_id}", response_model=PatientResponse)
def update_patient(patient_id: int, data: PatientUpdate, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(patient, key, value)

    db.commit()
    db.refresh(patient)
    return patient


# -------------------- DELETE PATIENT --------------------
@router.delete("/{patient_id}")
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    db.delete(patient)
    db.commit()
    return {"message": f"Patient {patient_id} removed"}
