from typing import List
from fastapi import Depends, Query

from fastapi import Path
from urban_sdk_homework.core.fastapi import APIRouter
from urban_sdk_homework.modules.traffic.models import Link, SpeedRecord
from urban_sdk_homework.modules.traffic.api.dependencies import service

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
        title="Link ID"  # Shows up in OpenAPI schema
    ),
    service=Depends(service)
) -> Link:
    """Get the aggregated speed per link for the given day and time period."""
    return service.get_link(link_id=link_id)


@router.get(
    "/aggregates/",
    name="get-aggregates",
    response_model=List[SpeedRecord],
    response_model_exclude_unset=True
)
def aggregates(
    day: int = Query(
        description="Day of the week",
        example=2,
        ge=1,
        le=7,
        title="Day of Week"
    ),
    period: int = Query(
        description="Time period",
        example=7,
        ge=1,
        le=7,
        title="Time Period"
    ),
    service=Depends(service)
) -> List[SpeedRecord]:
    """
    Get the aggregated speed per link for the given day and time period.
    """
    return service.get_aggregates(day=day, period=period)


@router.get(
    "/aggregates/{link_id}",
    name="get-aggregates-by-link",
    response_model=SpeedRecord,
    response_model_exclude_unset=True
)
def aggregates_by_link(
    link_id: int = Path(
        description="The unique identifier for the traffic link",
        example=1240632857,
        ge=0,
        title="Link ID"
    ),
    day: int = Query(
        description="Day of the week",
        example=2,
        ge=1,
        le=7,
        title="Day of Week"
    ),
    period: int = Query(
        description="Time period",
        example=7,
        ge=1,
        le=7,
        title="Time Period"
    ),
    service=Depends(service)
) -> SpeedRecord:
    """
    Get the aggregated speed per link for the given day and time period.
    """
    return service.get_aggregates(
        link_id=link_id,
        day=day,
        period=period
    )[0]  # Return the first result, as we expect only one.
