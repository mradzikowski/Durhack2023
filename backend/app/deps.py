from app.db.session import async_session
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError


async def get_db():
    """
    Dependency for the asynchronous database to yield the session
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except SQLAlchemyError as sql_ex:
            await session.rollback()
            raise sql_ex
        except HTTPException as http_ex:
            await session.rollback()
            raise http_ex
        finally:
            await session.close()
