"""Base marketplace handler contract."""
from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import AsyncIterator

from cs2_sniper.models.listing import Listing
from cs2_sniper.models.filters import WatchFilter


class MarketplaceHandler(ABC):
    """Each marketplace implements fetch + buy + normalize."""

    name: str = "base"

    @abstractmethod
    async def stream_listings(self, watch: WatchFilter) -> AsyncIterator[Listing]:
        """Yield normalized listings matching the watch filter."""

    @abstractmethod
    async def buy(self, listing: Listing) -> bool:
        """Attempt to purchase a listing. Returns True on success."""

    async def close(self) -> None:
        """Release HTTP/WS resources."""