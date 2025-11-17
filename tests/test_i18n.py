import logging
from pathlib import Path

import pytest
from pytest_approval import verify

from fastapi_i18n import _, get_locale
from fastapi_i18n.main import i18n, parse_accept_language


@pytest.fixture(autouse=True)
def test_upper_to_lower(monkeypatch):
    monkeypatch.setenv(
        "FASTAPI_I18N__LOCALE_DIR",
        str(Path(__file__).parent / "locale"),
    )
    monkeypatch.setenv(
        "FASTAPI_I18N__LOCALE_DEFAULT",
        "en",
    )


def test_translate(caplog):
    """Call translate without usage of the FastAPI dependency."""
    caplog.set_level(logging.DEBUG)
    assert _("Hello from fastapi-i18n!") == "Hello from fastapi-i18n!"
    assert "FastAPI I18N translator is not set." in caplog.text


def test_get_locale_default():
    assert get_locale() == "en"


def test_get_locale_custom(monkeypatch):
    monkeypatch.setenv(
        "FASTAPI_I18N__LOCALE_DEFAULT",
        "de",
    )
    assert get_locale() == "de"


@pytest.mark.asyncio
async def test_get_locale_context():
    gen = i18n("es")
    await anext(gen)
    assert get_locale() == "es"


@pytest.mark.asyncio
async def test_i18n_invalid_locale(caplog):
    gen = i18n("foo")
    await anext(gen)

    assert get_locale() == "en"
    assert verify(caplog.text.splitlines()[0])


def test_parse_accept_language():
    assert parse_accept_language("da, en-gb;q=0.8, en;q=0.7") == ["da", "en_gb", "en"]
    assert parse_accept_language("zh, en-us; q=0.8, en; q=0.6") == ["zh", "en_us", "en"]
    assert parse_accept_language("es-mx, es, en") == ["es_mx", "es", "en"]
    assert parse_accept_language("de; q=1.0, en; q=0.5") == ["de", "en"]
    assert parse_accept_language("de; q=1.0, en; q=0.5") == ["de", "en"]
    assert parse_accept_language("de-de, en-us;q=0") == ["de_de", "en_us"]
