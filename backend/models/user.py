from sqlalchemy import Column, String
from common.db import Base


class UserORM(Base):
    __tablename__ = "user"
    __table_args__ = {"comment": "사용자"}

    uid = Column(String(20), primary_key=True, index=True, comment="사용자 ID")
    uname = Column(String(20), nullable=False, comment="사용자 이름")
    upw = Column(String(100), nullable=False, comment="비밀번호")
    status = Column(String(1), nullable=False, comment="계정 상태 (N: 정상, D: 삭제)")