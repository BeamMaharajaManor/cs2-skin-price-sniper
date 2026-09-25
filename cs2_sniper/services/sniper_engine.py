"""Coordinates handlers, price evaluation, and buy execution."""
from __future__ import annotations

import asyncio

import structlog

from cs2_sniper.config.settings import Settings
from cs2_sniper.handlers.base import MarketplaceHandler
from cs2_sniper.models.filters import WatchFilter
from cs2_sniper.models.listing import Listing
from cs2_sniper.services.price_evaluator import PriceEvaluator
from cs2_sniper.services.notifier import Notifier

log = structlog.get_logger(__name__)


class SniperEngine:
    def __init__(
        self,
        registry: dict[str, MarketplaceHandler],
        settings: Settings,
    ) -> None:
        self.registry = registry
        self.settings = settings
        self.evaluator = PriceEvaluator(settings)
        self.notifier = Notifier()
        self._running = False

    async def run_watch(self, watch: WatchFilter) -> None:
        self._running = True
        tasks = [
            asyncio.create_task(self._consume(name, handler, watch))
            for name, handler in self.registry.items()
        ]
        try:
            await asyncio.gather(*tasks)
        finally:
            self._running = False

    async def _consume(
        self,
        name: str,
        handler: MarketplaceHandler,
        watch: WatchFilter,
    ) -> None:
        async for listing in handler.stream_listings(watch):
            decision = self.evaluator.evaluate(listing)
            if not decision.buy:
                continue
            log.info("sniper.hit", marketplace=name, price=listing.price_usd,
                     discount=decision.discount_percent)
            if self.settings.mode == "live":
                ok = await handler.buy(listing)
                await self.notifier.announce(listing, ok)

    def stop(self) -> None:
        self._running = False