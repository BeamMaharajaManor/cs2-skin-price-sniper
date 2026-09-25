"""Application wiring: config -> services -> UI."""
from __future__ import annotations

import structlog

from cs2_sniper.config.settings import load_settings
from cs2_sniper.handlers.registry import build_default_registry
from cs2_sniper.services.sniper_engine import SniperEngine
from cs2_sniper.ui.main_window import MainWindow
from cs2_sniper.utils.logging_setup import configure_logging

log = structlog.get_logger(__name__)


def run_desktop(argv: list[str]) -> int:
    settings = load_settings()
    configure_logging(settings.log_level)
    log.info("sniper.startup", version=settings.version, mode=settings.mode)

    registry = build_default_registry(settings)
    engine = SniperEngine(registry=registry, settings=settings)

    window = MainWindow(engine=engine, settings=settings)
    return window.run()