"""Объединение веток миграций

Revision ID: ccac7c51bdc3
Revises: ba79550454a3, d7c1fae4df98
Create Date: 2025-09-18 16:10:45.444293

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ccac7c51bdc3'
down_revision: Union[str, Sequence[str], None] = ('ba79550454a3', 'd7c1fae4df98')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
