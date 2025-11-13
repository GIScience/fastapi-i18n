from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from tests import main

client = TestClient(main.app)


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


def test_default_locale():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello from fastapi-i18n!"


def test_de_locale():
    response = client.get("/", headers={"Accept-Language": "de"})
    assert response.status_code == 200
    assert response.json() == "Hallo von fastapi-i18n!"


def test_multiple_locale():
    # example is inspired by headers send from swagger
    response = client.get("/", headers={"Accept-Language": "de-de, en-us;q=0"})
    assert response.status_code == 200
    assert response.json() == "Hallo von fastapi-i18n!"


def test_invalid_locale_fallback():
    response = client.get("/", headers={"Accept-Language": "foo"})
    assert response.status_code == 200
    assert response.json() == "Hello from fastapi-i18n!"


def test_referer_setting_unset():
    # setting Referer should have no effect
    response = client.get(
        "/",
        headers={
            "Accept-Language": "de",
            "Referer": "https://api.quality.ohsome.org/v1-test/docs",
        },
    )
    assert response.status_code == 200
    assert response.json() == "Hallo von fastapi-i18n!"


@pytest.mark.parametrize(
    "referer",
    [
        "https://api.quality.ohsome.org/v1-test/docs",
        "https://ohsome.org/,https://api.quality.ohsome.org/v1-test/docs",
        "foo,https://api.quality.ohsome.org/v1-test/docs",
    ],
)
def test_referer_setting_set(monkeypatch, referer):
    monkeypatch.setenv("FASTAPI_I18N__IGNORE_REFERERS", referer)
    response = client.get(
        "/",
        headers={
            "Accept-Language": "de",
            "Referer": "https://api.quality.ohsome.org/v1-test/docs",
        },
    )
    assert response.status_code == 200
    assert response.json() == "Hello from fastapi-i18n!"


def test_referer_setting_set_no_match(monkeypatch):
    monkeypatch.setenv("FASTAPI_I18N__IGNORE_REFERERS", "https://ohsome.org/")
    response = client.get(
        "/",
        headers={
            "Accept-Language": "de",
            "Referer": "https://api.quality.ohsome.org/v1-test/docs",
        },
    )
    assert response.status_code == 200
    assert response.json() == "Hallo von fastapi-i18n!"
