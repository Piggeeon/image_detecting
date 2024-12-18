"""recreate type

Revision ID: b9d142561bcb
Revises: 16ee34f54530
Create Date: 2024-11-18 22:25:20.379725

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'b9d142561bcb'
down_revision: Union[str, None] = '16ee34f54530'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('faces', 'bbox',
               existing_type=sa.VARCHAR(),
               type_=postgresql.JSONB(astext_type=sa.Text()),
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('faces', 'bbox',
               existing_type=postgresql.JSONB(astext_type=sa.Text()),
               type_=sa.VARCHAR(),
               existing_nullable=False)
    # ### end Alembic commands ###
