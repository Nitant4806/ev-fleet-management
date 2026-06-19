"""add vehicle target soc

Revision ID: a41a9406ce17
Revises: f856b63431e1
Create Date: 2026-06-14 16:51:30.897955

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "a41a9406ce17"
down_revision: Union[str, Sequence[str], None] = "f856b63431e1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():

    op.add_column(
        "vehicles",
        sa.Column(
            "target_soc",
            sa.Float(),
            nullable=True,
        ),
    )


def downgrade():

    op.drop_column(
        "vehicles",
        "target_soc",
    )
