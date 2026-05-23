import models
from models.ApiProvider import ApiProvider
from services.instant_purchase_provider import InstantPurchaseProvider
from services.providers.g2bulk_provider import G2BulkProvider
from services.providers.gamevouchers_provider import GameVouchersProvider


def get_provider(provider: ApiProvider) -> InstantPurchaseProvider:
    if provider == ApiProvider.G2BULK:
        return G2BulkProvider()
    if provider == ApiProvider.GAMEVOUCHERS:
        return GameVouchersProvider()
    raise ValueError(f"Unknown API provider: {provider}")


def get_active_provider() -> InstantPurchaseProvider:
    with models.session_scope() as s:
        settings = s.query(models.GeneralSettings).first()
        if not settings:
            settings = models.GeneralSettings()
            s.add(settings)
            s.commit()
            s.refresh(settings)
        provider = settings.active_api_provider or ApiProvider.G2BULK
    return get_provider(provider)


def get_active_provider_enum() -> ApiProvider:
    with models.session_scope() as s:
        settings = s.query(models.GeneralSettings).first()
        if not settings:
            return ApiProvider.G2BULK
        return settings.active_api_provider or ApiProvider.G2BULK
