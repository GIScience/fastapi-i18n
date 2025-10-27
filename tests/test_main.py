from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from tests import main

client = TestClient(main.app)


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


def test_default_locale():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello from fastapi-i18n!"


def test_de_locale():
    response = client.get("/", headers={"Accept-Language": "de"})
    assert response.status_code == 200
    assert response.json() == "Hallo von fastapi-i18n!"
