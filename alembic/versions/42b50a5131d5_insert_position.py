"""insert position

Revision ID: 42b50a5131d5
Revises: 47f8a842f929
Create Date: 2022-12-12 21:11:15.522204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy.exc import IntegrityError

from models import create_sync_session, Position
from models.engine import Session

revision = '42b50a5131d5'
down_revision = '47f8a842f929'
branch_labels = None
depends_on = None


# roles = [
#     'ЧБОБО',
#     'Тренер',
#     'Менеджер Джуниор',
#     'Менеджер',
#     'Заместитель Директора',
#     'Диретор'
# ]


@create_sync_session
def upgrade(session: Session = None) -> None:
    pass
    # for role in roles:
    #     role = Position(name=role)
    #     session.add(role)
    #     try:
    #         session.commit()
    #     except IntegrityError:
    #         pass


@create_sync_session
def downgrade(session: Session = None) -> None:
    pass
    # for role in roles:
    #     session.execute(
    #         sa.delete(Position)
    #         .where(Position.name == role)
    #     )
    #     session.commit()
