"""add user table

Revision ID: 862ab353389d
Revises: 4fec04f7c129
Create Date: 2022-02-14 22:17:22.612044

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '862ab353389d'
down_revision = '4fec04f7c129'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email')
                    )
    pass


def downgrade():
    op.drop_table('users')
    pass
