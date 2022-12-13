"""create tablesq

Revision ID: 9a06bf646e68
Revises: 42b50a5131d5
Create Date: 2022-12-13 13:03:24.094036

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a06bf646e68'
down_revision = '42b50a5131d5'
branch_labels = None
depends_on = None


def upgrade() -> None:

    op.create_table('positions',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.VARCHAR(length=24), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )

    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.BigInteger(), nullable=False),
                    sa.Column('lname', sa.Text(), nullable=False),
                    sa.Column('fname', sa.Text(), nullable=False),
                    sa.Column('mname', sa.Text(), nullable=False),
                    sa.Column('nickname', sa.Text(), nullable=False),
                    sa.Column('positions_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['positions_id'], ['positions.id'], ondelete='NO ACTION'),
                    sa.PrimaryKeyConstraint('id')
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
                    sa.Column('description', sa.Text(), default=None),
                    sa.Column('handle', sa.Boolean(), default=False),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='NO ACTION'),
                    sa.PrimaryKeyConstraint('id')
                    )




def downgrade() -> None:
    op.drop_table('positions')
    op.drop_table('users')
    op.drop_table('weeks')
