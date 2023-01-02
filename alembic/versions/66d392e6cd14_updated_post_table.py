"""Updated Post table

Revision ID: 66d392e6cd14
Revises: 925d31dc449b
Create Date: 2022-12-27 17:57:45.783326

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "66d392e6cd14"
down_revision = "925d31dc449b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("post", sa.Column("post_display_user", sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("post", "post_display_user")
    # ### end Alembic commands ###
