"""Watch filter describing what the sniper should hunt."""
from __future__ import annotations

from pydantic import BaseModel


class WatchFilter(BaseModel):
    market_hash_name: str
    wear: str | None = None
    stattrak: bool = False
    souvenir: bool = False
    max_price_usd: float | None = None