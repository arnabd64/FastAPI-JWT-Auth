import asyncio

import sqlmodel
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession

from .schema import SQLModel, Users

async_engine = AsyncEngine(sqlmodel.create_engine('sqlite+aiosqlite:///users.db', echo=True))

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



async def add_user(user: Users):
    Session = sessionmaker(
        bind=async_engine,
        class_=AsyncSession
    )
    async with Session() as session:
        async with session.begin() as transaction:
            try:
                session.add(user)
                await session.commit()
                print("successfully added user")

            except Exception as e:
                session.rollback()
                print("Failed to add User")


if __name__ == "__main__":
    import asyncio

    asyncio.run(create_tables())
    # asyncio.run(add_user(Users(username=f"arnabdhar.{schema.uid_generator()}", password=schema.uid_generator())))




