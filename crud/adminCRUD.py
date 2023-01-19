from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import AdminInDBSchema
from models import Admin, create_async_session


class CRUDAdmin(object):

    @staticmethod
    @create_async_session
    async def get(admin_id: int, session: AsyncSession = None) -> AdminInDBSchema | None:
        admins = await session.execute(
            select(Admin)
            .where(Admin.user_id == admin_id)
        )
        if admin := admins.first():
            return AdminInDBSchema(**admin[0].__dict__)

    @staticmethod
    @create_async_session
    async def get_all(session: AsyncSession = None) -> list[AdminInDBSchema]:
        admins = await session.execute(
            select(Admin)
        )
        return [AdminInDBSchema(**admin[0].__dict__) for admin in admins]
