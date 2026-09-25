"""Typed settings loaded from .env and defaults."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

ENV_FILE = Path(".env")


@dataclass(slots=True)
class MarketplaceCredential:
    name: str
    api_key: str = ""
    enabled: bool = False


@dataclass(slots=True)
class Settings:
    version: str = "0.6.3"
    mode: str = "live"  # live | dry_run | backtest
    log_level: str = "INFO"
    poll_interval_seconds: float = 2.5
    max_single_buy_usd: float = 250.0
    min_discount_percent: float = 12.0
    steam_currency: str = "USD"
    marketplaces: list[MarketplaceCredential] = field(default_factory=list)


def load_settings() -> Settings:
    load_dotenv(ENV_FILE, override=False)
    creds = [
        MarketplaceCredential("steam", os.getenv("STEAM_API_KEY", ""), True),
        MarketplaceCredential("csfloat", os.getenv("CSFLOAT_API_KEY", ""), True),
        MarketplaceCredential("skinport", os.getenv("SKINPORT_API_KEY", ""), bool(os.getenv("SKINPORT_API_KEY"))),
        MarketplaceCredential("buff", os.getenv("BUFF_COOKIE", ""), bool(os.getenv("BUFF_COOKIE"))),
    ]
    return Settings(
        mode=os.getenv("SNIPER_MODE", "live"),
        log_level=os.getenv("SNIPER_LOG_LEVEL", "INFO"),
        poll_interval_seconds=float(os.getenv("SNIPER_POLL_INTERVAL", "2.5")),
        max_single_buy_usd=float(os.getenv("SNIPER_MAX_BUY_USD", "250")),
        min_discount_percent=float(os.getenv("SNIPER_MIN_DISCOUNT", "12")),
        marketplaces=creds,
    )