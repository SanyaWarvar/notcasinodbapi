"""add use count

Revision ID: d2c081318cf0
Revises: d62a7fe2c68f
Create Date: 2024-03-06 14:30:00.694081

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd2c081318cf0'
down_revision: Union[str, None] = 'd62a7fe2c68f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('tokens', sa.Column('use_num', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('tokens', 'use_num')
    # ### end Alembic commands ###
