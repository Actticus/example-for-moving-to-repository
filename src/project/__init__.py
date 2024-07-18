from contextlib import asynccontextmanager

import fastapi
from fastapi import FastAPI

from . import adapters
from .infrastructure.web_framework import routes

_MB = 1024 ** 2


def init():
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Infrastructure setup
        adapters.engines.Database.init()
        await routes.init(app)
        yield

    app = fastapi.FastAPI(lifespan=lifespan)

    @app.middleware("http")
    async def global_middleware(request: fastapi.Request, handler):
        try:
            return await handler(request)
        except fastapi.exceptions.HTTPException as e:
            raise e
        except Exception:  # pylint: disable=broad-except
            return fastapi.responses.JSONResponse(
                status_code=500,
                content={
                    "detail": {
                        "loc": ["internal"],
                        "msg": "server got itself in trouble",
                        "type": "server_error"
                    }
                }
            )
    return app
