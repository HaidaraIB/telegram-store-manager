"""add api provider support (dual G2Bulk / Game Vouchers)

Revision ID: add_api_provider
Revises: add_order_workers
Create Date: 2026-05-23

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect, text

revision = "add_api_provider"
down_revision = "add_order_workers"
branch_labels = None
depends_on = None


def _column_names(inspector, table_name):
    return {c["name"] for c in inspector.get_columns(table_name)}


def upgrade() -> None:
    conn = op.get_bind()
    inspector = inspect(conn)

    if "general_settings" in inspector.get_table_names():
        cols = _column_names(inspector, "general_settings")
        if "active_api_provider" not in cols:
            op.add_column(
                "general_settings",
                sa.Column(
                    "active_api_provider",
                    sa.String(32),
                    nullable=False,
                    server_default="g2bulk",
                ),
            )

    if "api_games" in inspector.get_table_names():
        cols = _column_names(inspector, "api_games")
        if "provider" not in cols:
            _migrate_api_games(conn)

    if "api_purchase_orders" in inspector.get_table_names():
        col_info = [
            c
            for c in inspector.get_columns("api_purchase_orders")
            if c["name"] == "api_order_id"
        ]
        cols = _column_names(inspector, "api_purchase_orders")
        needs_rebuild = col_info and "INT" in str(col_info[0].get("type", "")).upper()
        if needs_rebuild:
            _migrate_api_purchase_orders(conn)
        else:
            if "api_provider" not in cols:
                op.add_column(
                    "api_purchase_orders",
                    sa.Column(
                        "api_provider",
                        sa.String(32),
                        nullable=False,
                        server_default="g2bulk",
                    ),
                )
            if "product_id" not in cols:
                op.add_column(
                    "api_purchase_orders",
                    sa.Column("product_id", sa.Integer(), nullable=True),
                )
            if "voucher_codes" not in cols:
                op.add_column(
                    "api_purchase_orders",
                    sa.Column("voucher_codes", sa.Text(), nullable=True),
                )


def downgrade() -> None:
    # Destructive downgrade not supported for table rebuilds; manual restore required.
    pass


def _migrate_api_games(conn):
    conn.execute(text("ALTER TABLE api_games ADD COLUMN provider VARCHAR(32) DEFAULT 'g2bulk'"))
    conn.execute(text("UPDATE api_games SET provider = 'g2bulk' WHERE provider IS NULL"))
    conn.execute(
        text(
            """
            CREATE TABLE api_games_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                provider VARCHAR(32) NOT NULL DEFAULT 'g2bulk',
                api_game_code VARCHAR NOT NULL,
                api_game_name VARCHAR NOT NULL,
                arabic_name VARCHAR,
                is_active BOOLEAN NOT NULL DEFAULT 1,
                created_at DATETIME,
                updated_at DATETIME,
                UNIQUE (provider, api_game_code)
            )
            """
        )
    )
    conn.execute(
        text(
            """
            INSERT INTO api_games_new
                (id, provider, api_game_code, api_game_name, arabic_name, is_active, created_at, updated_at)
            SELECT id, COALESCE(provider, 'g2bulk'), api_game_code, api_game_name, arabic_name, is_active, created_at, updated_at
            FROM api_games
            """
        )
    )
    conn.execute(text("DROP TABLE api_games"))
    conn.execute(text("ALTER TABLE api_games_new RENAME TO api_games"))


def _migrate_api_purchase_orders(conn):
    conn.execute(
        text(
            """
            CREATE TABLE api_purchase_orders_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id BIGINT NOT NULL,
                api_provider VARCHAR(32) NOT NULL DEFAULT 'g2bulk',
                api_order_id VARCHAR NOT NULL UNIQUE,
                api_game_code VARCHAR NOT NULL,
                product_id INTEGER,
                denomination_name VARCHAR NOT NULL,
                player_id VARCHAR,
                player_name VARCHAR,
                server_id VARCHAR,
                price_usd NUMERIC(10, 2) NOT NULL,
                price_sudan NUMERIC(10, 2) NOT NULL,
                status VARCHAR NOT NULL,
                api_message TEXT,
                remark TEXT,
                voucher_codes TEXT,
                created_at DATETIME,
                updated_at DATETIME,
                FOREIGN KEY(user_id) REFERENCES users(user_id) ON DELETE CASCADE
            )
            """
        )
    )
    conn.execute(
        text(
            """
            INSERT INTO api_purchase_orders_new
                (id, user_id, api_provider, api_order_id, api_game_code, product_id,
                 denomination_name, player_id, player_name, server_id,
                 price_usd, price_sudan, status, api_message, remark,
                 created_at, updated_at)
            SELECT id, user_id, 'g2bulk', CAST(api_order_id AS TEXT), api_game_code, NULL,
                   denomination_name, player_id, player_name, server_id,
                   price_usd, price_sudan, status, api_message, remark,
                   created_at, updated_at
            FROM api_purchase_orders
            """
        )
    )
    conn.execute(text("DROP TABLE api_purchase_orders"))
    conn.execute(text("ALTER TABLE api_purchase_orders_new RENAME TO api_purchase_orders"))
