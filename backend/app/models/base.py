import uuid
from typing import Any

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    """
    Declarative base for orm
    """

    id: Any
    __name__: str
    # Generate __tablename__ automatically

    @declared_attr
    def __tablename__(cls) -> str:
        """
        Method to change the tablename to lower

        :return:
        """
        return cls.__name__.lower()

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    async def save(self, db_session: AsyncSession):
        """
        Add the object to the database and save

        :param db_session: asynchronous database session
        :return:
        """
        try:
            db_session.add(self)
            return await db_session.commit()
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(ex),
            )

    async def delete(self, db_session: AsyncSession):
        """
        Delete the object from the database

        :param db_session: asynchronous database session
        :return:
        """
        try:
            await db_session.delete(self)
            await db_session.commit()
            return True
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(ex),
            )

    async def update(self, db_session: AsyncSession, **kwargs):
        """
        Update the object in the database

        :param db_session: asynchronous database session
        :param kwargs: additional arguments to update the object
        :return:
        """
        for k, v in kwargs.items():
            if v is not None:
                setattr(self, k, v)
        try:
            db_session.add(self)
            await db_session.commit()
            return self
        except SQLAlchemyError as ex:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=repr(ex),
            )

    @classmethod
    async def find_by_id(cls, db_session: AsyncSession, id: uuid.UUID):
        """
        Find the object by id without select in load

        :param id: identifier of the object
        :param db_session: asynchronous database session
        :return:
        """
        stmt = select(cls).where(cls.id == id)
        result = await db_session.execute(stmt)
        instance = result.scalars().first()
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There is no record for {cls.__name__} for requested id value : {id}",
            )
        return instance

    @classmethod
    async def find_all(cls, db_session: AsyncSession):
        """
        Find all objects without selecting other in load

        :param db_session: asynchronous database session
        :return:
        """
        stmt = select(cls)
        result = await db_session.execute(stmt)
        instance = result.scalars().all()
        if not instance:
            return []
        return list(instance)
