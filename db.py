__author__ = "AivanF"

from os import environ
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Index, Column, Integer, String, JSON
from sqlalchemy.future import select

DATABASE_URL = environ.get("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
engine = create_async_engine(DATABASE_URL, future=True, echo=True)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base = declarative_base()


async def delete_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def create_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


class Model(Base):
    __tablename__ = "smth"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    data = Column(JSON, nullable=False)

    idx_main = Index("name", "id")


async def create_object(db: Session, name: str, data: dict):
    connection = Model(name=name, data=data)
    db.add(connection)
    await db.flush()


async def get_objects(db: Session, name: str):
    raw_q = select(Model) \
        .where(Model.name == name) \
        .order_by(Model.id)
    q = await db.execute(raw_q)
    return q.scalars().all()
