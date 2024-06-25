from fastapi import APIRouter, HTTPException, status, Body, Depends
from sqlalchemy.orm import Session

from models.user import UserORM, UserDTO
from common.db import get_db
from common.auth import create_access_token, get_current_user, verify_password, expires_timedelta, pwd_context


router = APIRouter()


@router.get("/me")
async def me(current_user: UserORM = Depends(get_current_user)):
    return current_user


@router.post("/signup")
async def signup(user: UserDTO = Body(..., media_type="application/json"), db: Session = Depends(get_db)):
    db_user = db.query(UserORM).filter(UserORM.uid == user.uid).first()
    if db_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 ID 입니다")
    
    hashed_pw = pwd_context.hash(user.upw)
    new_user = UserORM(uid=user.uid, uname=user.uname, upw=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token({ "uid": new_user.uid, "uname": new_user.uname }, expires_delta=expires_timedelta)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/signin")
async def signin(user: UserDTO = Body(..., media_type="application/json"), db: Session = Depends(get_db)):
    db_user = db.query(UserORM).filter(UserORM.uid == user.uid).first()

    if not db_user or not verify_password(user.upw, db_user.upw):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인 정보가 올바르지 않습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token({ "uid": db_user.uid, "uname": db_user.uname }, expires_delta=expires_timedelta)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


