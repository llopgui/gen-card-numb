"""Punto de entrada principal de GEN_CARD_NUMB."""

import logging

from src.config import DEBUG
from src.card_gui import main as run_gui


def main() -> None:
    """Función principal: inicia la aplicación gráfica."""
    if DEBUG:
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(levelname)s %(name)s: %(message)s",
        )
    run_gui()


if __name__ == "__main__":
    main()
