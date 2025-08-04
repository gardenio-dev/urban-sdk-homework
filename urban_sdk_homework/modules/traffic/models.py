import datetime
from typing import Optional

from pydantic import Field
from urban_sdk_homework.core.models import BaseModel


class TrafficHello(BaseModel):

    timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
        description='Indicates when traffic said "hello".',
    )

    greeting: Optional[str] = Field(
        default=None,
        description="A greeting from traffic.",
    )
