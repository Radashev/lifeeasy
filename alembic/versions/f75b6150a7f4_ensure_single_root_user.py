"""ensure single root user

Revision ID: f75b6150a7f4
Revises: 3b795b95ed11
Create Date: 2026-07-30 16:21:10.440856

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "f75b6150a7f4"
down_revision: str | Sequence[str] | None = "3b795b95ed11"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_index(
        "uq_users_single_root",
        "users",
        ["role"],
        unique=True,
        postgresql_where=sa.text("role = 'root'"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(
        "uq_users_single_root",
        table_name="users",
    )
