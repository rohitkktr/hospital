from sqlalchemy.orm import Session
from models.admissions import Admission
from schemas.admissions import AdmissionCreate, AdmissionUpdate


def create_admission(db: Session, data: AdmissionCreate):
    obj = Admission(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_admission(db: Session, admission_id: int):
    return db.query(Admission).filter(Admission.id == admission_id).first()


def get_all_admissions(db: Session):
    return db.query(Admission).all()


def update_admission(db: Session, admission_id: int, data: AdmissionUpdate):
    obj = get_admission(db, admission_id)
    if not obj:
        return None
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_admission(db: Session, admission_id: int):
    obj = get_admission(db, admission_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return True