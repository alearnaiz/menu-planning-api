"""empty message

Revision ID: bd97d00703be
Revises: 758c4b8037f6
Create Date: 2017-06-25 12:54:59.602859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd97d00703be'
down_revision = '758c4b8037f6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('food', sa.Column('url', sa.String(length=100), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('food', 'url')
    # ### end Alembic commands ###
