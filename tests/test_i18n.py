from pathlib import Path
from unittest.mock import Mock

import pytest

from fastapi_i18n import _, get_locale
from fastapi_i18n.main import i18n


@pytest.fixture(autouse=True)
def test_upper_to_lower(monkeypatch):
    monkeypatch.setenv(
        "FASTAPI_I18N_LOCALE_DIR",
        str(Path(__file__).parent / "locale"),
    )
    monkeypatch.setenv(
        "FASTAPI_I18N_LOCALE_DEFAULT",
        "en",
    )


def test_translate(caplog):
    """Call translate without usage of the FastAPI dependency."""
    assert _("Hello from fastapi-i18n!") == "Hello from fastapi-i18n!"
    assert "FastAPI I18N translator is not set." in caplog.text


def test_get_locale_default():
    assert get_locale() == "en"


def test_get_locale_custom(monkeypatch):
    monkeypatch.setenv(
        "FASTAPI_I18N_LOCALE_DEFAULT",
        "de",
    )
    assert get_locale() == "de"


@pytest.mark.asyncio
async def test_get_locale_context():
    mock = Mock()
    mock.headers.get.return_value = "es"
    gen = i18n(mock)
    await anext(gen)

    assert get_locale() == "es"
