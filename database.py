from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()

db_url = os.getenv("DATABASE_URL") 
engine = create_engine(db_url)
session = sessionmaker(autocommit = False, autoflush=False, bind = engine)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()  