import os

from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from .schema import Users

# dialetc+driver://user:pass@hostname:port/dbname
DATABASE_URL = "mysql+asyncmy://auth-user:auth-user-password@mysql:3306/authentication"
ECHO = bool(os.getenv('SHOW_SQLALCHEMY_LOGS', False))
ASYNC_ENGINE = AsyncEngine(create_engine(DATABASE_URL, echo=ECHO))

        
async def create_tables():
    """
    Method to create all the necessary
    tables in the database
    """
    async with ASYNC_ENGINE.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session():
    """
    Method to create a Database
    Session
    """
    # create a AsyncSession instance
    async_session = sessionmaker(
        bind=ASYNC_ENGINE,
        class_=AsyncSession,
        expire_on_commit=False
    )

    # start a session
    async with async_session() as session:
        async with session.begin():
            yield session
