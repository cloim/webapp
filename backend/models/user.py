from typing import Optional
from sqlalchemy import Column, String
from pydantic import BaseModel, Field, ConfigDict
from common.db import Base


class UserORM(Base):
    __tablename__ = "user"
    __table_args__ = {"comment": "사용자"}

    uid = Column(String(20), primary_key=True, index=True, comment="사용자 ID")
    uname = Column(String(20), nullable=False, comment="사용자 이름")
    upw = Column(String(100), nullable=False, comment="비밀번호")

    
class UserDTO(BaseModel):
    uid: Optional[str] = Field(default=None)
    uname: Optional[str] = Field(default=None)
    upw: Optional[str] = Field(default=None)

    model_config = ConfigDict(from_attributes=True)
