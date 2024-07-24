from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from common.config_loader import conf
from common.logger import d


engine = create_engine(
    conf("dburl"), 
    echo=False, 
    pool_size=10, # 동시에 유지할 수 있는 최대 연결 수
    max_overflow=20, # pool_size 초과 시 추가로 생성할 수 있는 연결 수
    pool_timeout=30, # pool 에서 연결을 얻기 위해 대기할 최대 시간(초)
    pool_recycle=1800, # 지정된 시간(초) 후에 연결이 자동으로 재생성
    pool_pre_ping=True
)
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()


def init_db(reset: bool = False):
    d(f"Initializing database, reset={reset}")
    if reset:
        Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    
    try:
        yield db
    except Exception as e:
        if db.is_active:
            db.rollback()
    finally:
        try:
            db.close()
        except Exception as e:
            d(e)

