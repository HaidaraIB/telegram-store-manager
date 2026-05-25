from typing import List, Optional

import models
from services import provider_logging
from models.ApiPurchaseOrder import ApiPurchaseOrderStatus
from services.g2bulk_api import G2BulkAPI
from services.instant_purchase_provider import (
    BalanceInfo,
    CreateOrderResult,
    DenominationItem,
    GameListItem,
    OrderStatusResult,
    PlayerValidationResult,
    ProductType,
)


class G2BulkProvider:
    provider = models.ApiProvider.G2BULK
    _log_name = "g2bulk"

    def __init__(self):
        self._api = G2BulkAPI()

    async def list_games(self) -> List[GameListItem]:
        provider_logging.log_api_call(self._log_name, "list_games")
        games = await self._api.get_games()
        provider_logging.log_api_call(self._log_name, "list_games_ok", count=len(games))
        return [
            GameListItem(code=g.get("code", ""), name=g.get("name", g.get("code", "")))
            for g in games
            if g.get("code")
        ]

    async def get_denominations(self, game_code: str) -> List[DenominationItem]:
        provider_logging.log_api_call(
            self._log_name, "get_game_catalogue", game_code=game_code
        )
        catalogue_data = await self._api.get_game_catalogue(game_code)
        items = catalogue_data.get("catalogues", [])
        result = []
        for item in items:
            name = item.get("name", "")
            amount = float(item.get("amount", 0))
            result.append(
                DenominationItem(
                    id=name,
                    name=name,
                    price_usd=amount,
                    requires_player_id=True,
                    product_type=ProductType.TOPUP,
                    raw={**item, "currency": "USD"},
                )
            )
        provider_logging.log_catalogue_prices(self._log_name, game_code, result)
        return result

    async def get_balance(self) -> BalanceInfo:
        provider_logging.log_api_call(self._log_name, "get_me")
        data = await self._api.get_me()
        balance = float(data.get("balance", data.get("usd_balance", 0)))
        info = BalanceInfo(available_usd=balance, currency="USD")
        provider_logging.log_wallet_balance(self._log_name, info, raw=data)
        return info

    async def requires_server(self, game_code: str) -> bool:
        servers = await self._api.get_game_servers(game_code)
        return servers is not None and len(servers) > 0

    async def get_servers(self, game_code: str) -> Optional[dict]:
        return await self._api.get_game_servers(game_code)

    async def validate_player_id(
        self, game_code: str, player_id: str, server_id: Optional[str] = None
    ) -> PlayerValidationResult:
        try:
            result = await self._api.check_player_id(game_code, player_id, server_id)
            valid = result.get("valid") == "valid"
            return PlayerValidationResult(
                valid=valid,
                player_name=result.get("name") if valid else None,
            )
        except Exception:
            return PlayerValidationResult(valid=False)

    async def create_order(
        self,
        game_code: str,
        denomination: DenominationItem,
        player_id: Optional[str],
        server_id: Optional[str] = None,
        remark: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        quantity: int = 1,
    ) -> CreateOrderResult:
        provider_logging.log_price_conversion(
            self._log_name,
            "create_order",
            denomination.name,
            denomination.price_usd,
            "USD",
            product_id=denomination.id,
        )
        provider_logging.log_api_call(
            self._log_name,
            "create_game_order",
            game_code=game_code,
            catalogue=denomination.name,
        )
        order_data = await self._api.create_game_order(
            game_code=game_code,
            catalogue_name=denomination.name,
            player_id=player_id or "",
            server_id=server_id,
            remark=remark,
        )
        if not order_data.get("success"):
            return CreateOrderResult(
                external_id="",
                message=order_data.get("message", "Order failed"),
                success=False,
            )
        order_info = order_data.get("order", {})
        return CreateOrderResult(
            external_id=str(order_info.get("order_id", "")),
            message=order_data.get("message", ""),
            player_name=order_info.get("player_name"),
            success=True,
        )

    async def get_order_status(
        self, external_id: str, game_code: str
    ) -> OrderStatusResult:
        status_data = await self._api.get_order_status(int(external_id), game_code)
        if not status_data.get("success"):
            return OrderStatusResult(
                status=ApiPurchaseOrderStatus.PENDING,
                message=status_data.get("message", ""),
            )
        order_info = status_data.get("order", {})
        new_status_str = (
            order_info.get("status") or status_data.get("status") or ""
        ).lower()
        status_mapping = {
            "pending": ApiPurchaseOrderStatus.PENDING,
            "processing": ApiPurchaseOrderStatus.PROCESSING,
            "completed": ApiPurchaseOrderStatus.COMPLETED,
            "failed": ApiPurchaseOrderStatus.FAILED,
            "cancelled": ApiPurchaseOrderStatus.CANCELLED,
            "canceled": ApiPurchaseOrderStatus.CANCELLED,
        }
        status = status_mapping.get(new_status_str, ApiPurchaseOrderStatus.PENDING)
        return OrderStatusResult(
            status=status,
            message=status_data.get("message") or order_info.get("message") or "",
            player_name=order_info.get("player_name"),
        )
