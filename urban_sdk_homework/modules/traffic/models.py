from datetime import datetime
from enum import Enum
from typing import List

from geoalchemy2 import Geometry
from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import field_validator
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


class DayOfWeek(str, Enum):
    """Days of the week for traffic data aggregation."""

    Sunday = "Sunday"
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"

    @classmethod
    def from_int(cls, value: int) -> "DayOfWeek":
        """Create DayOfWeek from integer position (1=Sunday, 7=Saturday)."""
        members = list(cls)
        if 1 <= value <= len(members):
            return members[value - 1]  # Convert 1-based to 0-based indexing
        raise ValueError(
            f"Invalid day of week integer: {value}. "
            f"Must be 1-{len(members)}."
        )

    def __int__(self) -> int:
        """Convert DayOfWeek to integer position (1=Sunday, 7=Saturday)."""
        return list(DayOfWeek).index(self) + 1  # Convert 0-based to 1-based


class TimePeriod(str, Enum):
    """Time period for traffic data aggregation."""

    OVERNIGHT = "Overnight"
    EARLY_MORNING = "Early Morning"
    AM_PEAK = "AM Peak"
    MIDDAY = "Midday"
    EARLY_AFTERNOON = "Early Afternoon"
    PM_PEAK = "PM Peak"
    EVENING = "Evening"

    @classmethod
    def from_int(cls, value: int) -> "TimePeriod":
        """Create TimePeriod from integer position (1-7)."""
        members = list(cls)
        if 1 <= value <= len(members):
            return members[value - 1]  # Convert 1-based to 0-based indexing
        raise ValueError(
            f"Invalid time period integer: {value}. "
            f"Must be 1-{len(members)}."
        )

    def __int__(self) -> int:
        """Convert TimePeriod to integer position (1-7)."""
        return list(TimePeriod).index(self) + 1  # Convert 0-based to 1-based


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

    link_id: int = Field(
        description="The ID of the link.",
        title="Link ID",
    )
    road_name: str = Field(
        description="The name of the road to which this link belongs.",
        title="Road Name",
    )
    length: float = Field(
        description="The length of the link in meters.",
        title="Link Length",
    )
    speed: float = Field(title="Average Speed")
    day_of_week: DayOfWeek = Field(
        description="The day of the week for this traffic count.",
        title="Day of Week",
    )
    period: TimePeriod = Field(
        description="The time period for this traffic count.",
        title="Time Period",
    )
    geom: geojson.LineString = Field(
        description="The geometry of the link.",
        title="Link Geometry",
    )

    @field_validator("day_of_week", mode="before")
    @classmethod
    def convert_day_of_week(cls, v):
        """Convert integer (1-7) to DayOfWeek enum value."""
        if isinstance(v, int):
            if 1 <= v <= 7:
                return DayOfWeek.from_int(v)
            else:
                raise ValueError(
                    f"Day of week must be between 1 and 7, got {v}"
                )
        elif isinstance(v, DayOfWeek):
            return v
        else:
            raise ValueError(
                f"Day of week must be an integer or DayOfWeek enum, "
                f"got {type(v)}"
            )

    @field_validator("period", mode="before")
    @classmethod
    def convert_period(cls, v):
        """Convert integer (1-7) to TimePeriod enum value."""
        if isinstance(v, int):
            if 1 <= v <= 7:
                return TimePeriod.from_int(v)
            else:
                raise ValueError(
                    f"Time period must be between 1 and 7, got {v}"
                )
        elif isinstance(v, TimePeriod):
            return v
        else:
            raise ValueError(
                f"Time period must be an integer or TimePeriod enum, "
                f"got {type(v)}"
            )


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
