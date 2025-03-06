"""add current price to stocks table

Revision ID: 02fb4eabf9e5
Revises: 53f9536d64a6
Create Date: 2025-03-05 20:57:31.470140

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '02fb4eabf9e5'
down_revision = '53f9536d64a6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stocks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('current_price', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('current_price_date', sa.DateTime(), nullable=True))
        batch_op.add_column(sa.Column('position_value', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stocks', schema=None) as batch_op:
        batch_op.drop_column('position_value')
        batch_op.drop_column('current_price_date')
        batch_op.drop_column('current_price')

    # ### end Alembic commands ###
