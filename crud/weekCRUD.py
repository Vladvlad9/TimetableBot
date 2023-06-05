from sqlalchemy import select, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import WeekInDBSchema, WeekSchema
from models import Week, create_async_session


class CRUDWeek(object):

    @staticmethod
    @create_async_session
    async def add(week: WeekSchema, session: AsyncSession = None) -> WeekInDBSchema | None:
        weeks = Week(**week.dict())
        session.add(weeks)
        try:
            await session.commit()
        except IntegrityError as eq:
            print(eq)
        else:
            await session.refresh(weeks)
            return WeekInDBSchema(**weeks.__dict__)

    @staticmethod
    @create_async_session
    async def get(user_id: int, session: AsyncSession = None) -> WeekInDBSchema | None:
        week = await session.execute(
            select(Week)
            .where(Week.user_id == user_id)
        )
        if weeks := week.first():
            return WeekInDBSchema(**weeks[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_all(session: AsyncSession = None) -> list[WeekInDBSchema]:
        weeks = await session.execute(
            select(Week)
        )
        return [WeekInDBSchema(**week[0].__dict__) for week in weeks]

    @staticmethod
    @create_async_session
    async def update(user_week: WeekInDBSchema, session: AsyncSession = None) -> None:
        try:
            await session.execute(
                update(Week)
                .where(Week.id == user_week.id)
                .values(**user_week.dict())
            )
            await session.commit()
        except IntegrityError as eq:
            print(eq)

    @staticmethod
    @create_async_session
    async def delete(user_id: int = None, session: AsyncSession = None) -> None:
        if user_id:
            await session.execute(
                delete(Week).where(Week.user_id == user_id)
            )
        else:
            await session.execute(
                delete(Week)
            )
        await session.commit()
