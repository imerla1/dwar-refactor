from database import Base
from sqlalchemy import Column, Integer, String, DateTime, func, LargeBinary


class TokenModel(Base):
    __tablename__ = 'tokens'
    id = Column(Integer, primary_key=True, index=True)
    token = Column(LargeBinary, nullable=False, index=True)
    created_at = Column(DateTime, nullable=False, default=func.now())

