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
            
    def get_link(self, link_id: int) -> Link:
        """
        Get a link by its ID.
        
        :param link_id: The ID of the link to retrieve.
        :return: A Link object with the link's details.
        """
        with Session(self._engine) as session:
            # TODO: Use a more efficient query to fetch only the necessary
            # fields. This query fetches the fid, road_name, and geometry as
            # GeoJSON and we convert it to a `LineString`.  We can do this
            # automatically to prevent repetitive code.
            statement = select(
                Link.link_id,
                Link.road_name,
                Link.length,
                func.ST_AsGeoJSON(Link.geom).label('as_geojson')
            ).where(Link.link_id == link_id)
            
            try:
                result = session.exec(statement).one()
            except NoResultFound:
                raise NotFoundException(f"Link with ID {link_id} not found.")

            # Create a Link object with GeoJSON geometry
            geojson_obj = (
                json.loads(result.as_geojson)
                if result.as_geojson
                else None
            )

            # Create Link object manually (not bound to session)
            link = Link(
                link_id=result.link_id,
                road_name=result.road_name,
                length=result.length,
                geom=geojson.LineString.model_validate(geojson_obj)
            )
            return link

    # def get_slow_links(self, threshold: float) -> Tuple[Link, ...]:
    #     """
    #     Get links with average speed below a certain threshold.
        
    #     :param threshold: The speed threshold below which links are considered slow.
    #     :return: A tuple of Link objects that are considered slow.
    #     """
    #     with Session(self._engine) as session:
    #         statement = select(Link).where(
    #             LinkAggs.average_speed < threshold
    #         ).join(LinkAggs, Link.link_id == LinkAggs.link_id)
    #         result = session.exec(statement).all()
    #         return tuple(result)
    
    
    
    @classmethod
    @lru_cache()
    def connect(cls) -> Self:
        """Connect to the service."""
        return cls()
