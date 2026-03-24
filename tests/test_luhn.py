"""
Tests para el módulo de algoritmo de Luhn.
"""

import pytest

from src.luhn import (
    calculate_luhn_check_digit,
    es_texto_seguro_para_clipboard,
    format_card_number,
    generate_valid_card_number,
    truncar_para_clipboard,
    validate_luhn,
)


class TestValidateLuhn:
    """Tests de validación con algoritmo de Luhn."""

    def test_valid_visa_number(self) -> None:
        """Número Visa válido conocido."""
        assert validate_luhn("4532015112830366") is True

    def test_invalid_number(self) -> None:
        """Número que no pasa Luhn."""
        assert validate_luhn("4532015112830367") is False

    def test_valid_with_spaces(self) -> None:
        """Acepta números con espacios."""
        assert validate_luhn("4532 0151 1283 0366") is True

    def test_short_number_invalid(self) -> None:
        """Números muy cortos son inválidos."""
        assert validate_luhn("1") is False

    def test_empty_invalid(self) -> None:
        """Cadena vacía o sin dígitos."""
        assert validate_luhn("") is False

    def test_too_long_invalid(self) -> None:
        """Números muy largos son inválidos (límite anti-DoS)."""
        assert validate_luhn("1" * 25) is False


class TestCalculateCheckDigit:
    """Tests del cálculo del dígito de control."""

    def test_known_check_digit(self) -> None:
        """Dígito de control para número conocido."""
        assert calculate_luhn_check_digit("453201511283036") == 6

    def test_generated_validates(self) -> None:
        """El dígito calculado produce número válido."""
        partial = "453201511283036"
        check = calculate_luhn_check_digit(partial)
        assert validate_luhn(partial + str(check)) is True


class TestGenerateCardNumber:
    """Tests de generación de números."""

    def test_generated_is_valid(self) -> None:
        """Todo número generado debe pasar Luhn."""
        for _ in range(20):
            num = generate_valid_card_number("4", 16)
            assert validate_luhn(num) is True
            assert len(num) == 16

    def test_respects_prefix(self) -> None:
        """El prefijo debe aparecer al inicio."""
        num = generate_valid_card_number("4532", 16)
        assert num.startswith("4532")
        assert len(num) == 16

    def test_respects_length(self) -> None:
        """Debe respetar la longitud solicitada."""
        for length in (13, 16, 19):
            num = generate_valid_card_number("4", length)
            assert len(num) == length
            assert validate_luhn(num) is True


class TestFormatCardNumber:
    """Tests de formateo."""

    def test_formats_in_groups_of_four(self) -> None:
        """Agrupa en bloques de 4."""
        result = format_card_number("4532015112830366")
        assert result == "4532 0151 1283 0366"

    def test_custom_separator(self) -> None:
        """Acepta separador personalizado."""
        result = format_card_number("4532015112830366", separator="-")
        assert result == "4532-0151-1283-0366"


class TestClipboard:
    """Tests de utilidades para portapapeles."""

    def test_es_texto_seguro_corto(self) -> None:
        """Texto corto es seguro."""
        assert es_texto_seguro_para_clipboard("123") is True

    def test_truncar_no_trunca_corto(self) -> None:
        """Texto corto no se trunca."""
        texto, truncado = truncar_para_clipboard("123\n456")
        assert texto == "123\n456"
        assert truncado is False
