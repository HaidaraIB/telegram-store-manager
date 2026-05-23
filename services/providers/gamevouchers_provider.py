from typing import Dict, List, Optional

import models
from services import provider_logging
from models.ApiPurchaseOrder import ApiPurchaseOrderStatus
from services.gamevouchers_api import GameVouchersAPI
from services.instant_purchase_provider import (
    BalanceInfo,
    CreateOrderResult,
    DenominationItem,
    GameListItem,
    OrderStatusResult,
    PlayerValidationResult,
    ProductType,
)


def slugify_category(category_id: int, category_name: str) -> str:
    """Stable game code for ApiGame: gv_{category_id}"""
    return f"gv_{category_id}"


def parse_category_from_code(game_code: str) -> Optional[int]:
    if game_code.startswith("gv_"):
        try:
            return int(game_code[3:])
        except ValueError:
            return None
    return None


class GameVouchersProvider:
    provider = models.ApiProvider.GAMEVOUCHERS
    _log_name = "gamevouchers"

    def __init__(self):
        self._api = GameVouchersAPI()
        self._products_cache: Optional[List[dict]] = None

    async def _get_products(self) -> List[dict]:
        if self._products_cache is None:
            provider_logging.log_api_call(self._log_name, "list_products")
            self._products_cache = await self._api.list_products()
            provider_logging.log_api_call(
                self._log_name, "list_products_ok", count=len(self._products_cache)
            )
        return self._products_cache

    def clear_cache(self):
        self._products_cache = None

    def _group_by_category(self, products: List[dict]) -> Dict[str, GameListItem]:
        games: Dict[str, GameListItem] = {}
        for p in products:
            if not p.get("is_active", True):
                continue
            cat_id = p.get("category_id", 0)
            cat_name = p.get("category_name", "Unknown")
            code = slugify_category(cat_id, cat_name)
            if code not in games:
                games[code] = GameListItem(code=code, name=cat_name)
        return games

    async def list_games(self) -> List[GameListItem]:
        products = await self._get_products()
        return list(self._group_by_category(products).values())

    async def get_denominations(self, game_code: str) -> List[DenominationItem]:
        category_id = parse_category_from_code(game_code)
        if category_id is None:
            return []
        products = await self._get_products()
        result = []
        for p in products:
            if p.get("category_id") != category_id:
                continue
            if not p.get("is_active", True):
                continue
            ptype = p.get("type", "voucher")
            result.append(
                DenominationItem(
                    id=str(p.get("id")),
                    name=p.get("name", ""),
                    price_usd=float(p.get("price", 0)),
                    requires_player_id=p.get("requires_game_uid", False),
                    product_type=(
                        ProductType.TOPUP
                        if ptype == "autotopup"
                        else ProductType.VOUCHER
                    ),
                    delivery_mode=p.get("delivery_mode", "instant"),
                    stock=int(p.get("stock", 0)),
                    raw=p,
                )
            )
        provider_logging.log_catalogue_prices(self._log_name, game_code, result)
        return result

    async def get_balance(self) -> BalanceInfo:
        provider_logging.log_api_call(self._log_name, "get_balance")
        data = await self._api.get_balance()
        info = BalanceInfo(
            available_usd=float(data.get("available", 0)),
            currency=data.get("currency", "USDT"),
        )
        provider_logging.log_wallet_balance(self._log_name, info, raw=data)
        return info

    async def requires_server(self, game_code: str) -> bool:
        return False

    async def get_servers(self, game_code: str) -> Optional[dict]:
        return None

    async def validate_player_id(
        self, game_code: str, player_id: str, server_id: Optional[str] = None
    ) -> PlayerValidationResult:
        if not player_id or not player_id.strip():
            return PlayerValidationResult(valid=False)
        return PlayerValidationResult(valid=True, player_name=None)

    async def create_order(
        self,
        game_code: str,
        denomination: DenominationItem,
        player_id: Optional[str],
        server_id: Optional[str] = None,
        remark: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> CreateOrderResult:
        product_id = int(denomination.id)
        game_uid = player_id if denomination.requires_player_id else None
        raw = denomination.raw or {}
        api_currency = str(raw.get("currency", "USDT"))
        provider_logging.log_price_conversion(
            self._log_name,
            "create_purchase",
            denomination.name,
            denomination.price_usd,
            api_currency,
            product_id=str(product_id),
        )
        provider_logging.log_api_call(
            self._log_name,
            "create_purchase",
            product_id=product_id,
            game_uid=game_uid,
        )
        try:
            data = await self._api.create_purchase(
                product_id=product_id,
                quantity=1,
                game_uid=game_uid,
                client_reference=remark,
                idempotency_key=idempotency_key,
            )
        except Exception as e:
            return CreateOrderResult(
                external_id="",
                message=str(e),
                success=False,
            )
        operation_id = data.get("operation_id", "")
        return CreateOrderResult(
            external_id=str(operation_id),
            message="Purchase accepted",
            success=bool(operation_id),
        )

    async def get_order_status(
        self, external_id: str, game_code: str
    ) -> OrderStatusResult:
        data = await self._api.get_operation(external_id)
        status_str = (data.get("status") or "PROCESSING").upper()
        status_mapping = {
            "PROCESSING": ApiPurchaseOrderStatus.PROCESSING,
            "COMPLETED": ApiPurchaseOrderStatus.COMPLETED,
            "FAILED": ApiPurchaseOrderStatus.FAILED,
            "PENDING": ApiPurchaseOrderStatus.PENDING,
        }
        status = status_mapping.get(status_str, ApiPurchaseOrderStatus.PROCESSING)
        codes = data.get("codes")
        if codes and isinstance(codes, list):
            voucher_codes = [str(c) for c in codes]
        else:
            voucher_codes = None
        return OrderStatusResult(
            status=status,
            message=data.get("error_message") or "",
            voucher_codes=voucher_codes,
        )
