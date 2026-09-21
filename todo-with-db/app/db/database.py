from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker,create_async_engine
from sqlalchemy.orm import DeclarativeBase
from app.config.settings import settings


engine=create_async_engine(url=settings.database_url)

AsyncSessionLocal=async_sessionmaker(
    bind=engine,
    autoflush=False,
    class_=AsyncSession,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    """Base class every SQLAlchemy model will inherit from."""
    pass


async def create_tables():
     from app.models import Todo 

     async with engine.begin() as connection:
          await connection.run_sync(Base.metadata.create_all)


async def get_db():
    async with AsyncSessionLocal() as session:
            yield session
