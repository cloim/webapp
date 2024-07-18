from fastapi import APIRouter, HTTPException, Request, status, Depends
from sqlalchemy.orm import Session

from models.user import UserORM
from common.db import get_db
from common.auth import create_access_token, get_current_user, verify_password, expires_timedelta, pwd_context


router = APIRouter()


@router.get("/me")
async def me(current_user: UserORM = Depends(get_current_user)):
    return current_user


@router.post("/signup")
async def signup(request: Request, db: Session = Depends(get_db)):
    params = await request.json()
    db_user = db.query(UserORM).filter(UserORM.uid == params["uid"]).first()
    if db_user:
        raise HTTPException(status_code=409, detail="이미 존재하는 ID 입니다")

    hashed_pw = pwd_context.hash(params["upw"])
    new_user = UserORM(
        uid=params["uid"], uname=params["uname"], upw=hashed_pw, status=params["status"])
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    access_token = create_access_token(
        {"uid": new_user.uid, "uname": new_user.uname}, expires_delta=expires_timedelta)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/signin")
async def signin(request: Request, db: Session = Depends(get_db)):
    params = await request.json()
    db_user = db.query(UserORM).filter(
        UserORM.status == "N",
        UserORM.uid == params["uid"]
    ).first()

    if not db_user or not verify_password(params["upw"], db_user.upw):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="로그인 정보가 올바르지 않습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        {"uid": db_user.uid, "uname": db_user.uname}, expires_delta=expires_timedelta)
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
