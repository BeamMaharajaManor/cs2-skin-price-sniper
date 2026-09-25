"""Skinport marketplace handler (public listings feed)."""
from __future__ import annotations

from collections.abc import AsyncIterator

import httpx

from cs2_sniper.config.settings import MarketplaceCredential
from cs2_sniper.handlers.base import MarketplaceHandler
from cs2_sniper.models.filters import WatchFilter
from cs2_sniper.models.listing import Listing
from cs2_sniper.utils.rate_limit import TokenBucket

SKINPORT_ITEMS = "https://api.skinport.com/v1/items"


class SkinportHandler(MarketplaceHandler):
    name = "skinport"

    def __init__(self, cred: MarketplaceCredential) -> None:
        self.cred = cred
        self._bucket = TokenBucket(rate=0.5, capacity=3)
        self._client = httpx.AsyncClient(timeout=15.0)

    async def stream_listings(self, watch: WatchFilter) -> AsyncIterator[Listing]:
        await self._bucket.acquire()
        resp = await self._client.get(
            SKINPORT_ITEMS,
            params={"app_id": 730, "currency": "USD"},
        )
        resp.raise_for_status()
        for row in resp.json():
            if row.get("market_hash_name") != watch.market_hash_name:
                continue
            yield Listing(
                marketplace=self.name,
                market_hash_name=row["market_hash_name"],
                price_usd=float(row.get("min_price", 0)),
                url=f"https://skinport.com/market?search={row['market_hash_name']}",
            )

    async def buy(self, listing: Listing) -> bool:
        return False

    async def close(self) -> None:
        await self._client.aclose()