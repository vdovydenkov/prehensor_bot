# tests/utils/test_format.py
import pytest
from bot.utils.format import format_bytes, format_duration

# --- format_bytes
def test_format_bytes_under_one_kb():
    # проверяем, что числа меньше 1024 остаются в байтах
    assert format_bytes(500) == "500 Б"

def test_format_bytes_exact_kb_and_mb():
    # 1024 байт = 1 КБ
    assert format_bytes(1024) == "1 КБ"
    # чуть больше одного мегабайта
    assert format_bytes(1024**2 + 123456) == "1 МБ"
    # большие значения
    assert format_bytes(5 * 1024**3) == "5 ГБ"

def test_format_bytes_invalid_input():
    # передали не число
    assert format_bytes("1024") is None

# --- format_duration
def test_format_duration_zero_seconds():
    # Проверяем границу 0 секунд
    assert format_duration(0) == "0 секунд"

def test_format_duration_various():
    # 1 секунда
    assert format_duration(1) == "1 секунда"
    # минуты и секунды
    assert format_duration(65) == "1 минута, 5 секунд"
    # часы, минуты, секунды
    assert format_duration(3600 + 62) == "1 час, 1 минута, 2 секунды"

def test_format_duration_invalid_input():
    assert format_duration("100") is None
