"""Structured logging for instant-purchase API providers (prices, balance, calls)."""

import logging
from typing import Any, Dict, List, Optional

from services.instant_purchase_provider import BalanceInfo, DenominationItem

logger = logging.getLogger("services.api_provider")


def _exchange_rate() -> float:
    from common.common import get_exchange_rate

    return float(get_exchange_rate())


def log_api_call(provider_name: str, operation: str, **details: Any) -> None:
    if details:
        detail_str = " ".join(f"{k}={v!r}" for k, v in details.items())
        logger.info("[%s] %s %s", provider_name, operation, detail_str)
    else:
        logger.info("[%s] %s", provider_name, operation)


def log_wallet_balance(
    provider_name: str,
    balance_info: BalanceInfo,
    raw: Optional[Dict[str, Any]] = None,
) -> None:
    rate = _exchange_rate()
    extra = ""
    if raw:
        extra = f" raw={raw}"
    logger.info(
        "[%s] wallet available=%.4f %s (used for stock checks) | usd_to_sdg_rate=%s%s",
        provider_name,
        balance_info.available_usd,
        balance_info.currency,
        rate,
        extra,
    )


def _api_price_from_raw(denom: DenominationItem) -> tuple[float, str]:
    raw = denom.raw or {}
    currency = str(raw.get("currency", "USD"))
    if "amount" in raw:
        return float(raw.get("amount", denom.price_usd)), currency
    if "price" in raw:
        return float(raw.get("price", denom.price_usd)), currency
    return denom.price_usd, "USD"


def log_catalogue_prices(
    provider_name: str, game_code: str, denoms: List[DenominationItem]
) -> None:
    rate = _exchange_rate()
    logger.info(
        "[%s] catalogue game=%s items=%d | usd_to_sdg_rate=%s",
        provider_name,
        game_code,
        len(denoms),
        rate,
    )
    for denom in denoms:
        api_price, api_currency = _api_price_from_raw(denom)
        sdg = denom.price_usd * rate
        logger.info(
            "[%s]   product=%r id=%s api_price=%.4f %s normalized=%.4f -> SDG %.2f",
            provider_name,
            denom.name,
            denom.id,
            api_price,
            api_currency,
            denom.price_usd,
            sdg,
        )


def log_price_conversion(
    provider_name: str,
    context: str,
    product_name: str,
    api_amount: float,
    api_currency: str = "USD",
    *,
    user_id: Optional[int] = None,
    product_id: Optional[str] = None,
) -> None:
    """Log a single price at the point it is shown or charged to the user."""
    rate = _exchange_rate()
    sdg = api_amount * rate
    user_part = f" user_id={user_id}" if user_id is not None else ""
    id_part = f" product_id={product_id}" if product_id else ""
    logger.info(
        "[%s] %s product=%r%s api_price=%.4f %s -> SDG %.2f (rate=%s)%s",
        provider_name,
        context,
        product_name,
        id_part,
        api_amount,
        api_currency,
        sdg,
        rate,
        user_part,
    )
