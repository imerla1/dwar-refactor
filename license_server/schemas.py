from pydantic import BaseModel
from models import LicenseTypeEnum
from datetime import datetime
from typing import Optional

class LicenseKeySchema(BaseModel):
    license_key: str 
    license_type: LicenseTypeEnum
    key_expires_at: Optional[datetime] = None
    session_id: Optional[str] = None
    recovery_key: Optional[str] = None

    class Config:
        orm_mode = True