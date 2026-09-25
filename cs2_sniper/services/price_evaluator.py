"""Pure price math for the CS2 Skin Price Sniper."""
from __future__ import annotations

from dataclasses import dataclass

from cs2_sniper.config.settings import Settings
from cs2_sniper.models.listing import Listing


@dataclass(slots=True)
class Decision:
    buy: bool
    discount_percent: float
    reason: str


class PriceEvaluator:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def evaluate(self, listing: Listing) -> Decision:
        if listing.price_usd <= 0:
            return Decision(False, 0.0, "no_price")
        if listing.price_usd > self.settings.max_single_buy_usd:
            return Decision(False, 0.0, "over_budget")
        ref = listing.reference_price_usd or listing.price_usd
        discount = (ref - listing.price_usd) / ref * 100.0 if ref else 0.0
        if discount >= self.settings.min_discount_percent:
            return Decision(True, discount, "underpriced")
        return Decision(False, discount, "not_discounted")