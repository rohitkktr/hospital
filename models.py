from sqlalchemy import Column, Integer, String, BigInteger, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
import enum

# User roles
class UserRole(str, enum.Enum):
    JR = "JR"
    SR = "SR"
    Faculty = "Faculty"
    Nurse = "Nurse"

# UNIT
class Unit(Base):
    __tablename__ = "unit"
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False)

    beds = relationship("Bed", back_populates="unit")
    users = relationship("User", back_populates="unit")
    admissions = relationship("Admission", back_populates="unit")

# BED
class Bed(Base):
    __tablename__ = "bed"
    id = Column(BigInteger, primary_key=True, index=True)
    unit_id = Column(BigInteger, ForeignKey("unit.id"))
    label = Column(String(50), nullable=False, unique=True)
    is_active = Column(Boolean, default=True)

    unit = relationship("Unit", back_populates="beds")
    admissions = relationship("Admission", back_populates="bed")

# PATIENT
class Patient(Base):
    __tablename__ = "patient"
    patient_id = Column(BigInteger, primary_key=True, index=True)
    anonymized_id = Column(String(50), nullable=False, unique=True)
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

# USER
class User(Base):
    __tablename__ = "user"
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(100), unique=True)
    role = Column(Enum(UserRole), nullable=False)
    unit_id = Column(BigInteger, ForeignKey("unit.id"), nullable=True)
    is_active = Column(Boolean, default=True)

    unit = relationship("Unit", back_populates="users")
