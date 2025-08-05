from functools import lru_cache
import json
from typing import Self
from urban_sdk_homework.core.services import Service
from urban_sdk_homework.modules.traffic.models import Link, TrafficHello
from sqlmodel import select, Session, create_engine, SQLModel
from sqlalchemy import func
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
        print("Initializing TrafficService...")
        self._engine = create_engine(
            "postgresql://postgres:postgres@host.docker.internal:5432/urbansdk" # TODO: Move to .env.
        )
        SQLModel.metadata.create_all(self._engine)

    def say_hello(self) -> str:
        """Get a friendly greeting."""
        return TrafficHello(greeting="Hello!")

    def get_link(self, link_id: int) -> Link:
        """Get a link by its ID."""
        # with Session(self._engine) as session:
        #     statement = select(Link).where(Link.fid == link_id)
        #     link = session.exec(statement).first()
        #     return link
        # with Session(self._engine) as session:
        #     statement = select(
        #         Link.fid,
        #         Link.road_name,
        #         func.ST_AsGeoJSON(Link.geom).label('geom')
        #     ).where(Link.fid == link_id)
        #     link = session.exec(statement).first()
        #     return link

        with Session(self._engine) as session:
            # TODO: Use a more efficient query to fetch only the necessary 
            # fields. This query fetches the fid, road_name, and geometry as 
            # GeoJSON and we convert it to a `LineString`.  We can do this
            # automatically to prevent repetitive code.
            statement = select(
                Link.fid,
                Link.road_name,
                func.ST_AsGeoJSON(Link.geom).label('geom_as_geojson')
            ).where(Link.fid == link_id)
            
            result = session.exec(statement).first()
            if result is None:
                return None
            
            # Create a Link object with GeoJSON geometry
            geojson_obj = (
                json.loads(result.geom_as_geojson)
                if result.geom_as_geojson
                else None
            )

            # Create Link object manually (not bound to session)
            link = Link(
                fid=result.fid,
                road_name=result.road_name,
                geom=geojson.LineString.model_validate(geojson_obj)
            )
            return link

    @classmethod
    @lru_cache()
    def connect(cls) -> Self:
        """Connect to the service."""
        return cls()
