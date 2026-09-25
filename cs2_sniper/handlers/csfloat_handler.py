"""CSFloat marketplace handler."""
from __future__ import annotations

from collections.abc import AsyncIterator

import httpx

from cs2_sniper.config.settings import MarketplaceCredential
from cs2_sniper.handlers.base import MarketplaceHandler
from cs2_sniper.models.filters import WatchFilter
from cs2_sniper.models.listing import Listing
from cs2_sniper.utils.rate_limit import TokenBucket

CSFLOAT_LISTINGS = "https://csfloat.com/api/v1/listings"


class CSFloatHandler(MarketplaceHandler):
    name = "csfloat"

    def __init__(self, cred: MarketplaceCredential) -> None:
        self.cred = cred
        self._bucket = TokenBucket(rate=2.0, capacity=8)
        self._client = httpx.AsyncClient(
            timeout=10.0,
            headers={"Authorization": cred.api_key} if cred.api_key else {},
        )

    async def stream_listings(self, watch: WatchFilter) -> AsyncIterator[Listing]:
        await self._bucket.acquire()
        resp = await self._client.get(
            CSFLOAT_LISTINGS,
            params={"market_hash_name": watch.market_hash_name, "limit": 50},
        )
        resp.raise_for_status()
        for row in resp.json().get("data", []):
            yield Listing(
                marketplace=self.name,
                listing_id=str(row.get("id")),
                market_hash_name=row.get("item", {}).get("market_hash_name", ""),
                price_usd=float(row.get("price", 0)) / 100.0,
                float_value=row.get("item", {}).get("float_value"),
                url=f"https://csfloat.com/item/{row.get('id')}",
            )

    async def buy(self, listing: Listing) -> bool:
        resp = await self._client.post(f"{CSFLOAT_LISTINGS}/{listing.listing_id}/buy")
        return resp.status_code == 200

    async def close(self) -> None:
        await self._client.aclose()