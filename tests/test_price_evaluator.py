"""Unit tests for the sniper price evaluator."""
from __future__ import annotations

from cs2_sniper.config.settings import Settings
from cs2_sniper.models.listing import Listing
from cs2_sniper.services.price_evaluator import PriceEvaluator


def _settings(min_discount: float = 10.0, max_buy: float = 500.0) -> Settings:
    return Settings(min_discount_percent=min_discount, max_single_buy_usd=max_buy)


def test_underpriced_listing_triggers_buy() -> None:
    ev = PriceEvaluator(_settings())
    listing = Listing(
        marketplace="csfloat",
        market_hash_name="AK-47 | Redline (Field-Tested)",
        price_usd=18.0,
        reference_price_usd=30.0,
    )
    decision = ev.evaluate(listing)
    assert decision.buy is True
    assert decision.discount_percent > 10.0


def test_over_budget_listing_is_rejected() -> None:
    ev = PriceEvaluator(_settings(max_buy=50.0))
    listing = Listing(
        marketplace="csfloat",
        market_hash_name="AWP | Dragon Lore (Factory New)",
        price_usd=9000.0,
        reference_price_usd=12000.0,
    )
    assert ev.evaluate(listing).buy is False


def test_zero_price_is_rejected() -> None:
    ev = PriceEvaluator(_settings())
    listing = Listing(
        marketplace="steam",
        market_hash_name="P250 | Sand Dune (Minimal Wear)",
        price_usd=0.0,
    )
    assert ev.evaluate(listing).reason == "no_price"