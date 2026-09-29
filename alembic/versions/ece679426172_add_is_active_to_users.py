"""add is_active to users

Revision ID: ece679426172
Revises: 1851ca14b7bd
Create Date: 2026-09-28 17:18:52.752518

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ece679426172'
down_revision: Union[str, Sequence[str], None] = '1851ca14b7bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'users',
        sa.Column(
            'is_active',
            sa.Boolean(),
            nullable=False,
            server_default=sa.true(),
        ),
    )

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('users', 'is_active')