"""Desktop + log notifications for sniper hits."""
from __future__ import annotations

import structlog

from cs2_sniper.models.listing import Listing

log = structlog.get_logger(__name__)


class Notifier:
    async def announce(self, listing: Listing, bought: bool) -> None:
        status = "BOUGHT" if bought else "MISSED"
        log.info(
            "sniper.notify",
            status=status,
            marketplace=listing.marketplace,
            item=listing.market_hash_name,
            price=listing.price_usd,
            url=listing.url,
        )