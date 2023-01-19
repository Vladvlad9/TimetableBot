"""create admin table

Revision ID: 5cf33e95cc77
Revises: 9a06bf646e68
Create Date: 2023-01-19 13:32:42.528810

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5cf33e95cc77'
down_revision = '9a06bf646e68'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('admins',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.BigInteger(), nullable=False),
                    sa.Column('lname', sa.Text(), nullable=False),
                    sa.Column('fname', sa.Text(), nullable=False),
                    sa.Column('mname', sa.Text(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('admins')
