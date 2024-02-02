"""API entry point
"""

from fastapi import FastAPI
from .auth import router as authorize
from . import constants


app = FastAPI(
    title=constants.API_TITLE,
    description=constants.API_DESCRIPTION,
    summary=constants.API_SUMMARY,
    version=constants.API_VERSION,
)

app.include_router(authorize.router, prefix=constants.AUTH_ROUTE_PREFIX)
