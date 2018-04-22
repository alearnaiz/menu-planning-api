"""Create table User

Revision ID: f4375e5d4144
Revises: bd97d00703be
Create Date: 2018-04-08 11:44:38.307191

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f4375e5d4144'
down_revision = 'bd97d00703be'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('username', sa.String(length=200), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('username')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###
