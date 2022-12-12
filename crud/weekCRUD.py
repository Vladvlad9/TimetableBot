from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import WeekInDBSchema
from models import Week, create_async_session


class CRUDRole(object):

    @staticmethod
    @create_async_session
    async def get(week_id: int, session: AsyncSession = None) -> WeekInDBSchema | None:
        week = await session.execute(
            select(Week)
            .where(Week.id == week_id)
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
