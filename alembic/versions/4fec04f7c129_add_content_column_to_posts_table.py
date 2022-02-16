"""add content column to posts table

Revision ID: 4fec04f7c129
Revises: 12d9f622c191
Create Date: 2022-02-14 22:09:00.242598

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4fec04f7c129'
down_revision = '12d9f622c191'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
