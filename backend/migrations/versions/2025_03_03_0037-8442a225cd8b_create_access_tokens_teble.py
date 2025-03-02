"""create access tokens teble

Revision ID: 8442a225cd8b
Revises: dc688c107e7c
Create Date: 2025-03-03 00:37:52.494323

"""

from typing import Sequence, Union

import fastapi_users_db_sqlalchemy
from alembic import op
import sqlalchemy as sa


revision: str = "8442a225cd8b"
down_revision: Union[str, None] = "dc688c107e7c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "access_tokens",
        sa.Column("token", sa.String(length=43), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            fastapi_users_db_sqlalchemy.generics.TIMESTAMPAware(timezone=True),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk_access_tokens_user_id_users"),
            ondelete="cascade",
        ),
        sa.PrimaryKeyConstraint("token", name=op.f("pk_access_tokens")),
    )
    op.create_index(
        op.f("ix_access_tokens_created_at"),
        "access_tokens",
        ["created_at"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_access_tokens_created_at"),
        table_name="access_tokens"
    )
    op.drop_table("access_tokens")
