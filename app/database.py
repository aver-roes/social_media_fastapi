# NOTE: this file handles the connection to the database and creates sessions

from sqlalchemy import create_engine, engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# postgresql://username:password@localhost/database_name
SQLALCHEMY_DATEBASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


# connect to the datebase
engine = create_engine(SQLALCHEMY_DATEBASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# create a base class for the database
Base = declarative_base()


# Dependency:create a session to connect to the database then close it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
