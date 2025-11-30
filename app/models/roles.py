from sqlalchemy import Column, Integer, String, BigInteger, Boolean, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.utils.database import Base
import enum

# User roles
class UserRole(str, enum.Enum):
    JR = "JR"
    SR = "SR"
    Faculty = "Faculty"
    Nurse = "Nurse"