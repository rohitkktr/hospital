from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from pydantic import BaseModel
from database import SessionLocal, engine, Base

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Hospital Management API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------- UNIT --------------------
@app.post("/units", response_model=schemas.UnitResponse)
def create_unit(unit: schemas.UnitCreate, db: Session = Depends(get_db)):
    new_unit = models.Unit(**unit.model_dump())
    db.add(new_unit)
    db.commit()
    db.refresh(new_unit)
    return new_unit

@app.get("/units", response_model=List[schemas.UnitResponse])
def get_units(db: Session = Depends(get_db)):
    return db.query(models.Unit).all()

@app.delete("/units/{unit_id}")
def delete_unit(unit_id: int, db: Session = Depends(get_db)):
    unit = db.query(models.Unit).filter(models.Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Unit not found")
    db.delete(unit)
    db.commit()
    return {"message": f"Unit {unit_id} deleted successfully"}

# -------------------- BED --------------------
@app.post("/beds", response_model=schemas.BedResponse)
def create_bed(bed: schemas.BedCreate, db: Session = Depends(get_db)):
    unit = db.query(models.Unit).filter(models.Unit.id == bed.unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail=f"Unit {bed.unit_id} not found")
    new_bed = models.Bed(**bed.model_dump())
    db.add(new_bed)
    db.commit()
    db.refresh(new_bed)
    return new_bed

@app.get("/beds", response_model=List[schemas.BedResponse])
def get_beds(db: Session = Depends(get_db)):
    return db.query(models.Bed).filter(models.Bed.is_active==True).all()

class BedDeleteRequest(BaseModel):
    label: str
@app.delete("/beds/delete-by-label")
def delete_bed_by_label(request: BedDeleteRequest, db: Session = Depends(get_db)):
    bed = db.query(models.Bed).filter(models.Bed.label == request.label).first()
    if not bed:
        raise HTTPException(status_code=404, detail="Bed not found")
    
    bed.is_active = False  # soft delete
    db.commit()
    return {"message": f"Bed with label '{request.label}' deactivated successfully."}

# -------------------- PATIENT --------------------
@app.post("/patients", response_model=schemas.PatientResponse)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    new_patient = models.Patient(**patient.model_dump())
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient

@app.get("/patients", response_model=List[schemas.PatientResponse])
def get_patients(db: Session = Depends(get_db)):
    return db.query(models.Patient).all()

class PatientDeleteRequest(BaseModel):
    anonymized_id: str 
@app.delete("/patients/delete-by-id")
def delete_patient_by_label(request: PatientDeleteRequest, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.anonymized_id == request.anonymized_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    db.delete(patient)
    db.commit()
    return {"message": f"Patient with anonymized_id '{request.anonymized_id}' deleted successfully."}

# -------------------- USER --------------------
@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if user.unit_id:
        unit = db.query(models.Unit).filter(models.Unit.id == user.unit_id).first()
        if not unit:
            raise HTTPException(status_code=404, detail=f"Unit {user.unit_id} not found")
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users", response_model=List[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).filter(models.User.is_active==True).all()

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.is_active = False
    db.commit()
    return {"message": f"User {user_id} deactivated"}

# -------------------- RESTRAINT --------------------
@app.post("/restraints", response_model=schemas.RestraintResponse)
def create_restraint(restraint: schemas.RestraintCreate, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.patient_id == restraint.patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail=f"Patient {restraint.patient_id} not found")
    new_restraint = models.Restraint(**restraint.model_dump())
    db.add(new_restraint)
    db.commit()
    db.refresh(new_restraint)
    return new_restraint

@app.get("/restraints", response_model=List[schemas.RestraintResponse])
def get_restraints(db: Session = Depends(get_db)):
    return db.query(models.Restraint).all()

@app.delete("/restraints/{restraint_id}")
def delete_restraint(restraint_id: int, db: Session = Depends(get_db)):
    restraint = db.query(models.Restraint).filter(models.Restraint.restraint_id == restraint_id).first()
    if not restraint:
        raise HTTPException(status_code=404, detail="Restraint not found")
    db.delete(restraint)
    db.commit()
    return {"message": f"Restraint {restraint_id} deleted"}

# -------------------- ADMISSION --------------------
@app.post("/admissions", response_model=schemas.AdmissionResponse)
def create_admission(admission: schemas.AdmissionCreate, db: Session = Depends(get_db)):
    patient = db.query(models.Patient).filter(models.Patient.patient_id == admission.patient_id).first()
    unit = db.query(models.Unit).filter(models.Unit.id == admission.unit_id).first()
    bed = db.query(models.Bed).filter(models.Bed.id == admission.bed_id).first()
    if admission.restraint_id:
        restraint = db.query(models.Restraint).filter(models.Restraint.restraint_id == admission.restraint_id).first()
        if not restraint:
            raise HTTPException(status_code=404, detail=f"Restraint {admission.restraint_id} not found")
    if not patient or not unit or not bed:
        raise HTTPException(status_code=404, detail="Patient, Unit, or Bed not found")
    new_adm = models.Admission(**admission.model_dump())
    db.add(new_adm)
    db.commit()
    db.refresh(new_adm)
    return new_adm

@app.get("/admissions", response_model=List[schemas.AdmissionResponse])
def get_admissions(db: Session = Depends(get_db)):
    return db.query(models.Admission).all()

@app.delete("/admissions/{admission_id}")
def delete_admission(admission_id: int, db: Session = Depends(get_db)):
    admission = db.query(models.Admission).filter(models.Admission.id == admission_id).first()
    if not admission:
        raise HTTPException(status_code=404, detail="Admission not found")
    db.delete(admission)
    db.commit()
    return {"message": f"Admission {admission_id} deleted"}
