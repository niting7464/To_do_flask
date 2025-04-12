"""empty message

Revision ID: 1fb7c27973cf
Revises: ddd0945caa89
Create Date: 2025-04-12 23:29:11.928218

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1fb7c27973cf'
down_revision = 'ddd0945caa89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.add_column(sa.Column('description', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('file_path', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('task', schema=None) as batch_op:
        batch_op.drop_column('file_path')
        batch_op.drop_column('description')

    # ### end Alembic commands ###
