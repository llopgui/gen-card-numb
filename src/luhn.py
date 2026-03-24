"""
Módulo de implementación del algoritmo de Luhn.

El algoritmo de Luhn (también conocido como "módulo 10") es una fórmula
de suma de verificación utilizada para validar números de identificación,
especialmente números de tarjetas de crédito y débito.

ADVERTENCIA: Este código es ÚNICAMENTE para fines educativos y de prueba.
Los números generados NO son tarjetas reales ni deben usarse para transacciones.
"""

import re
import secrets


def validate_luhn(number: str) -> bool:
    """
    Valida un número usando el algoritmo de Luhn.

    Args:
        number: Cadena con el número a validar (solo dígitos).

    Returns:
        True si el número pasa la validación de Luhn, False en caso contrario.

    Examples:
        >>> validate_luhn("4532015112830366")
        True
        >>> validate_luhn("4532015112830367")
        False
    """
    digits = re.sub(r"\D", "", number)
    if len(digits) < 2 or len(digits) > _MAX_CARD_LENGTH:
        return False

    total = 0
    # Procesar de derecha a izquierda
    for i, digit in enumerate(reversed(digits)):
        n = int(digit)
        if i % 2 == 1:  # Posiciones pares desde la derecha (índice impar)
            n *= 2
            if n > 9:
                n -= 9  # Equivalente a sumar los dígitos: 16 -> 1+6=7, 16-9=7
        total += n

    return total % 10 == 0


def calculate_luhn_check_digit(partial_number: str) -> int:
    """
    Calcula el dígito de control de Luhn para un número parcial.

    Args:
        partial_number: Número sin el último dígito (o con un placeholder).

    Returns:
        El dígito de control (0-9) que hace válido el número completo.

    Examples:
        >>> calculate_luhn_check_digit("453201511283036")
        6
    """
    digits = re.sub(r"\D", "", partial_number)
    if not digits:
        return 0

    total = 0
    for i, digit in enumerate(reversed(digits)):
        n = int(digit)
        if i % 2 == 0:  # Check digit: posiciones impares desde la derecha
            n *= 2
            if n > 9:
                n -= 9
        total += n

    return (10 - (total % 10)) % 10


def generate_valid_card_number(prefix: str = "4", length: int = 16) -> str:
    """
    Genera un número de tarjeta que pasa la validación de Luhn.

    ADVERTENCIA: Los números generados son FICTICIOS. Solo para pruebas
    y ejercicios educativos. NUNCA usar para transacciones reales.

    Args:
        prefix: Prefijo BIN (primeros dígitos). Por defecto "4" (estilo Visa).
        length: Longitud total del número (típicamente 13, 16 o 19).

    Returns:
        Cadena con un número que pasa la validación de Luhn.
    """
    if length not in (13, 16, 19):
        length = 16
    prefix = re.sub(r"\D", "", prefix)
    if len(prefix) >= length:
        prefix = prefix[: length - 1]

    # Generar dígitos aleatorios hasta completar length-1
    remaining = length - len(prefix) - 1  # -1 para el dígito de control
    if remaining < 0:
        remaining = 0

    rng = secrets.SystemRandom()
    rand_digits = (str(rng.randint(0, 9)) for _ in range(remaining))
    random_digits = "".join(rand_digits)
    partial = prefix + random_digits
    check_digit = calculate_luhn_check_digit(partial)

    return partial + str(check_digit)


# Límite máximo de bytes para copiar al portapapeles (1 MB)
_CLIPBOARD_MAX_BYTES: int = 1_048_576

# Longitud máxima de número de tarjeta para validación (evita DoS)
_MAX_CARD_LENGTH: int = 24


def es_texto_seguro_para_clipboard(texto: str) -> bool:
    """
    Comprueba si un texto es seguro para copiar al portapapeles.

    Args:
        texto: Texto a validar.

    Returns:
        True si el tamaño está dentro del límite permitido.
    """
    if not isinstance(texto, str):
        return False
    return len(texto.encode("utf-8")) <= _CLIPBOARD_MAX_BYTES


def truncar_para_clipboard(texto: str) -> tuple[str, bool]:
    """
    Trunca el texto si excede el límite seguro para el portapapeles.

    Corta en el último salto de línea completo para no partir números.

    Args:
        texto: Texto a procesar.

    Returns:
        Tupla (texto_truncado, fue_truncado).
    """
    if not isinstance(texto, str):
        return ("", True)
    if es_texto_seguro_para_clipboard(texto):
        return (texto, False)
    encoded = texto.encode("utf-8")
    truncated = encoded[:_CLIPBOARD_MAX_BYTES].decode("utf-8", errors="ignore")
    last_newline = truncated.rfind("\n")
    if last_newline > 0:
        truncated = truncated[: last_newline + 1]
    return (truncated.rstrip(), True)


def format_card_number(number: str, separator: str = " ") -> str:
    """
    Formatea un número de tarjeta en grupos de 4 dígitos.

    Args:
        number: Número sin formatear.
        separator: Carácter separador entre grupos.

    Returns:
        Número formateado (ej: "4532 0151 1283 0366").
    """
    digits = re.sub(r"\D", "", number)
    return separator.join(digits[i:i+4] for i in range(0, len(digits), 4))
