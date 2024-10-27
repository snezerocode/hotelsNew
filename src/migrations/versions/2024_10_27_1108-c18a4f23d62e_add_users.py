"""add users

Revision ID: c18a4f23d62e
Revises: 1c0810aa557c
Create Date: 2024-10-27 11:08:46.346283

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "c18a4f23d62e"
down_revision: Union[str, None] = "1c0810aa557c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
