"""add the rest of column for posts table

Revision ID: d1d70d5a438a
Revises: adad158670ec
Create Date: 2022-02-14 22:50:26.062631

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd1d70d5a438a'
down_revision = 'adad158670ec'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean, nullable=False, server_default='TRUE'),

                  op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                                   server_default=sa.text('now()'), nullable=False)))
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
