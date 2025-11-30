from sqlalchemy import Column, Integer, String, BigInteger, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.utils.database import Base
import enum

# RESTRAINT
class Restraint(Base):
    __tablename__ = "restraint"
    restraint_id = Column(BigInteger, primary_key=True, index=True)
    patient_id = Column(BigInteger, ForeignKey("patient.patient_id"))
    Treatment_type = Column(String(100), nullable=False)
    Start_time = Column(DateTime)
    End_time = Column(DateTime, nullable=True)

    patient = relationship("Patient", back_populates="restraints")
    admissions = relationship("Admission", back_populates="restraint")

## ENUM for Treatment Type