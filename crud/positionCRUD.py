from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update, delete
from schemas import PositionInDBSchema, PositionSchema
from models import Position, create_async_session


class CRUDPosition(object):

    @staticmethod
    @create_async_session
    async def add(position: PositionSchema, session: AsyncSession = None) -> PositionInDBSchema | None:
        position = Position(**position.dict())
        session.add(position)
        try:
            await session.commit()
        except IntegrityError:
            pass
        else:
            await session.refresh(position)
            return PositionInDBSchema(**position.__dict__)

    @staticmethod
    @create_async_session
    async def delete(position_id: int, parent_id: int = None, session: AsyncSession = None) -> None:
        if parent_id:
            await session.execute(
                delete(Position)
                .where(Position.parent_id == parent_id)
            )
            await session.commit()
        await session.execute(
            delete(Position)
            .where(Position.id == position_id)
        )
        await session.commit()

    @staticmethod
    @create_async_session
    async def get(position_id: int, session: AsyncSession = None) -> PositionInDBSchema | None:
        position = await session.execute(
            select(Position)
            .where(Position.id == position_id)
        )
        if position := position.first():
            return PositionInDBSchema(**position[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_all(session: AsyncSession = None) -> list[PositionInDBSchema]:
        positions = await session.execute(
            select(Position)
        )
        return [PositionInDBSchema(**position[0].__dict__) for position in positions]

    @staticmethod
    @create_async_session
    async def update(position: PositionInDBSchema,
                     session: AsyncSession = None) -> None:
        await session.execute(
            update(Position)
            .where(Position.id == position.id)
            .values(**position.dict())
        )
        await session.commit()
