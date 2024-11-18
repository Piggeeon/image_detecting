"""init

Revision ID: 16ee34f54530
Revises: 
Create Date: 2024-11-18 22:17:13.442084

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '16ee34f54530'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('faces',
    sa.Column('uid', sa.UUID(), nullable=False),
    sa.Column('image_name', sa.String(), nullable=False),
    sa.Column('bbox', sa.String(), nullable=False),
    sa.Column('gender', sa.String(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['image_name'], ['images.name'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('uid')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('faces')
    # ### end Alembic commands ###