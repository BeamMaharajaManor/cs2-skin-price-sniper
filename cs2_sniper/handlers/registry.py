"""Registry that wires enabled marketplace handlers from settings."""
from __future__ import annotations

from cs2_sniper.config.settings import Settings
from cs2_sniper.handlers.base import MarketplaceHandler
from cs2_sniper.handlers.steam_handler import SteamMarketHandler
from cs2_sniper.handlers.csfloat_handler import CSFloatHandler
from cs2_sniper.handlers.skinport_handler import SkinportHandler


def build_default_registry(settings: Settings) -> dict[str, MarketplaceHandler]:
    registry: dict[str, MarketplaceHandler] = {}
    for cred in settings.marketplaces:
        if not cred.enabled:
            continue
        if cred.name == "steam":
            registry["steam"] = SteamMarketHandler(cred)
        elif cred.name == "csfloat":
            registry["csfloat"] = CSFloatHandler(cred)
        elif cred.name == "skinport":
            registry["skinport"] = SkinportHandler(cred)
    return registry