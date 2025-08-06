from datetime import datetime
from typing import List

from geoalchemy2 import Geometry
from pydantic import ConfigDict
from pydantic import BaseModel
from sqlmodel import Field
from sqlmodel import SQLModel

from urban_sdk_homework.core.geometry import geojson



# class DayOfWeek(IntEnum):
#     """Days of the week for traffic data aggregation."""

#     SUNDAY = 1
#     MONDAY = 2
#     TUESDAY = 3
#     WEDNESDAY = 4
#     THURSDAY = 5
#     FRIDAY = 6
#     SATURDAY = 7


# class TimePeriod(IntEnum):
#     """Time period for traffic data aggregation."""

#     OVERNIGHT = 1
#     EARLY_MORNING = 2
#     AM_PEAK = 3
#     MIDDAY = 4
#     EARLY_AFTERNOON = 5
#     PM_PEAK = 6
#     EVENING = 7


class TrafficSQLModel(SQLModel):
    """Base class for traffic SQLModel models."""

    __table_args__ = {"schema": "traffic"}


class Link(TrafficSQLModel, table=True):
    """A link in the traffic network."""

    __tablename__ = "links"

    link_id: int | None = Field(default=None, primary_key=True)
    road_name: str | None = Field(
        default=None,
        description="This is the name of the road to which this link belongs.",
    )
    length: float | None = Field(
        default=None, description="The length of the link in meters."
    )
    geom: geojson.LineString = Field(
        description="This is the link geometry.",
        sa_type=Geometry("LineString", 4326),
    )


class SpeedRecord(TrafficSQLModel, table=True):
    """Aggregated traffic counts for links."""

    __tablename__ = "speed_records"

    id: int | None = Field(default=None, primary_key=True)
    link_id: int = Field(
        description="The ID of the link to which this traffic count belongs.",
        foreign_key="traffic.links.link_id",
        index=True,
    )
    day_of_week: int = Field(
        description="The day of the week for this traffic count.",
        index=True,
    )
    period: int = Field(
        description="The time period for this traffic count.",
        index=True,
    )
    speed: float = Field(
        description=(
            "The average speed for this link during the specified day and "
            "period."
        ),
    )
    timestamp: datetime = Field(
        default=None,
        description="Indicates when this record was created.",
        index=True,
    )


class Aggregate(BaseModel):
    """Aggregated traffic data for a link."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "link_id": 123,
                "road_name": "Main St",
                "length": 1500.0,
                "speed": 45.5,
                "day_of_week": 2,
                "period": 3,
            }
        }
    )

    # TODO: Add field descriptors.
    link_id: int
    road_name: str
    length: float
    speed: float
    day_of_week: int
    period: int
    geom: geojson.LineString


class SpatialFilterParams(BaseModel):
    """Request model for spatial filtering."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "day": 2,
                "period": 7,
                "bbox": [-81.8, 30.1, -81.6, 30.3],
            }
        }
    )

    day: int = Field(
        description="Day of the week",
        # example=2,
        ge=1,
        le=7,
        title="Day of Week",
    )
    period: int = Field(
        description="Time period",
        # example=7,
        ge=1,
        le=7,
        title="Time Period",
    )
    bbox: List[float] = Field(
        description="Bounding box to filter links (minx, miny, maxx, maxy)",
        # example=[-81.8, 30.1, -81.6, 30.3],
        title="Bounding Box",
        min_length=4,
        max_length=4,
    )
