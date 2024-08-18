"""Add is_verified column to User table

Revision ID: f45564d813b7
Revises: 
Create Date: 2024-08-10 12:35:27.511122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'f45564d813b7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

new_column = sa.Column('is_verified', sa.Boolean(), nullable=True)


def upgrade():
    conn = op.get_bind()
    inspector = sa.inspect(conn)

    if 'users' in inspector.get_table_names():
        columns = [col['name'] for col in inspector.get_columns('users')]

        if 'is_verified' not in columns:
            op.add_column('users', new_column)


def downgrade() -> None:
    op.drop_column('users', 'is_verified')
