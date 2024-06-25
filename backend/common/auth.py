from datetime import datetime, timezone, timedelta
from typing import Optional
from fastapi import HTTPException, status, Depends, Header
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext

from models.user import UserORM
from common.config_loader import conf
from common.db import get_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/signin")
hash_algorithm = conf("hash_algorithm")
expires_timedelta = timedelta(minutes=60 * 24)
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    uid = get_uid_from_token(token)
    user = db.query(UserORM).filter(UserORM.uid == uid).first()
    if user is None:
        raise credentials_exception
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, conf("salt"), algorithm=hash_algorithm)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_uid_from_token(token: str):
    try:
        payload = jwt.decode(token, conf("salt"), algorithms=[hash_algorithm])
        uid: str = payload.get("uid")
        if uid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return uid


async def verify_authorization(authorization: str = Header(...)):
    if not authorization:
        raise HTTPException(status_code=401, detail="No Authorization header")
    token = authorization.split(" ")[-1]
    return get_uid_from_token(token)
    