from datetime import datetime
import sqlalchemy as sa
from models.DB import Base
from models.ApiProvider import ApiProvider


class GeneralSettings(Base):
    __tablename__ = "general_settings"

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    usd_to_sudan_rate = sa.Column(sa.Float, nullable=False, default=1.0)
    active_api_provider = sa.Column(
        sa.Enum(ApiProvider, values_callable=lambda x: [e.value for e in x]),
        default=ApiProvider.GAMEVOUCHERS,
        nullable=False,
    )

    created_at = sa.Column(sa.DateTime, default=datetime.now)
    updated_at = sa.Column(sa.DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return (
            f"GeneralSettings(usd_to_sudan_rate={self.usd_to_sudan_rate}, "
            f"active_api_provider={self.active_api_provider})"
        )
