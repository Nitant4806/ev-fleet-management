"""convert status fields to enums

Revision ID: 09ea02581086
Revises: 6886dcf81fea
Create Date: 2026-06-12 15:07:51.384881

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "09ea02581086"
down_revision: Union[str, Sequence[str], None] = "6886dcf81fea"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:

    chargingsessionstatus = sa.Enum(
        "scheduled",
        "charging",
        "completed",
        "cancelled",
        name="chargingsessionstatus",
    )

    tripstatus = sa.Enum(
        "pending",
        "in_progress",
        "completed",
        "cancelled",
        name="tripstatus",
    )

    vehiclestatus = sa.Enum(
        "available",
        "dispatched",
        "on_trip",
        "returned",
        "needs_charging",
        "charging",
        "maintenance",
        "offline",
        name="vehiclestatus",
    )

    bind = op.get_bind()

    chargingsessionstatus.create(bind, checkfirst=True)
    tripstatus.create(bind, checkfirst=True)
    vehiclestatus.create(bind, checkfirst=True)

    op.execute("""
        ALTER TABLE charging_sessions
        ALTER COLUMN status
        TYPE chargingsessionstatus
        USING status::chargingsessionstatus
    """)

    op.execute("""
        ALTER TABLE trips
        ALTER COLUMN status
        TYPE tripstatus
        USING status::tripstatus
    """)

    op.execute("""
        ALTER TABLE vehicles
        ALTER COLUMN status
        TYPE vehiclestatus
        USING status::vehiclestatus
    """)


def downgrade() -> None:

    op.alter_column(
        "vehicles",
        "status",
        type_=sa.String(),
    )

    op.alter_column(
        "trips",
        "status",
        type_=sa.String(),
    )

    op.alter_column(
        "charging_sessions",
        "status",
        type_=sa.String(),
    )

    bind = op.get_bind()

    sa.Enum(name="vehiclestatus").drop(bind, checkfirst=True)

    sa.Enum(name="tripstatus").drop(bind, checkfirst=True)

    sa.Enum(name="chargingsessionstatus").drop(bind, checkfirst=True)
