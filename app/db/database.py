from sqlalchemy.async import create_async_engine
from sqlalchmemy.orm import async_sessionmaker, declarative_base
from app.config import DATABASE_URL
 
engine = create_async_engine(DATABASE_URL)
Session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
 
 
def get_db():
    db = Session()
    try:
        yield db
    finally:
        db.close()