"""create account table

Revision ID: 7e971f7bcd8d
Revises: 
Create Date: 2022-12-12 18:15:41.152793

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e971f7bcd8d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('positions',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.VARCHAR(length=24), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )

    op.create_table('users',
                    sa.Column('id', sa.BigInteger(), nullable=False),
                    sa.Column('lname', sa.Text(), nullable=False),
                    sa.Column('fname', sa.Text(), nullable=False),
                    sa.Column('mname', sa.Text(), nullable=False),
                    sa.Column('positions_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['positions_id'], ['users.id'], ondelete='NO ACTION'),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )

    op.create_table('weeks',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.BigInteger(), nullable=False),

                    sa.Column('Monday', sa.Text(), default=None),
                    sa.Column('Tuesday', sa.Text(), default=None),
                    sa.Column('Wednesday', sa.Text(), default=None),
                    sa.Column('Thursday', sa.Text(), default=None),
                    sa.Column('Friday', sa.Text(), default=None),
                    sa.Column('Saturday', sa.Text(), default=None),
                    sa.Column('Sunday', sa.Text(), default=None),

                    sa.ForeignKeyConstraint(['user_id'], ['weeks.id'], ondelete='NO ACTION'),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('positions')
    op.drop_table('users')
    op.drop_table('weeks')
