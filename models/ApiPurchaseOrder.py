from enum import Enum
import sqlalchemy as sa
from models.DB import Base
from models.ApiProvider import ApiProvider
from sqlalchemy.orm import relationship
from datetime import datetime
import json


class ApiPurchaseOrderStatus(Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ApiPurchaseOrder(Base):
    __tablename__ = "api_purchase_orders"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(
        sa.BigInteger,
        sa.ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    api_provider = sa.Column(
        sa.Enum(ApiProvider, values_callable=lambda x: [e.value for e in x]),
        default=ApiProvider.G2BULK,
        nullable=False,
    )
    api_order_id = sa.Column(sa.String, nullable=False, unique=True)
    api_game_code = sa.Column(sa.String, nullable=False)
    product_id = sa.Column(sa.Integer, nullable=True)
    denomination_name = sa.Column(sa.String, nullable=False)
    player_id = sa.Column(sa.String, nullable=True)
    player_name = sa.Column(sa.String, nullable=True)
    server_id = sa.Column(sa.String, nullable=True)
    price_usd = sa.Column(sa.Numeric(10, 2), nullable=False)
    price_sudan = sa.Column(sa.Numeric(10, 2), nullable=False)
    status = sa.Column(
        sa.Enum(ApiPurchaseOrderStatus),
        default=ApiPurchaseOrderStatus.PENDING,
        nullable=False,
    )
    api_message = sa.Column(sa.Text, nullable=True)
    remark = sa.Column(sa.Text, nullable=True)
    voucher_codes = sa.Column(sa.Text, nullable=True)

    created_at = sa.Column(sa.DateTime, default=datetime.now)
    updated_at = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)

    user = relationship("User", back_populates="api_purchase_orders")
    api_game = relationship(
        "ApiGame",
        primaryjoin="and_(foreign(ApiPurchaseOrder.api_game_code)==ApiGame.api_game_code, "
        "foreign(ApiPurchaseOrder.api_provider)==ApiGame.provider)",
        viewonly=True,
        uselist=False,
    )

    def set_voucher_codes(self, codes: list):
        if codes:
            self.voucher_codes = json.dumps(codes)
        else:
            self.voucher_codes = None

    def get_voucher_codes(self) -> list:
        if not self.voucher_codes:
            return []
        try:
            return json.loads(self.voucher_codes)
        except json.JSONDecodeError:
            return []

    def __repr__(self):
        return (
            f"ApiPurchaseOrder(id={self.id}, user_id={self.user_id}, "
            f"api_order_id={self.api_order_id}, status={self.status.value})"
        )

    def stringify(self, lang):
        from common.lang_dicts import TEXTS
        from common.common import escape_html, format_datetime, format_float

        texts = TEXTS[lang]
        from common.common import get_status_emoji

        status_emoji = get_status_emoji(self.status)
        status_text = texts.get(
            f"api_order_status_{self.status.value}", self.status.value
        )
        game_display_name = (
            self.api_game.get_display_name(lang) if self.api_game else "N/A"
        )

        lines = [
            f"<b>{texts.get('order_details_text', 'Order Details')}</b>",
            "",
            f"<b>{texts.get('order_id', 'Order ID')}:</b> <code>{self.id}</code>",
            f"<b>{texts.get('api_order_id', 'API Order ID')}:</b> <code>{escape_html(str(self.api_order_id))}</code>",
            f"<b>{texts.get('order_status', 'Status')}:</b> {status_text} {status_emoji}",
            f"<b>{texts.get('game', 'Game')}:</b> {escape_html(game_display_name)}",
            f"<b>{texts.get('denomination', 'Denomination')}:</b> {escape_html(self.denomination_name)}",
        ]

        if self.player_id:
            lines.append(
                f"<b>{texts.get('player_id', 'Player ID')}:</b> <code>{escape_html(self.player_id)}</code>"
            )

        if self.player_name:
            lines.append(
                f"<b>{texts.get('player_name', 'Player Name')}:</b> {escape_html(self.player_name)}"
            )

        if self.server_id:
            lines.append(
                f"<b>{texts.get('server_id', 'Server ID')}:</b> <code>{escape_html(self.server_id)}</code>"
            )

        lines.extend(
            [
                f"<b>{texts.get('price', 'Price')}:</b> <code>{format_float(self.price_sudan)} SDG</code>",
                f"<b>{texts.get('order_date', 'Order Date')}:</b> <code>{format_datetime(self.created_at)}</code>",
            ]
        )

        codes = self.get_voucher_codes()
        if codes:
            lines.append("")
            lines.append(f"<b>{texts.get('voucher_codes', 'Voucher Codes')}:</b>")
            for code in codes:
                lines.append(f"<code>{escape_html(code)}</code>")

        if self.api_message:
            lines.append("")
            lines.append(f"<b>{texts.get('message', 'Message')}:</b>")
            lines.append(f"<i>{escape_html(self.api_message)}</i>")

        if self.remark:
            lines.append("")
            lines.append(f"<b>{texts.get('remark', 'Remark')}:</b>")
            lines.append(f"<i>{escape_html(self.remark)}</i>")

        return "\n".join(lines)

    def is_terminal(self) -> bool:
        return self.status in [
            ApiPurchaseOrderStatus.COMPLETED,
            ApiPurchaseOrderStatus.FAILED,
            ApiPurchaseOrderStatus.CANCELLED,
        ]
