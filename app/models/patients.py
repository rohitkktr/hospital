from sqlalchemy import Column, Integer, String, BigInteger, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.utils.database import Base
import enum

# PATIENT
class Patient(Base):
    __tablename__ = "patient"
    patient_id = Column(BigInteger, primary_key=True, index=True)
    fName = Column(String(100), nullable=True)
    lName = Column(String(100), nullable=True)
    Gender = Column(String(10), nullable=True)
    Address1 = Column(String(200), nullable=True)
    Address2 = Column(String(200), nullable=True)
    Address3 = Column(String(200), nullable=True)
    Email = Column(String(100), nullable=True)
    Emergencey_Contact1 = Column(String(100), nullable=True)
    Emergencey_Contact2 = Column(String(100), nullable=True)
    Emergencey_family_member_name = Column(String(100), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)

    admissions = relationship("Admission", back_populates="patient")
    restraints = relationship("Restraint", back_populates="patient")
