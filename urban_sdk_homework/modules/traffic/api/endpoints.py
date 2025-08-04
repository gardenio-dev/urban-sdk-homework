from fastapi import Depends

from urban_sdk_homework.core.fastapi import APIRouter
from urban_sdk_homework.modules.traffic.models import TrafficHello
from urban_sdk_homework.modules.traffic.api.dependencies import service


router = APIRouter(tags=["traffic"], prefix="/traffic")


@router.get(
    "/{tenant}/hello",
    name="say-hello",
    response_model=TrafficHello,
)
def hello(service=Depends(service)) -> TrafficHello:
    """Get a friendly greeting from traffic."""
    return service.say_hello()
