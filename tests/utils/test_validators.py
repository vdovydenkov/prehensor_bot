# tests/utils/test_validators.py
import pytest
from bot.utils.validators import is_http_url

@pytest.mark.parametrize("url,expected", [
    ("http://tiflocomp.ru", True),
    ("https://sub.domain.org/path?query=1", True),
    ("ftp://example.com", False),           # не-http
    ("http://localhost:8000", False),       # локалхост запрещён
    ("https://256.256.256.256", False),     # невалидный IP
    ("not a url", False),
])
def test_is_http_url(url, expected):
    assert is_http_url(url) is expected
