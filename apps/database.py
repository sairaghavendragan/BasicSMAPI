from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker
 
from .config import settings

class Base(DeclarativeBase):
    pass

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

 


def getdb():
    
    with SessionLocal() as db:
        yield db

    '''try:
        yield db
    finally:
        db.close()'''


 