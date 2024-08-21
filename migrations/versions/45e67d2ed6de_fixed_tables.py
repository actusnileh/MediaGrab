"""fixed tables

Revision ID: 45e67d2ed6de
Revises: ffdbeb4eb8e0
Create Date: 2024-08-19 17:12:01.279378

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "45e67d2ed6de"
down_revision: Union[str, None] = "ffdbeb4eb8e0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("videos", sa.Column("user_id", sa.Integer(), nullable=False))
    op.create_foreign_key(None, "videos", "users", ["user_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "videos", type_="foreignkey")
    op.drop_column("videos", "user_id")
    # ### end Alembic commands ###
