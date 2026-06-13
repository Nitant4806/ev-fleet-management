"""add vehicle charging station relation

Revision ID: f856b63431e1
Revises: 6717a6497abc
Create Date: 2026-06-13 17:43:26.840665

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "f856b63431e1"
down_revision: Union[str, Sequence[str], None] = "6717a6497abc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column(
        "vehicles",
        sa.Column(
            "charging_station_id",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.create_foreign_key(
        "fk_vehicle_station",
        "vehicles",
        "charging_stations",
        ["charging_station_id"],
        ["id"],
    )


def downgrade():

    op.drop_constraint(
        "fk_vehicle_station",
        "vehicles",
        type_="foreignkey",
    )

    op.drop_column(
        "vehicles",
        "charging_station_id",
    )
