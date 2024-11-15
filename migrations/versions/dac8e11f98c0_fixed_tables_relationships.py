"""fixed tables relationships

Revision ID: dac8e11f98c0
Revises: 3aaac178e5f9
Create Date: 2024-08-20 23:09:44.266278

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'dac8e11f98c0'
down_revision: Union[str, None] = '3aaac178e5f9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('videos', sa.Column('user', sa.Integer(), nullable=False))
    op.drop_constraint('videos_user_id_fkey', 'videos', type_='foreignkey')
    op.create_foreign_key(None, 'videos', 'users', ['user'], ['id'])
    op.drop_column('videos', 'user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('videos', sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'videos', type_='foreignkey')
    op.create_foreign_key('videos_user_id_fkey', 'videos', 'users', ['user_id'], ['id'])
    op.drop_column('videos', 'user')
    # ### end Alembic commands ###
