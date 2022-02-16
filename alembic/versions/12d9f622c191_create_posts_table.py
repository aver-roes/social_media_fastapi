"""create posts table

Revision ID: 12d9f622c191
Revises: 
Create Date: 2022-02-14 21:56:01.035565

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '12d9f622c191'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.INTEGER(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
