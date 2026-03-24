"""Tests del módulo de configuración por defecto."""

from src.config import (
    APP_NAME,
    APP_VERSION,
    COLORES,
    DEBUG,
    LOTE_MAX,
    LOTE_MIN,
    SEPARADORES,
    WINDOW_TITLE,
)


def test_config_constants_exist() -> None:
    """Las constantes de configuración están definidas y son coherentes."""
    assert APP_NAME == "GEN_CARD_NUMB"
    assert isinstance(APP_VERSION, str)
    assert len(WINDOW_TITLE) > 0
    assert isinstance(DEBUG, bool)
    assert LOTE_MIN <= LOTE_MAX
    assert "primario" in COLORES
    assert "\n" in SEPARADORES.values()
