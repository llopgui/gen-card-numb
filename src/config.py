"""
Configuración por defecto de la aplicación.

No se usa archivo .env: los valores están definidos aquí.
Para personalizar, modifica estas constantes o amplía este módulo.
"""

from typing import Final

# Identificación de la aplicación
APP_NAME: Final[str] = "GEN_CARD_NUMB"
APP_VERSION: Final[str] = "1.0.0"

# Título de la ventana principal (Tkinter)
WINDOW_TITLE: Final[str] = "Generador Números de Tarjeta (Luhn)"

# Tamaño mínimo de la ventana (px)
WINDOW_MIN_WIDTH: Final[int] = 450
WINDOW_MIN_HEIGHT: Final[int] = 620

# Límites de cantidad en generación por lotes (GUI y validación)
LOTE_MIN: Final[int] = 1
LOTE_MAX: Final[int] = 10_000

# Separadores para exportación / unión de números en lote (etiqueta → carácter)
SEPARADORES: Final[dict[str, str]] = {
    "Línea nueva": "\n",
    "Coma": ",",
    "Punto y coma": ";",
    "Tabulación": "\t",
}

# Prefijos BIN de ejemplo (solo formato visual; números siempre ficticios)
BIN_PRESETS: Final[dict[str, str]] = {
    "Visa (ejemplo)": "4",
    "Mastercard (ejemplo)": "51",
    "Amex (ejemplo)": "34",
    "Discover (ejemplo)": "6011",
    "Personalizado": "",
}

# Paleta de colores de la interfaz (inspirada en diseño SaaS)
COLORES: Final[dict[str, str]] = {
    "fondo": "#f8fafc",
    "superficie": "#ffffff",
    "borde": "#e2e8f0",
    "primario": "#2563eb",
    "primario_hover": "#1d4ed8",
    "exito": "#059669",
    "error": "#dc2626",
    "texto": "#1e293b",
    "texto_secundario": "#64748b",
    "acento_suave": "#dbeafe",
}

# Modo depuración (activa logging en ``main``)
DEBUG: Final[bool] = False
