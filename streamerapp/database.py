from sqlalchemy.ext.asyncio import create_async_engine,AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from . import models
from core.config import get_settings

settings = get_settings()



async_engine = create_async_engine(settings.SQLALCHEMY_URL_DATABASE,pool_pre_ping=True,pool_recycle=300,pool_size=5,max_overflow=0)


AsyncSessionLocal = async_sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)


class Base(DeclarativeBase):
    pass

async def get_async_db():
    db =  AsyncSessionLocal()
    try:
        yield db
    finally:
        await db.close()
      