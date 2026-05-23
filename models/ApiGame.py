import sqlalchemy as sa
from models.DB import Base
from models.ApiProvider import ApiProvider
from datetime import datetime
import models


class ApiGame(Base):
    __tablename__ = "api_games"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    provider = sa.Column(
        sa.Enum(ApiProvider, values_callable=lambda x: [e.value for e in x]),
        default=ApiProvider.G2BULK,
        nullable=False,
    )
    api_game_code = sa.Column(
        sa.String, nullable=False
    )  # Game code from API (e.g., "pubg", "gv_1")
    api_game_name = sa.Column(sa.String, nullable=False)
    arabic_name = sa.Column(sa.String, nullable=True)
    is_active = sa.Column(sa.Boolean, default=True, nullable=False)

    created_at = sa.Column(sa.DateTime, default=datetime.now)
    updated_at = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)


    __table_args__ = (
        sa.UniqueConstraint("provider", "api_game_code", name="uq_api_game_provider_code"),
    )

    def __str__(self):
        return f"{self.api_game_name} ({self.api_game_code})"

    def __repr__(self):
        return (
            f"ApiGame(id={self.id}, provider={self.provider}, "
            f"api_game_code={self.api_game_code}, is_active={self.is_active})"
        )

    def get_display_name(self, lang):
        if lang == models.Language.ARABIC and self.arabic_name:
            return self.arabic_name
        return self.api_game_name

    def stringify(self, lang):
        from common.lang_dicts import TEXTS
        from common.common import escape_html, format_datetime

        texts = TEXTS[lang]
        display_name = self.get_display_name(lang)

        lines = [
            f"<b>{escape_html(display_name)}</b>",
            f"<code>{escape_html(self.api_game_code)}</code>",
            "",
            f"<b>{texts.get('original_name', 'Original Name')}:</b> {escape_html(self.api_game_name)}",
        ]

        if self.arabic_name:
            lines.append(
                f"<b>{texts.get('arabic_name', 'Arabic Name')}:</b> {escape_html(self.arabic_name)}"
            )

        provider_label = texts.get(
            f"api_provider_{self.provider.value}",
            self.provider.value,
        )
        lines.extend(
            [
                "",
                f"<b>{texts.get('api_provider', 'API Provider')}:</b> {escape_html(provider_label)}",
                f"<b>{texts.get('status', 'Status')}:</b> {texts.get('active' if self.is_active else 'inactive', 'N/A')}",
                "",
                f"<b>{texts.get('created', 'Created')}:</b> <code>{format_datetime(self.created_at)}</code>",
                f"<b>{texts.get('updated', 'Updated')}:</b> <code>{format_datetime(self.updated_at)}</code>",
            ]
        )

        return "\n".join(lines)
