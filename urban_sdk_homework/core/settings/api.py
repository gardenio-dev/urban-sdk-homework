from functools import lru_cache
from typing import Type

from urban_sdk_homework.core.fastapi import APIRouter
from urban_sdk_homework.core.models import BaseModel


# TODO: Errors coming later.
# errors = {
#     403: {"model": ErrorMessage},
#     500: {"model": ErrorMessage},
#     503: {"model": ErrorMessage},
# }


@lru_cache()
def router(settings: Type[BaseModel]) -> APIRouter:
    """Get a settings router."""
    router_ = APIRouter(tags=["Settings"], dependencies=[], prefix="")
    settings_ = settings()

    @router_.get(
        "/",
        name="get-settings",
        response_model=settings,
        response_model_by_alias=True,
        # responses=errors,
    )
    async def get_settings():
        """Get the current settings."""
        return settings_

    return router_
