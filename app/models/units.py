from sqlalchemy import Column, Integer, String, BigInteger, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from utils.database import Base
import enum

# UNIT
class Unit(Base):
    __tablename__ = "unit"
    id = Column(BigInteger, primary_key=True, index=True)
    name = Column(String(100), nullable=False,unique=True)

    beds = relationship("Bed", back_populates="unit")
    users = relationship("User", back_populates="unit")
    admissions = relationship("Admission", back_populates="unit")
