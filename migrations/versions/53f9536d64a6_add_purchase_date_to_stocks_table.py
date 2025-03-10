"""add purchase date to stocks table

Revision ID: 53f9536d64a6
Revises: 314b7d0b7502
Create Date: 2025-03-03 16:31:36.917153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53f9536d64a6'
down_revision = '314b7d0b7502'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stocks', schema=None) as batch_op:
        batch_op.add_column(sa.Column('purchase_date', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('stocks', schema=None) as batch_op:
        batch_op.drop_column('purchase_date')

    # ### end Alembic commands ###
