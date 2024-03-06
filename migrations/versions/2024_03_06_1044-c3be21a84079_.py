"""empty message

Revision ID: c3be21a84079
Revises: 855e99375759
Create Date: 2024-03-06 10:44:43.224676

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c3be21a84079'
down_revision: Union[str, None] = '855e99375759'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
