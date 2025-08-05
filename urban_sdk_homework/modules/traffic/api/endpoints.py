from fastapi import Depends

from urban_sdk_homework.core.fastapi import APIRouter
from urban_sdk_homework.modules.traffic.models import Link, TrafficHello
from urban_sdk_homework.modules.traffic.api.dependencies import service
from urban_sdk_homework.modules.traffic.models import DayOfWeek, TimePeriod

# Note to the Future:  Since these traffic endpoints are currently our
# only service endpoints, we'll mount them without a prefix.
# router = APIRouter(tags=["traffic"], prefix="/traffic")
router = APIRouter(tags=["traffic"])


@router.get(
    "/hello",
    name="say-hello",
    response_model=TrafficHello,
)
def hello(service=Depends(service)) -> TrafficHello:
    """Get a friendly greeting from traffic."""
    return service.say_hello()

@router.get(
    "/link/{link_id}",
    name="get-link",
    response_model=Link,
)
def link(
    link_id: int,
    service=Depends(service)
) -> Link:
    """
    Get the aggregated speed per link for the given day and time period.
    """
    return service.get_link(link_id=link_id)

@router.get(
    "/aggregates/",
    name="get-link-speed-aggregates",
    #response_model=TrafficHello,
)
def aggregates(
    day: DayOfWeek,
    period: TimePeriod,
    service=Depends(service)
) -> str:
    """
    Get the aggregated speed per link for the given day and time period.
    """
    return f"Implement me! Day: {int(day)}, Period: {period}"


@router.get(
    "/aggregates/{link_id}",
    name="get-aggregates-by-link",
    response_model=Link,
)
def aggregates_by_link(
    link_id: int,
    service=Depends(service)
) -> Link:
    """
    Get the aggregated speed per link for the given day and time period.
    """
    # return service.get_link(link_id=link_id)
