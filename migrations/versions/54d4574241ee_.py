"""empty message

Revision ID: 54d4574241ee
Revises: f3504b40174a
Create Date: 2020-02-29 09:27:55.574427

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54d4574241ee'
down_revision = 'f3504b40174a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=256), nullable=False),
    sa.Column('password', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
