from database import Base
from enum import Enum
from sqlalchemy import Column, Integer, String, DateTime, Enum as SQLAlchemyEnum
from sqlalchemy.sql import func


class LicenseTypeEnum(Enum):
    FULL = 'full'
    TRIAL = 'trial'


class LicenseModel(Base):
    __tablename__ = "licenses"
    id = Column(Integer, primary_key=True, index=True)
    license_key = Column(String, unique=True, nullable=False, index=True)
    license_type = Column(SQLAlchemyEnum(LicenseTypeEnum), nullable=False)
    key_expires_at = Column(DateTime, nullable=True)
    session_id = Column(String, unique=True, nullable=True)
    recovery_key = Column(String, unique=False, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
