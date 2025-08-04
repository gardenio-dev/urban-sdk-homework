from urban_sdk_homework.core.auth.models import Friend
from urban_sdk_homework.core.fastapi import APIRouter
from urban_sdk_homework.core.project.metadata import Metadata
from urban_sdk_homework.core.project.metadata import metadata

router = APIRouter(
    tags=["Project"],
    dependencies=[],
    prefix="",
)

# TODO: Errors coming later.
# errors = {
#     403: {"model": ErrorMessage},
#     500: {"model": ErrorMessage},
#     503: {"model": ErrorMessage},
# }


@router.get(
    "/",
    name="get-metadata",
    response_model=Metadata,
    response_model_by_alias=True,
    response_model_include=("name", "version"),
    response_model_exclude_none=True,  # TODO: Expose in development mode.
    include_in_schema=False,
    # responses=errors,
)
async def meta() -> Friend:
    """Get service metadata."""
    return metadata()
