from datetime import datetime, timedelta
from fastapi import FastAPI, Depends, Body, HTTPException, status, Header
from database import engine, SessionLocal
import models
from sqlalchemy.orm import Session
import utils
import schemas
from pydantic import BaseModel
from jose import jwt
from jose.exceptions import JWTError
from basic_auth import basic_auth_guard


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

class LicenseKeyRequestParam(BaseModel):
    license_key: str




class LicenseController:
    @staticmethod
    def create_license_data(trial: bool, recovery_key: str, db: Session) -> models.LicenseModel:
        license_type = models.LicenseTypeEnum.TRIAL if trial else models.LicenseTypeEnum.FULL
        license_key = utils.generate_random_sequence()
        key_expires_at = datetime.now() + TRIAL_PERIOD_DELTA if trial else None

        license_data = models.LicenseModel(
            license_key=license_key,
            license_type=license_type,
            key_expires_at=key_expires_at,
            recovery_key=recovery_key
        )

        db.add(license_data)
        db.commit()
        return license_data

    @staticmethod
    def verify_license_key(license_key: str, db: Session) -> dict:
        key_exist = db.query(models.LicenseModel).filter_by(license_key=license_key).first()
        if key_exist:
            exp = key_exist.key_expires_at
            session_id = utils.generate_random_sequence()
            key_exist.session_id = session_id
            db.commit()
            custom_data = {
                "session_id": session_id,
                "sub": license_key
            }
            if exp:
                custom_data["exp"] = exp.timestamp()

            token = jwt.encode(custom_data, SECRET_KEY, algorithm=ALGORITHM)
            return {"token": token}

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The license key provided is not valid. Please check and try again."
        )

    @staticmethod
    def verify_session(jwt_token: str, db: Session) -> str:
        try:
            decoded_token = jwt.decode(jwt_token, SECRET_KEY, algorithms=[ALGORITHM])
            license_key = decoded_token.get("sub")
            license_record = db.query(models.LicenseModel).filter_by(license_key=license_key).first()
        except JWTError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"JWT Error, {str(e)}"
            )

        if license_record:
            server_session_id = license_record.session_id
            client_session_id = decoded_token.get("session_id")
            if server_session_id == client_session_id:
                return "OK"
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Session id")

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid License key")

license_controller = LicenseController()

@app.post("/generate/license_key", response_model=schemas.LicenseKeySchema)
async def create_license_key(trial: bool = False, recovery_key: str = None, db: Session = Depends(get_db), auth=Depends(basic_auth_guard)):
    return license_controller.create_license_data(trial, recovery_key, db)

@app.post("/verify/key")
async def verify_license(request_body: LicenseKeyRequestParam, db: Session = Depends(get_db), auth=Depends(basic_auth_guard)):
    return license_controller.verify_license_key(request_body.license_key, db)

@app.get("/verify/session")
async def verify_session(x_jwt_token: str = Header(...), db: Session = Depends(get_db), auth=Depends(basic_auth_guard)):
    
    return license_controller.verify_session(x_jwt_token, db)