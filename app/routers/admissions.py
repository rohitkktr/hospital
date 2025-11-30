from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import models
from app.utils.database import get_db
from app.schemas.admissions import (
    AdmissionCreate,
    AdmissionUpdate,
    AdmissionResponse,
    AdmissionDetailsResponse
)

router = APIRouter(prefix="/admissions", tags=["Admissions"])


# -------------------- CREATE ADMISSION --------------------
@router.post("/", response_model=AdmissionResponse)
def create_admission(data: AdmissionCreate, db: Session = Depends(get_db)):

    # Check patient
    patient = db.query(models.Patient).filter(models.Patient.patient_id == data.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Check bed
    bed = db.query(models.Bed).filter(models.Bed.id == data.bed_id).first()
    if not bed:
        raise HTTPException(status_code=404, detail="Bed not found")

    if not bed.is_active:
        raise HTTPException(status_code=400, detail="Bed is inactive or unavailable")

    # Create admission record
    new_admission = models.Admission(
        patient_id=data.patient_id,
        bed_id=data.bed_id,
        admission_time=data.admission_time,
        reason=data.reason,
        is_active=True
    )

    db.add(new_admission)
    db.commit()
    db.refresh(new_admission)

    return new_admission


# -------------------- GET ALL ADMISSIONS --------------------
@router.get("/", response_model=List[AdmissionResponse])
def get_all_admissions(db: Session = Depends(get_db)):
    admissions = db.query(models.Admission).filter(models.Admission.is_active == True).all()
    return admissions


# -------------------- GET ADMISSION BY ID --------------------
@router.get("/{admission_id}", response_model=AdmissionDetailsResponse)
def get_admission(admission_id: int, db: Session = Depends(get_db)):
    admission = db.query(models.Admission).filter(models.Admission.id == admission_id).first()

    if not admission:
        raise HTTPException(status_code=404, detail="Admission not found")

    patient = db.query(models.Patient).filter(models.Patient.patient_id == admission.patient_id).first()
    bed = db.query(models.Bed).filter(models.Bed.bed_id== admission.bed_id).first()

    return {
        "id": admission.id,
        "patient_id": admission.patient_id,
        "patient_name": f"{patient.fName} {patient.lName}" if patient else None,
        "bed_id": admission.bed_id,
        "bed_number": bed.bed_number if bed else None,
        "admission_time": admission.admission_time,
        "reason": admission.reason,
        "is_active": admission.is_active
    }


# -------------------- UPDATE ADMISSION --------------------
@router.put("/{admission_id}", response_model=AdmissionResponse)
def update_admission(admission_id: int, data: AdmissionUpdate, db: Session = Depends(get_db)):
    admission = db.query(models.Admission).filter(models.Admission.id == admission_id).first()

    if not admission:
        raise HTTPException(status_code=404, detail="Admission not found")

    if data.reason is not None:
        admission.reason = data.reason

    if data.bed_id is not None:
        bed = db.query(models.Bed).filter(models.Bed.id == data.bed_id).first()
        if not bed:
            raise HTTPException(status_code=404, detail="New bed not found")
        admission.bed_id = data.bed_id

    db.commit()
    db.refresh(admission)

    return admission


# -------------------- DISCHARGE (SOFT DELETE) --------------------
@router.delete("/{admission_id}")
def discharge_admission(admission_id: int, db: Session = Depends(get_db)):
    admission = db.query(models.Admission).filter(models.Admission.id == admission_id).first()

    if not admission:
        raise HTTPException(status_code=404, detail="Admission not found")

    admission.is_active = False
    db.commit()

    return {"message": f"Admission {admission_id} discharged"}