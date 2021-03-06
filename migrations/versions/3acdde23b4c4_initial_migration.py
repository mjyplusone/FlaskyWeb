"""initial migration

Revision ID: 3acdde23b4c4
Revises: a45712c053e1
Create Date: 2017-02-16 15:12:40.427000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3acdde23b4c4'
down_revision = 'a45712c053e1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('confirmed', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'confirmed')
    # ### end Alembic commands ###
