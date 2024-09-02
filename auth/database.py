from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
import os
from .schema import Users

DATABASE_URL = "sqlite+aiosqlite:///user-data.db"
async_engine = AsyncEngine(create_engine(DATABASE_URL, echo=bool(os.getenv('SHOW_SQLALCHEMY_LOGS', False))))


async def create_tables():
    """
    Method to create all the necessary
    tables in the database
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    """
    Method to create a Database
    Session
    """
    # create a AsyncSession instance
    async_session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    # start a session
    async with async_session() as session:
        async with session.begin():
            yield session
