from collections.abc import Mapping
import datetime
from enum import IntEnum
from functools import lru_cache
from geoalchemy2 import Geometry
from sqlmodel import Field, SQLModel
from typing import Optional

from urban_sdk_homework.core.geometry import geojson
from urban_sdk_homework.core.models import BaseModel


class DayOfWeek(IntEnum):
    """Days of the week for traffic data aggregation."""

    SUNDAY = 1
    MONDAY = 2
    TUESDAY = 3
    WEDNESDAY = 4
    THURSDAY = 5
    FRIDAY = 6
    SATURDAY = 7


class TimePeriod(IntEnum):
    """Time period for traffic data aggregation."""

    OVERNIGHT = 1
    EARLY_MORNING = 2
    AM_PEAK = 3
    MIDDAY = 4
    EARLY_AFTERNOON = 5
    PM_PEAK = 6
    EVENING = 7


class TrafficHello(BaseModel):

    timestamp: datetime.datetime = Field(
        default_factory=datetime.datetime.now,
        description='Indicates when traffic said "hello".',
    )

    greeting: Optional[str] = Field(
        default=None,
        description="A greeting from traffic.",
    )


class TrafficSQLModel(SQLModel):
    """Base class for traffic SQLModel models."""
    __table_args__ = {"schema": "traffic"}


class Link(TrafficSQLModel, table=True):
    """A link in the traffic network."""
    __tablename__ = "links"

    link_id: int | None = Field(default=None, primary_key=True)
    road_name: str | None = Field(
        default=None,
        description="This is the name of the road to which this link belongs."
    )
    geom: geojson.LineString = Field(
        description="This is the link geometry.",
        sa_type=Geometry("LineString", 4326),
    )


class LinkAggs(TrafficSQLModel, table=True):
    """Aggregated traffic counts for links."""
    __tablename__ = "link_aggs"

    id: int | None = Field(default=None, primary_key=True)
    link_id: int = Field(
        description="The ID of the link to which this traffic count belongs.",
        foreign_key="traffic.links.link_id",
        index=True,
    )
    day_of_week: DayOfWeek = Field(
        description="The day of the week for this traffic count.",
        #sa_column_kwargs={"type_": "SMALLINT"},
        index=True,
    )
    period: TimePeriod = Field(
        description="The time period for this traffic count.",
        #sa_column_kwargs={"type_": "SMALLINT"},
        index=True,
    )
