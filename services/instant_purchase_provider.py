from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, List, Protocol, runtime_checkable

import models
from models.ApiPurchaseOrder import ApiPurchaseOrderStatus


class ProductType(str, Enum):
    TOPUP = "topup"
    VOUCHER = "voucher"


@dataclass
class GameListItem:
    code: str
    name: str


@dataclass
class DenominationItem:
    id: str
    name: str
    price_usd: float
    requires_player_id: bool = True
    product_type: ProductType = ProductType.TOPUP
    delivery_mode: str = "instant"
    stock: int = 0
    raw: dict = field(default_factory=dict)


@dataclass
class BalanceInfo:
    available_usd: float
    currency: str = "USD"


@dataclass
class CreateOrderResult:
    external_id: str
    message: str = ""
    player_name: Optional[str] = None
    voucher_codes: Optional[List[str]] = None
    success: bool = True


@dataclass
class OrderStatusResult:
    status: ApiPurchaseOrderStatus
    message: str = ""
    player_name: Optional[str] = None
    voucher_codes: Optional[List[str]] = None


@dataclass
class PlayerValidationResult:
    valid: bool
    player_name: Optional[str] = None


@runtime_checkable
class InstantPurchaseProvider(Protocol):
    provider: models.ApiProvider

    async def list_games(self) -> List[GameListItem]: ...

    async def get_denominations(self, game_code: str) -> List[DenominationItem]: ...

    async def get_balance(self) -> BalanceInfo: ...

    async def requires_server(self, game_code: str) -> bool: ...

    async def get_servers(self, game_code: str) -> Optional[dict]: ...

    async def validate_player_id(
        self, game_code: str, player_id: str, server_id: Optional[str] = None
    ) -> PlayerValidationResult: ...

    async def create_order(
        self,
        game_code: str,
        denomination: DenominationItem,
        player_id: Optional[str],
        server_id: Optional[str] = None,
        remark: Optional[str] = None,
        idempotency_key: Optional[str] = None,
        quantity: int = 1,
    ) -> CreateOrderResult: ...

    async def get_order_status(
        self, external_id: str, game_code: str
    ) -> OrderStatusResult: ...
