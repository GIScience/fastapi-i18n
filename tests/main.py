from fastapi import FastAPI, Depends

from fastapi_i18n import i18n, _

app = FastAPI(dependencies=[Depends(i18n)])


@app.get("/")
def root():
    return _("Hello from fastapi-i18n!")
