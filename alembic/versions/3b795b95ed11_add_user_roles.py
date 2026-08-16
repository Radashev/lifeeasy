"""add user roles

Revision ID: 3b795b95ed11
Revises: ab2182ed00f4
Create Date: 2026-07-28 22:27:13.964563

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3b795b95ed11"
down_revision: str | Sequence[str] | None = "ab2182ed00f4"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    user_role = sa.Enum(
        "root",
        "admin",
        "user",
        name="user_role",
    )

    user_role.create(
        op.get_bind(),
        checkfirst=True,
    )

    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role,
            nullable=False,
            server_default="user",
        ),
    )

    op.alter_column(
        "users",
        "role",
        server_default=None,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "users",
        "role",
    )

    user_role = sa.Enum(
        "root",
        "admin",
        "user",
        name="user_role",
    )

    user_role.drop(
        op.get_bind(),
        checkfirst=True,
    )
