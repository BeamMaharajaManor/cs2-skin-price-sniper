"""Smoke tests for marketplace handler registration."""
from __future__ import annotations

from cs2_sniper.config.settings import MarketplaceCredential, Settings
from cs2_sniper.handlers.registry import build_default_registry


def test_registry_skips_disabled_credentials() -> None:
    settings = Settings(
        marketplaces=[
            MarketplaceCredential("steam", "key", True),
            MarketplaceCredential("skinport", "", False),
        ]
    )
    registry = build_default_registry(settings)
    assert "steam" in registry
    assert "skinport" not in registry


def test_registry_includes_enabled_csfloat() -> None:
    settings = Settings(
        marketplaces=[MarketplaceCredential("csfloat", "abc", True)]
    )
    registry = build_default_registry(settings)
    assert registry["csfloat"].name == "csfloat"