"""Steam Community Market handler (read-only price feed)."""
from __future__ import annotations

from collections.abc import AsyncIterator

import httpx

from cs2_sniper.config.settings import MarketplaceCredential
from cs2_sniper.handlers.base import MarketplaceHandler
from cs2_sniper.models.filters import WatchFilter
from cs2_sniper.models.listing import Listing
from cs2_sniper.utils.rate_limit import TokenBucket

STEAM_SEARCH = "https://steamcommunity.com/market/search/render/"


class SteamMarketHandler(MarketplaceHandler):
    name = "steam"

    def __init__(self, cred: MarketplaceCredential) -> None:
        self.cred = cred
        self._bucket = TokenBucket(rate=1.0, capacity=5)
        self._client = httpx.AsyncClient(timeout=10.0)

    async def stream_listings(self, watch: WatchFilter) -> AsyncIterator[Listing]:
        await self._bucket.acquire()
        params = {"query": watch.market_hash_name, "appid": 730, "norender": 1}
        resp = await self._client.get(STEAM_SEARCH, params=params)
        resp.raise_for_status()
        for row in resp.json().get("results", []):
            yield Listing(
                marketplace=self.name,
                market_hash_name=row.get("hash_name", ""),
                price_usd=float(row.get("sell_price", 0)) / 100.0,
                wear=watch.wear,
                url=f"https://steamcommunity.com/market/listings/730/{row.get('hash_name','')}",
            )

    async def buy(self, listing: Listing) -> bool:
        # Steam purchases require wallet flows out of scope for auto-snipe.
        return False

    async def close(self) -> None:
        await self._client.aclose()