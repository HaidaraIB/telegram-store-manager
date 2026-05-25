from typing import List
from services.instant_purchase_provider import DenominationItem, GameListItem


def games_to_dict(games: List[GameListItem]) -> list:
    return [{"code": g.code, "name": g.name} for g in games]


def denoms_to_catalogues(denoms: List[DenominationItem]) -> list:
    rows = []
    for d in denoms:
        raw = d.raw or {}
        rows.append(
            {
                "name": d.name,
                "amount": d.price_usd,
                "id": d.id,
                "currency": raw.get("currency", "USD"),
                "requires_player_id": d.requires_player_id,
                "product_type": d.product_type.value,
                "uses_quantity_flow": bool((d.raw or {}).get("uses_quantity_flow")),
                "category_name": (d.raw or {}).get("category_name", ""),
                "delivery_mode": d.delivery_mode,
                "stock": d.stock,
            }
        )
    return rows


def catalogue_to_denomination(catalogue: dict) -> DenominationItem:
    from services.instant_purchase_provider import ProductType

    ptype = catalogue.get("product_type", "topup")
    return DenominationItem(
        id=str(catalogue.get("id", catalogue.get("name", ""))),
        name=catalogue.get("name", ""),
        price_usd=float(catalogue.get("amount", 0)),
        requires_player_id=catalogue.get("requires_player_id", True),
        product_type=(ProductType.VOUCHER if ptype == "voucher" else ProductType.TOPUP),
        delivery_mode=catalogue.get("delivery_mode", "instant"),
        stock=int(catalogue.get("stock", 0)),
        raw=catalogue,
    )
