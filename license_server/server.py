from datetime import datetime, timedelta
from fastapi import FastAPI, Depends
from database import engine, SessionLocal
import models
from sqlalchemy.orm import Session
from models import LicenseModel, LicenseTypeEnum
import utils
import schemas

# create all models
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DWAR License Server",
    version="0.1.0"
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SECRET_KEY = "09d25e094faa6ca2556c8181f2039f23jgvwedsklvsdmv6cf63b88e8d3e7"
ALGORITHM = "HS256"
# Trial License Period 1 day
TRIAL_PERIOD_DELTA = timedelta(days=1)

@app.post("/{trial}", response_model=schemas.LicenseKeySchema)
async def create_license_key(trial: bool = False, recovery_key: str = None,  db: Session = Depends(get_db)):
    license_type = LicenseTypeEnum.TRIAL if trial else LicenseTypeEnum.FULL
    license_key = utils.generate_random_sequence()
    key_expires_at = None
    if trial:
        key_expires_at = datetime.now() + TRIAL_PERIOD_DELTA
    license_data = LicenseModel(
        license_key=license_key,
        license_type=license_type,
        key_expires_at=key_expires_at,
        recovery_key = recovery_key
    )
    db.add(license_data)
    db.commit()
    
    return license_data
