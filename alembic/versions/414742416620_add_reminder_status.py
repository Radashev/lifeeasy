"""add reminder status

Revision ID: 414742416620
Revises: 91a1d0a2ec7d
Create Date: 2026-08-23 10:08:18.731620

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "414742416620"
down_revision: Union[str, Sequence[str], None] = "91a1d0a2ec7d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    reminder_status = sa.Enum(
        "pending",
        "sent",
        "cancelled",
        name="reminder_status",
    )

    reminder_status.create(
        op.get_bind(),
        checkfirst=True,
    )
    op.add_column(
        "reminders",
        sa.Column(
            "status",
            reminder_status,
            server_default="pending",
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column(
        "reminders",
        "status",
    )

    reminder_status = sa.Enum(
        "pending",
        "sent",
        "cancelled",
        name="reminder_status",
    )

    reminder_status.drop(
        op.get_bind(),
        checkfirst=True,
    )
