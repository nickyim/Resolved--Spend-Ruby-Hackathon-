"""Add created_at timestamp to User model

Revision ID: 4c255426c432
Revises: 34abbda346fb
Create Date: 2024-08-18 04:40:10.970241

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4c255426c432'
down_revision: Union[str, None] = '34abbda346fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('created_at', sa.DateTime(), server_default=sa.func.now(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'created_at')
    # ### end Alembic commands ###
