from pathlib import Path
import pytest
from fastapi_i18n import _


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
