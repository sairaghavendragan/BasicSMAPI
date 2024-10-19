from sqlalchemy import create_engine
import psycopg

from psycopg.rows import dict_row

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def getdb():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


# try:
#     conn = psycopg.connect(
#         host="localhost",
#         dbname="fastapi",
#         user="postgres",
#         password="password",
#         port=5432,
#         row_factory=dict_row,
#     )

#     cur = conn.cursor()
#     print("connected")

# except Exception as error:
#     print(error)