from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    """
    Base repository.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, instance):
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance):
        await self.session.delete(instance)

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def execute(self, statement):
        return await self.session.execute(statement)

    async def scalar(self, statement):
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def scalars(self, statement):
        result = await self.session.execute(statement)
        return result.scalars().all()
