from sqlalchemy.orm import Session
from app.models.beds import Bed
from app.schemas.beds import BedCreate


def create_bed(db: Session, bed_in: BedCreate):
    bed = Bed(bed_number=bed_in.bed_number, is_available=bed_in.is_available, unit_id=bed_in.unit_id, start_time=bed_in.start_time)
    db.add(bed)
    db.commit()
    db.refresh(bed)
    return bed


def get_bed(db: Session, bed_id: int):
    return db.query(Bed).filter(Bed.id == bed_id).first()