from typing import List

from fastapi import Depends
from fastapi import Path
from fastapi import Query

from urban_sdk_homework.core.fastapi import APIRouter
from urban_sdk_homework.modules.traffic.api.dependencies import service
from urban_sdk_homework.modules.traffic.models import Link
from urban_sdk_homework.modules.traffic.models import SpatialFilterParams
from urban_sdk_homework.modules.traffic.models import SpeedRecord

# Note to the Future:  Since these traffic endpoints are currently our
# only service endpoints, we'll mount them without a prefix.
# router = APIRouter(tags=["traffic"], prefix="/traffic")
router = APIRouter(tags=["traffic"])


@router.get(
    "/link/{link_id}",
    name="get-link",
    response_model=Link,
)
def link(
    link_id: int = Path(
        description="The unique identifier for the traffic link",
        example=1240632857,
        ge=0,  # Greater than or equal to 1
        title="Link ID",  # Shows up in OpenAPI schema
    ),
    service=Depends(service),
) -> Link:
    """Get the aggregated speed per link for the given day and time period."""
    # TODO: Handle IndexError if link_id is not found.
    return service.get_links(link_id=link_id)[0]


@router.get(
    "/aggregates/",
    name="get-aggregates",
    response_model=List[SpeedRecord],
    response_model_exclude_unset=True,
)
def aggregates(
    day: int = Query(
        description="Day of the week",
        example=2,
        ge=1,
        le=7,
        title="Day of Week",
    ),
    period: int = Query(
        description="Time period", example=7, ge=1, le=7, title="Time Period"
    ),
    service=Depends(service),
) -> List[SpeedRecord]:
    """
    Get the aggregated speed per link for the given day and time period.
    """
    return service.get_aggregates(day=day, period=period)


@router.get(
    "/aggregates/{link_id}",
    name="get-aggregates-by-link",
    response_model=SpeedRecord,
    response_model_exclude_unset=True,
)
def aggregates_by_link(
    link_id: int = Path(
        description="The unique identifier for the traffic link",
        example=1240632857,
        ge=0,
        title="Link ID",
    ),
    day: int = Query(
        description="Day of the week",
        example=2,
        ge=1,
        le=7,
        title="Day of Week",
    ),
    period: int = Query(
        description="Time period", example=7, ge=1, le=7, title="Time Period"
    ),
    service=Depends(service),
) -> SpeedRecord:
    """
    Get the aggregated speed per link for the given day and time period.
    """
    # TODO: Handle IndexError if link_id is not found.
    return service.get_aggregates(link_id=link_id, day=day, period=period)[0]


@router.get(
    "/patterns/slow_links/",
    name="get-slow-links",
    response_model=List[Link],
    response_model_exclude_unset=True,
)
def get_slow_links(
    period: int = Query(
        description="Time period", example=7, ge=1, le=7, title="Time Period"
    ),
    threshold: float = Query(
        description="Speed threshold",
        example=30.0,
        gt=0,
        title="Speed Threshold",
    ),
    min_days: int = Query(
        description=(
            "Minimum number of days the link must be below the threshold to "
            "be considered consistently slo."
        ),
        example=3,
        ge=1,
        title="Minimum Days",
    ),
    service=Depends(service),
) -> List[Link]:
    """
    Get links that have been consistently slow over a period of time.
    """
    return service.get_slow_links(
        period=period, threshold=threshold, min_days=min_days
    )


@router.post(
    "/aggregates/spatial_filter/",
    name="get-aggregates-spatial-filter",
    response_model=List[Link],
    response_model_exclude_unset=True,
)
def get_aggregates_spatial_filter(
    # day: int = Query(
    #     description="Day of the week",
    #     example=2,
    #     ge=1,
    #     le=7,
    #     title="Day of Week"
    # ),
    # period: int = Query(
    #     description="Time period",
    #     example=7,
    #     ge=1,
    #     le=7,
    #     title="Time Period"
    # ),
    # bbox: List[float] = Query(
    #     ...,
    #     description="Bounding box to filter links (minx, miny, maxx, maxy)",
    #     example=[-81.8, 30.1, -81.6, 30.3],
    #     title="Bounding Box",
    #     min_length=4,
    #     max_length=4,
    # ),
    params: SpatialFilterParams,
    service=Depends(service),
) -> List[Link]:
    """
    Get the aggregated speed per link for the given day and time period
    within a specified bounding box.
    """
    return service.get_links(
        bbox=params.bbox, day=params.day, period=params.period
    )
