import fastapi

from ...adapters import views


async def init(app: fastapi.FastAPI):
    _ROUTER_CONFIGS: list[dict[str, fastapi.APIRouter | str]] = [
        {"router": views.users.Users().router, "prefix": "/api/v1/users"},
    ]

    for router_config in _ROUTER_CONFIGS:
        app.include_router(**router_config)
