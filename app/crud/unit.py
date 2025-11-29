from sqlalchemy.orm import Session
from app.models.units import Unit
from app.schemas.units import UnitCreate


def create_unit(db: Session, unit_in: UnitCreate):
    unit = Unit(name=unit_in.name, floor=unit_in.floor)
    db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit


def get_unit(db: Session, unit_id: int):
    return db.query(Unit).filter(Unit.id == unit_id).first()