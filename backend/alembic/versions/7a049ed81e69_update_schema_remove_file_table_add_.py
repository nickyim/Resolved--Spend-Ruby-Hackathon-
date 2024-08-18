"""Update schema: remove File table, add fileType to Entry

Revision ID: 7a049ed81e69
Revises: 01c654cab405
Create Date: 2024-08-17 21:54:58.447057

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7a049ed81e69'
down_revision: Union[str, None] = '01c654cab405'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Conditionally drop the 'file' table if it exists
    op.execute("DROP TABLE IF EXISTS file")

    # Create 'entry' table if it doesn't exist
    op.create_table('entry',
        sa.Column('id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('entryId', sa.String, unique=True, nullable=False),
        sa.Column('isComplaint', sa.Boolean, nullable=False),
        sa.Column('product', sa.String),
        sa.Column('subProduct', sa.String),
        sa.Column('entryText', sa.Text, nullable=False),
        sa.Column('summary', sa.String),
        sa.Column('userId', sa.Integer, sa.ForeignKey('user.id'), nullable=False),
    )
    
    # Add the 'fileType' column with a default value to prevent NotNullViolation
    filetype_enum = sa.Enum('TEXT', 'IMAGE', 'VIDEO', 'AUDIO', 'JSON', name='filetype')
    filetype_enum.create(op.get_bind(), checkfirst=True)

    op.add_column('entry', sa.Column('fileType', filetype_enum, nullable=False, server_default='TEXT'))

    # Remove the server_default to match the final schema
    op.alter_column('entry', 'fileType', server_default=None)


def downgrade() -> None:
    # Drop the 'fileType' column and ENUM type
    op.drop_column('entry', 'fileType')
    filetype_enum = sa.Enum('TEXT', 'IMAGE', 'VIDEO', 'AUDIO', 'JSON', name='filetype')
    filetype_enum.drop(op.get_bind(), checkfirst=True)

    # Recreate the 'file' table as it was before
    op.create_table('file',
        sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column('url', sa.VARCHAR(), nullable=False),
        sa.Column('type', postgresql.ENUM('TEXT', 'IMAGE', 'VIDEO', 'AUDIO', 'JSON', name='filetype'), nullable=False),
        sa.Column('entryId', sa.INTEGER(), nullable=False),
        sa.Column('userId', sa.INTEGER(), nullable=False),
        sa.ForeignKeyConstraint(['entryId'], ['entry.id'], name='file_entryId_fkey'),
        sa.ForeignKeyConstraint(['userId'], ['user.id'], name='file_userId_fkey'),
        sa.PrimaryKeyConstraint('id', name='file_pkey')
    )
