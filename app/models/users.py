from sqlalchemy import Column, Integer, String, BigInteger, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from  utils.database import Base
import enum
from .roles import UserRole

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
