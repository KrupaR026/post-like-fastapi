"""Updated table

Revision ID: 1f4dce620290
Revises: 059bd5cbbdab
Create Date: 2022-12-22 14:20:28.867067

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1f4dce620290'
down_revision = '059bd5cbbdab'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('like', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('like', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('like', sa.Column('created_by', sa.String(), nullable=True))
    op.add_column('like', sa.Column('updated_by', sa.String(), nullable=True))
    op.drop_column('like', 'time')
    op.drop_column('like', 'username')
    op.add_column('post', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('post', sa.Column('created_by', sa.String(), nullable=True))
    op.add_column('post', sa.Column('updated_by', sa.String(), nullable=True))
    op.drop_column('post', 'published_at')
    op.add_column('users', sa.Column('created_by', sa.String(), nullable=True))
    op.add_column('users', sa.Column('updated_by', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'updated_by')
    op.drop_column('users', 'created_by')
    op.add_column('post', sa.Column('published_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('post', 'updated_by')
    op.drop_column('post', 'created_by')
    op.drop_column('post', 'created_at')
    op.add_column('like', sa.Column('username', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('like', sa.Column('time', postgresql.TIMESTAMP(), autoincrement=False, nullable=True))
    op.drop_column('like', 'updated_by')
    op.drop_column('like', 'created_by')
    op.drop_column('like', 'updated_at')
    op.drop_column('like', 'created_at')
    # ### end Alembic commands ###