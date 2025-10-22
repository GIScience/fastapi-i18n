# FastAPI Internationalization (i18n)

[![Build Status](https://jenkins.heigit.org/buildStatus/icon?job=fastapi-i18n/main)](https://jenkins.heigit.org/job/fastapi-i18n/job/main/)
[![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=fastapi-i18n-to-sql&metric=alert_status)](https://sonarcloud.io/dashboard?id=fastapi-i18n-to-sql)
[![LICENSE](https://img.shields.io/github/license/GIScience/fastapi-i18n-to-sql)](COPYING)
[![status: active](https://github.com/GIScience/badges/raw/master/status/active.svg)](https://github.com/GIScience/badges#active)

This package is implemented as a [FastAPI dependency](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/?h=depende) which initializes translations using the [`gettext`](https://docs.python.org/3/library/gettext.html) module and makes them available throughout the request lifecycle using a [Conext Variable](https://docs.python.org/3/library/contextvars.html).

## Installation

```bash
uv add git+https://gitlab.heigit.org/mschaub/fastapi-i18n.git
```

## Prerequisites

A locale directory adhering to the GNU gettext message catalog API containing translated messages. See [chapter on Babel](#Babel) for more details.

## Configuration

```bash
export FASTAPI_I18N_LOCALE_DIR="paht/to/locale/dir"
export FASTAPI_I18N_LOCALE_DEFAULT="de"
```

## Usage

```python
from fastapi import FastAPI, Depends

from fastapi_i18n import i18n, _

app = FastAPI(dependencies=[Depends(i18n)])


@app.get("/")
def root():
    return _("Hello from fastapi-i18n!")
```

Set `Accept-Language` header for requests to get a translated version of the response.

For an complete example see [tests](/tests).

### Babel

Babel is not a dependency of FastAPI i18n, but it is useful for [working with GNU gettext message catalogs](https://babel.pocoo.org/en/latest/messages.html).

To add new locale and use babel to extract messages from Python files run:
```bash
echo "[python: **.py]" > babel.cfg

pybabel extract -F babel.cfg -o messages.pot .
pybabel init -i messages.pot -d locale -l de

# Now translate messages in locale/de/LC_MESSAGES/messages.po

# Then compile locale:
pybabel compile -d locale
```

To update existing locale run `update` instead of `init` run:
```bash
pybabel extract -F babel.cfg -o messages.pot .
pybabel update -i messages.pot -d locale
```


## Roadmap

- [ ] Move to GitHub
- [ ] Support configuration via `pyproject.toml`
- [ ] Validate locale string
- [ ] Support setting locale using query parameter
- [ ] Support configuration of domain (currently defaults to "messages")

## Alternatives

- [FastAPI babel](https://github.com/Anbarryprojects/fastapi-babel)
