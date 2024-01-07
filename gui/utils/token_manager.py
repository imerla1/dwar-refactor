from sqlalchemy.orm import Session
from models.token_model import TokenModel
from globals import secure_crypto
from jose import jwt
from datetime import datetime


def fetch_jwt_token(db: Session):
    token = db.query(TokenModel).first()
    decrypted_token = None

    if token:
        decrypted_token = secure_crypto.decrypt(token.token)

        try:
            # Decode the token without verifying the signature
            payload = jwt.decode(
                decrypted_token,
                options={"verify_signature": False},
                key={},
            )

            # Check if the 'exp' claim exists and if the token is not expired
            if 'exp' in payload:
                expiration_time = payload['exp']
                current_time = datetime.utcnow().timestamp()

                if current_time < expiration_time:

                    return decrypted_token
                else:
                    return False

        except jwt.JWTError as e:
            print(f"Error decoding token: {e}")
            return False

    return decrypted_token




