# TODO: Read config from pyproject.toml and fail if config is not found


import gettext

from contextvars import ContextVar
import os

from fastapi import Request


class Translator:
    def __init__(self, locale: str):
        locale_dir = os.getenv("FASTAPI_I18N_LOCALE_DIR")
        self.translations = gettext.translation(
            domain="messages",
            localedir=locale_dir,
            languages=[locale],
            fallback=True,
        )

    def translate(self, message: str):
        return self.translations.gettext(message)


translator: ContextVar[Translator] = ContextVar("translator")
locale: ContextVar[str] = ContextVar("locale")


async def i18n(request: Request):
    locale_default = os.getenv("FASTAPI_I18N_LOCALE_DEFAULT")
    locale = request.headers.get("Accept-Language", locale_default)
    token_locale = translator.set(locale)
    token_translator = translator.set(Translator(locale=locale))
    try:
        yield
    finally:
        translator.reset(token_locale)
        translator.reset(token_translator)


def _(message: str) -> str:
    return translator.get().translate(message)
