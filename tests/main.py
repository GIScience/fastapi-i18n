from fastapi import Depends, FastAPI

from fastapi_i18n import _, i18n

app = FastAPI(dependencies=[Depends(i18n)])


@app.get("/")
def root():
    return _("Hello from fastapi-i18n!")
