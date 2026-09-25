"""User-defined snipe targets persisted between sessions."""
from __future__ import annotations

from pydantic import BaseModel

from cs2_sniper.models.filters import WatchFilter


class SnipeTarget(BaseModel):
    label: str
    filter: WatchFilter
    auto_buy: bool = False
    max_quantity: int = 1