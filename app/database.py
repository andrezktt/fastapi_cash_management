from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

DATABASE_URL = config(search_path='DATABASE_URL')

engine = create_engine(DATABASE_URL)
local_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()

def get_database():
    database = local_session()
    try:
        yield database
    finally:
        database.close()