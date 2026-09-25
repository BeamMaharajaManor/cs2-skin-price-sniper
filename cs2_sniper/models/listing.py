"""Normalized listing model shared across marketplace handlers."""
from __future__ import annotations

from pydantic import BaseModel, Field


class Listing(BaseModel):
    marketplace: str
    market_hash_name: str
    price_usd: float
    listing_id: str | None = None
    reference_price_usd: float | None = None
    wear: str | None = None
    float_value: float | None = Field(default=None, ge=0.0, le=1.0)
    url: str | None = None