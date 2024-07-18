from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from common.config_loader import conf
from common.logger import d, ex


engine = create_engine(conf("dburl"), echo=False, pool_size=10,
                       max_overflow=20, pool_timeout=30, pool_recycle=1800, pool_pre_ping=True)
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
        ex(e)
        if db.is_active:
            db.rollback()
    finally:
        db.close()
