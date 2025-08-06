from typing import Tuple
from functools import lru_cache
import json
from typing import Self
from urban_sdk_homework.core.services import Service
from urban_sdk_homework.modules.traffic.errors import NotFoundException
from urban_sdk_homework.modules.traffic.models import Link, SpeedRecord
from sqlmodel import select, Session, create_engine, SQLModel
from sqlalchemy import func
from sqlalchemy.exc import NoResultFound
from urban_sdk_homework.core.geometry import geojson

# Note to the Future: If we ever want to implement multi-tenancy, we can
# uncomment the tenant parameter and pass it to the service.
# class TrafficService(Service):
#     """traffic service."""
#
#     def __init__(self, tenant: str):
#         """Create a new instance."""
#         self._tenant = tenant
#
#     @property
#     def tenant(self) -> str:
#         """Get the current tenant."""
#         return self._tenant
#
#     def say_hello(self) -> TrafficHello:
#         """Get a friendly greeting."""
#         return TrafficHello(greeting=f"Hello, {self._tenant}!")
#    
#     @classmethod
#     @lru_cache()
#     def connect(cls, tenant: str) -> Self:
#         """Connect to the service."""
#         return cls(tenant=tenant)


class TrafficService(Service):
    """Traffic service."""

    def __init__(self):
        """Create a new instance."""
        self._engine = create_engine(
            "postgresql://postgres:postgres@host.docker.internal:5432/urbansdk", # TODO: Move to .env.
            echo=True,
        )
        SQLModel.metadata.create_all(self._engine)

    def get_aggregates(
        self,
        day: int,
        period: int,
        link_id: int = None,
        offset: int = 0,
        limit: int = 10
    ) -> Tuple[SpeedRecord, ...]:
        with Session(self._engine) as session:
            statement = select(
                SpeedRecord.link_id,
                SpeedRecord.day_of_week,
                SpeedRecord.period,
                func.avg(SpeedRecord.speed).label('speed')
            ).where(
                SpeedRecord.day_of_week == day,
                SpeedRecord.period == period
            )
            # Only add link_id filter if the argument was supplied.
            if link_id is not None:
                statement = statement.where(SpeedRecord.link_id == link_id)
            # Build the rest of the statement.
            statement = statement.group_by(
                SpeedRecord.link_id,
                SpeedRecord.day_of_week,
                SpeedRecord.period
            ).order_by(
                SpeedRecord.link_id
            ).offset(
                offset
            ).limit(
                limit
            )
            result = session.exec(statement).all()
            return [
                SpeedRecord(
                    link_id=row.link_id,
                    day_of_week=row.day_of_week,
                    period=row.period,
                    speed=row.speed,
                )
                for row in result
            ]

    def get_links(
        self,
        link_id: int = None,
        bbox: Tuple[float, float, float, float] = None,
        offset: int = 0,
        limit: int = 10
    ) -> Tuple[Link, ...]:
        """
        Get links by ID, or all links if no ID is provided.
        :param link_id: The ID of the link to retrieve. If None, returns all links.
        :return: A tuple of Link objects with their details.
        """
        with Session(self._engine) as session:
            # TODO: Use a more efficient query to fetch only the necessary
            # fields. This query fetches the link_id, road_name, and geometry as
            # GeoJSON and we convert it to a `LineString`.  We can do this
            # automatically to prevent repetitive code.
            statement = select(
                Link.link_id,
                Link.road_name,
                Link.length,
                func.ST_AsGeoJSON(Link.geom).label('as_geojson')
            )
            # Only add link_id filter if the caller has supplied one.
            if link_id is not None:
                statement = statement.where(Link.link_id == link_id)
            # If a bounding box is provided, use it to filter the links.
            if bbox is not None:
                # Create a bounding box geometry.
                bbox_geom = func.ST_MakeEnvelope(
                    bbox[0], bbox[1], bbox[2], bbox[3], 4326
                )
                statement = statement.where(
                    func.ST_Intersects(Link.geom, bbox_geom)
                )
            # Add ordering, offset, and limit to the query.
            statement = statement.order_by(
                Link.link_id
            ).offset(
                offset
            ).limit(
                limit
            )
            # Execute the query and fetch results.
            result = session.exec(statement).all()
            # If no results are found, return an empty tuple.
            if not result:
                return tuple()
            return tuple(
                Link(
                    link_id=row.link_id,
                    road_name=row.road_name,
                    length=row.length,
                    geom=(
                        geojson.LineString.model_validate(
                            json.loads(row.as_geojson)
                            if row.as_geojson else None
                        )
                        if row.as_geojson else None
                    )
                ) for row in result
            )
    
    def get_slow_links(
        self,
        period: int,
        threshold: float,
        min_days: int = 3,
        offset: int = 0,
        limit: int = 10,
    ) -> Tuple[Link, ...]:
        with Session(self._engine) as session:
            statement = select(
                Link.link_id,
                Link.road_name,
                Link.length,
                func.avg(SpeedRecord.speed).label('speed'),
                func.ST_AsGeoJSON(Link.geom).label('as_geojson')
            ).join(
                SpeedRecord,
                SpeedRecord.link_id == Link.link_id
            ).where(
                SpeedRecord.period == period,
                SpeedRecord.speed < threshold
            ).group_by(
                Link.link_id,
                Link.road_name,
                Link.length
            ).having(
                func.count(SpeedRecord.id) >= min_days
            ).order_by(
                Link.link_id
            ).offset(
                offset
            ).limit(
                limit
            )
            result = session.exec(statement).all()
            return [
                Link(
                    link_id=row.link_id,
                    road_name=row.road_name,
                    length=row.length,
                    geom=geojson.LineString.model_validate(
                        json.loads(row.as_geojson)
                    ) if row.as_geojson else None
                )
                for row in result
            ]

    @classmethod
    @lru_cache()
    def connect(cls) -> Self:
        """Connect to the service."""
        return cls()
