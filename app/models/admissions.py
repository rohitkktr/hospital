
from sqlalchemy import Column, Integer, String, BigInteger, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.utils.database import Base
import enum

# ADMISSION
class Admission(Base):
    __tablename__ = "admission"
    id = Column(BigInteger, primary_key=True, index=True)
    patient_id = Column(BigInteger, ForeignKey("patient.patient_id"))
    unit_id = Column(BigInteger, ForeignKey("unit.id"))
    bed_id = Column(BigInteger, ForeignKey("bed.id"))
    restraint_id = Column(BigInteger, ForeignKey("restraint.restraint_id"), nullable=True)
    admitted_at = Column(DateTime)
    discharged_at = Column(DateTime, nullable=True)

    patient = relationship("Patient", back_populates="admissions")
    unit = relationship("Unit", back_populates="admissions")
    bed = relationship("Bed", back_populates="admissions")
    restraint = relationship("Restraint", back_populates="admissions", uselist=False)
