from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import os
from dotenv import load_dotenv

load_dotenv()

# Get Database URL from environment or use a default compatible with your local setup
db_url = os.getenv("DATABASE_URL")

if not db_url:
    # Fallback to sqlite for local dev if no postgres URL is found (optional, but good for beginners)
    # Or just raise a clear error
    raise ValueError("DATABASE_URL environment variable is not set. Please set it in your .env file or deployment settings.")

# Fix for some cloud providers (Heroku/Render) that use 'postgres://' which is deprecated in SQLAlchemy
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

engine = create_engine(db_url)
session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()  