from sqlalchemy.orm import Session
from app.models.restraints import Restraint
from app.schemas.restraints import RestraintCreate, RestraintUpdate


def create_restraint(db: Session, data: RestraintCreate):
    obj = Restraint(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_restraint(db: Session, restraint_id: int):
    return db.query(Restraint).filter(Restraint.id == restraint_id).first()


def get_all_restraints(db: Session):
    return db.query(Restraint).all()


def update_restraint(db: Session, restraint_id: int, data: RestraintUpdate):
    obj = get_restraint(db, restraint_id)
    if not obj:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(obj, field, value)
    db.commit()
    db.refresh(obj)
    return obj


def delete_restraint(db: Session, restraint_id: int):
    obj = get_restraint(db, restraint_id)
    if not obj:
        return None
    db.delete(obj)
    db.commit()
    return True