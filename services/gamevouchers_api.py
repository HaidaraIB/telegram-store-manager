import logging
import aiohttp
from typing import Optional, Dict, List, Any
from Config import Config

logger = logging.getLogger("services.api_provider.http")


class GameVouchersAPI:
    def __init__(self, api_key: str = None, base_url: str = None):
        self.api_key = api_key or Config.GAMEVOUCHERS_API_KEY
        self.base_url = (base_url or Config.GAMEVOUCHERS_BASE_URL).rstrip("/")
        if not self.api_key:
            raise ValueError("GAMEVOUCHERS_API_KEY is not set in Config")

    def _get_headers(self, idempotency_key: Optional[str] = None) -> Dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        if idempotency_key:
            headers["Idempotency-Key"] = idempotency_key
        return headers

    async def _request(
        self,
        method: str,
        path: str,
        json: Optional[Dict] = None,
        idempotency_key: Optional[str] = None,
        expected_status: Optional[int] = None,
    ) -> Any:
        url = f"{self.base_url}{path}"
        logger.debug("GameVouchers %s %s", method, path)
        async with aiohttp.ClientSession() as session:
            async with session.request(
                method,
                url,
                headers=self._get_headers(idempotency_key),
                json=json,
            ) as response:
                logger.debug(
                    "GameVouchers %s %s -> HTTP %s", method, path, response.status
                )
                if expected_status and response.status != expected_status:
                    await self._raise_api_error(response)
                if response.status >= 400:
                    await self._raise_api_error(response)
                if response.status == 204:
                    return {}
                data = await response.json()
                if path == "/api/v1/products" and isinstance(data, list):
                    logger.debug(
                        "GameVouchers products sample (first 3): %s",
                        [
                            {
                                "id": p.get("id"),
                                "name": p.get("name"),
                                "price": p.get("price"),
                                "currency": p.get("currency"),
                            }
                            for p in data[:3]
                        ],
                    )
                elif path == "/api/v1/balance":
                    logger.debug("GameVouchers balance response: %s", data)
                return data

    async def _raise_api_error(self, response: aiohttp.ClientResponse):
        try:
            error_data = await response.json()
            detail = error_data.get("detail", error_data)
            if isinstance(detail, list) and detail:
                msg = detail[0].get("msg", str(detail))
            elif isinstance(detail, dict):
                msg = detail.get("message", str(detail))
            else:
                msg = str(detail)
        except Exception:
            msg = await response.text() or f"HTTP {response.status}"
        raise Exception(f"API Error ({response.status}): {msg}")

    async def list_products(self) -> List[Dict[str, Any]]:
        """GET /api/v1/products"""
        return await self._request("GET", "/api/v1/products")

    async def get_balance(self) -> Dict[str, Any]:
        """GET /api/v1/balance"""
        return await self._request("GET", "/api/v1/balance")

    async def create_purchase(
        self,
        product_id: int,
        quantity: int = 1,
        game_uid: Optional[str] = None,
        client_reference: Optional[str] = None,
        idempotency_key: Optional[str] = None,
    ) -> Dict[str, Any]:
        """POST /api/v1/purchases — returns HTTP 202 body"""
        payload: Dict[str, Any] = {"product_id": product_id, "quantity": quantity}
        if game_uid:
            payload["game_uid"] = game_uid
        if client_reference:
            payload["client_reference"] = client_reference

        url = f"{self.base_url}/api/v1/purchases"
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers=self._get_headers(idempotency_key),
                json=payload,
            ) as response:
                if response.status == 202:
                    return await response.json()
                await self._raise_api_error(response)
        return {}

    async def get_operation(self, operation_id: str) -> Dict[str, Any]:
        """GET /api/v1/operations/{operation_id}"""
        return await self._request("GET", f"/api/v1/operations/{operation_id}")
