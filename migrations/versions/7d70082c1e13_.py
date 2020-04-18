"""empty message

Revision ID: 7d70082c1e13
Revises: 54d4574241ee
Create Date: 2020-04-18 17:26:27.698095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7d70082c1e13'
down_revision = '54d4574241ee'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('created_by', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'posts', 'users', ['created_by'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'posts', type_='foreignkey')
    op.drop_column('posts', 'created_by')
    # ### end Alembic commands ###
