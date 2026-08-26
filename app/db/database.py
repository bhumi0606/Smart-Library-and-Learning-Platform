from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from app.core.config import DATABASE_URL
 
engine = create_async_engine(DATABASE_URL)
Session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False,)
Base = declarative_base()
 
 
async def get_db():
    db = Session()
    try:
        yield db
    finally:
        await db.close()