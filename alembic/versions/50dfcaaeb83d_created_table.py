"""Created table

Revision ID: 50dfcaaeb83d
Revises: cfd32d5d0a79
Create Date: 2023-01-06 10:48:00.637539

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "50dfcaaeb83d"
down_revision = "cfd32d5d0a79"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "post", sa.Column("updated_by", postgresql.UUID(as_uuid=True), nullable=True)
    )
    op.create_foreign_key(None, "post", "users", ["updated_by"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "post", type_="foreignkey")
    op.drop_column("post", "updated_by")
    # ### end Alembic commands ###