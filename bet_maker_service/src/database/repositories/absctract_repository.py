from abc import ABC
from typing import Generic, Sequence, Type, TypeVar

from sqlalchemy import Executable
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.database.models.base import Base

_MODEL_TYPE = TypeVar("_MODEL_TYPE", bound=Base)
_QUERY = TypeVar("_QUERY", bound=Executable)


class AbstractRepository(ABC, Generic[_MODEL_TYPE]):
    _model: Type[_MODEL_TYPE] | None = None

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_all(self) -> Sequence[_MODEL_TYPE]:
        query = select(self._model)
        result = await self._session.execute(query)
        return result.scalars().all()

    async def create(self, **kwargs) -> _MODEL_TYPE:
        entity = self._model(**kwargs)
        self._session.add(entity)
        await self._session.commit()
        return entity
