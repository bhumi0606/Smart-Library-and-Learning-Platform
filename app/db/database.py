from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
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