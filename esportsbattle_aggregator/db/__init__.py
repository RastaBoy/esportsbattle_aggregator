from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from .models import Base, MetaData
from .services.meta import MetaService

from .. import config

CONNECTION_STRING = f"postgresql+asyncpg://{config.POSTGRES_USERNAME}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_HOST}:{config.POSTGRES_PORT}/{config.POSTGRES_DB_NAME}"


class DataBaseController:
    _engine = create_async_engine(CONNECTION_STRING, echo=False)
    _session = async_sessionmaker(bind=_engine)

    
    @staticmethod
    async def __get_version__(session : AsyncSession) -> int:
        meta_service = MetaService(session)
        meta = await meta_service.get_by_id(0)
        if meta is None:
            await meta_service.create(MetaData(version=0))
            return 0

        return meta.version


    @staticmethod
    async def create_database():
        async with DataBaseController._engine.begin() as conn:
            # await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)


    @staticmethod
    @asynccontextmanager
    async def get_session() -> AsyncSession:
            async with DataBaseController._session.begin() as session:
                yield session    
                


from .models import *