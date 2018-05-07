"""empty message

Revision ID: 22b45d160ffd
Revises: 8485fdd3e386
Create Date: 2018-05-07 15:28:38.455990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22b45d160ffd'
down_revision = '8485fdd3e386'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('opinion', sa.String(length=300), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.Column('business_main', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['business_main'], ['businesses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviews')
    # ### end Alembic commands ###