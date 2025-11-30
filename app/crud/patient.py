from sqlalchemy.orm import Session
from app.models.patients import Patient
from app.schemas.patients import PatientCreate, PatientUpdate


def create_patient(db: Session, data: PatientCreate):
    obj = Patient(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_patient(db: Session, patient_id: int):
    return db.query(Patient).filter(Patient.id == patient_id).first()


def get_all_patients(db: Session):
    return db.query(Patient).all()


def update_patient(db: Session, patient_id: int, data: PatientUpdate):
    obj = get_patient(db, patient_id)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_patient(db: Session, patient_id: int):
    obj = get_patient(db, patient_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return True