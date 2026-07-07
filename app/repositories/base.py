from __future__ import annotations

from typing import Any, Generic, TypeVar

from sqlalchemy import Select, select
from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")


class BaseRepository(Generic[ModelType]):
    """
    Base repository for all repositories.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, instance: ModelType) -> ModelType:
        self.session.add(instance)
        await self.session.flush()
        await self.session.refresh(instance)
        return instance

    async def delete(self, instance: ModelType) -> None:
        await self.session.delete(instance)

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def execute(self, statement: Select[Any]):
        return await self.session.execute(statement)

    async def scalar(self, statement: Select[Any]):
        result = await self.session.execute(statement)
        return result.scalar_one_or_none()

    async def scalars(self, statement: Select[Any]):
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def exists(
        self,
        model,
        **filters,
    ) -> bool:

        stmt = select(model).filter_by(**filters)

        result = await self.scalar(stmt)

        return result is not None
