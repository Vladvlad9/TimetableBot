"""insert position

Revision ID: 4d43d8549ba2
Revises: 7e971f7bcd8d
Create Date: 2022-12-12 18:32:22.080775

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError


# revision identifiers, used by Alembic.
from models import create_sync_session, Position

revision = '4d43d8549ba2'
down_revision = '7e971f7bcd8d'
branch_labels = None
depends_on = None

roles = [
    'ЧБОБО',
    'Тренер',
    'Менеджер Джуниор',
    'Менеджер',
    'Заместитель Директора',
    'Диретор'
]


@create_sync_session
def upgrade(session: Session = None) -> None:
    for role in roles:
        role = Position(name=role)
        session.add(role)
        try:
            session.commit()
        except IntegrityError:
            pass


@create_sync_session
def downgrade(session: Session = None) -> None:
    for role in roles:
        session.execute(
            sa.delete(Position)
            .where(Position.name == role)
        )
        session.commit()
