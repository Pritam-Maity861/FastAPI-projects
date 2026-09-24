import uuid
from datetime import datetime, timedelta, timezone

from pwdlib import PasswordHash
import jwt

from app.config.settings import settings


password_hasher=PasswordHash.recommended()

def hash_password(plain_password:str)->str:
    return password_hasher.hash(plain_password)

def verify_password(plain_password:str,hashed_password:str)->bool:
    return password_hasher.verify(password=plain_password,hash=hashed_password)


def create_access_token(user_id:uuid.UUID)->str:
    now = datetime.now(timezone.utc)
    expires_at = now + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": str(user_id),
        "iat":now,
        "exp":expires_at,
        # "aud":"access-Token"
    }

    return jwt.encode(payload,key=settings.secret_key,algorithm=settings.jwt_algorithm)


def decode_access_token(token:str)->dict:
    return jwt.decode(token,settings.secret_key,algorithms=[settings.jwt_algorithm])




