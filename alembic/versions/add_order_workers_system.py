"""add order workers system

Revision ID: add_order_workers
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_order_workers'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    from sqlalchemy import inspect

    conn = op.get_bind()
    inspector = inspect(conn)
    tables = set(inspector.get_table_names())

    if "order_admin_messages" not in tables:
        op.create_table(
            "order_admin_messages",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("order_type", sa.String(), nullable=False),
            sa.Column("order_id", sa.Integer(), nullable=False),
            sa.Column("admin_id", sa.BigInteger(), nullable=False),
            sa.Column("message_id", sa.Integer(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )

    if "charging_balance_orders" in tables:
        cols = {c["name"] for c in inspector.get_columns("charging_balance_orders")}
        if "assigned_admin_id" not in cols:
            with op.batch_alter_table("charging_balance_orders") as batch_op:
                batch_op.add_column(
                    sa.Column("assigned_admin_id", sa.BigInteger(), nullable=True)
                )

    if "purchase_orders" in tables:
        cols = {c["name"] for c in inspector.get_columns("purchase_orders")}
        if "assigned_admin_id" not in cols:
            with op.batch_alter_table("purchase_orders") as batch_op:
                batch_op.add_column(
                    sa.Column("assigned_admin_id", sa.BigInteger(), nullable=True)
                )


def downgrade() -> None:
    # Remove assigned_admin_id column from purchase_orders table
    op.drop_column('purchase_orders', 'assigned_admin_id')
    
    # Remove assigned_admin_id column from charging_balance_orders table
    op.drop_column('charging_balance_orders', 'assigned_admin_id')
    
    # Drop order_admin_messages table
    op.drop_table('order_admin_messages')

