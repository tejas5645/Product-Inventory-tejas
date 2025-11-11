from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db_url="postgresql://postgres:admin@localhost:5432/practice"
engine = create_engine(db_url)
session = sessionmaker(autoflush=False,autocommit=False,bind=engine)