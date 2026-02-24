from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

import os 
from dotenv import load_dotenv 

load_dotenv()


engine = create_engine(f"postgresql+psycopg://{os.getenv('DB_URI')}", echo=False) 

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, bind=engine)

def get_db():
    
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()    