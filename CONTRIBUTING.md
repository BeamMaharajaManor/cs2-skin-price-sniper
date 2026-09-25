# Contributing to CS2 Skin Price Sniper

Thanks for helping improve the CS2 Skin Price Sniper. This is a Windows desktop
tool that watches CS2 skin marketplaces and fires buy actions on underpriced
listings.

## Development setup

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -m cs2_sniper
```

## Architecture

- `cs2_sniper/handlers/` — marketplace-specific adapters (Steam, CSFloat, Skinport, Buff)
- `cs2_sniper/services/` — sniper engine, price evaluator, notifier
- `cs2_sniper/models/` — pydantic models for listings, filters, targets
- `cs2_sniper/utils/` — rate limiters, currency conversion, logging helpers

## Pull request checklist

- [ ] Tests pass (`pytest`)
- [ ] `ruff check` and `mypy cs2_sniper` clean
- [ ] New marketplace handler registered in `handlers/registry.py`
- [ ] No secrets committed (see SECURITY.md)

## Style

Keep handlers thin: fetch, normalize, yield `Listing` objects. All price math
belongs in `services/price_evaluator.py` so we can unit test it.