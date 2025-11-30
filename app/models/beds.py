from sqlalchemy import Column, Integer, String, BigInteger, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.utils.database import Base
import enum

# BED
class Bed(Base):
    __tablename__ = "bed"
    id = Column(BigInteger, primary_key=True, index=True)
    unit_id = Column(BigInteger, ForeignKey("unit.id"))
    label = Column(String(50), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)
    start_time = Column(DateTime, nullable=True)  # from restraint, optional

    unit = relationship("Unit", back_populates="beds")
    admissions = relationship("Admission", back_populates="bed")
