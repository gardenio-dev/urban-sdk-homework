import json
from abc import ABC
from typing import Annotated
from typing import Any
from typing import List
from typing import Literal
from typing import Mapping
from typing import Optional
from typing import Self
from typing import Sequence
from typing import Tuple
from typing import Union

from pydantic import Field
from shapely.geometry import mapping
from shapely.geometry import shape
from shapely.geometry.base import BaseGeometry

from urban_sdk_homework.core.geometry.errors import CrsMismatchException
from urban_sdk_homework.core.geometry.errors import MissingCrsException
from urban_sdk_homework.core.geometry.errors import (
    NonContiguousLineStringException
)
# from urban_sdk_homework.core.geometry.proj import bestsrid
# from urban_sdk_homework.core.geometry.proj import projector
from urban_sdk_homework.core.models import BaseModel


Coordinate = Annotated[
    Union[float, int],
    Field(
        title="coordinate value",
    ),
]

Coordinates = Annotated[
    Tuple[Coordinate, ...],
    Field(title="geometry coordinates", min_items=2, max_items=4),
]


class CrsProperties(BaseModel):
    """Coordinate reference system properties."""

    name: str = Field(description="the CRS identifier")


class Crs(BaseModel):
    """Coordinate reference system details."""

    type: Literal["name"] = Field(
        default="name", description="the CRS definition type"
    )
    properties: CrsProperties = Field(description="CRS properties")


class Geometry(BaseModel, ABC):
    """Base class for geometry types."""

    crs: Optional[Crs] = Field(
        default=None, description="spatial reference details"
    )

    def shape(self) -> BaseGeometry:
        """Create a Shapely geometry based on this shape."""
        return shape(self.model_dump())

    def srid(self) -> Optional[int]:
        """
        Get the spatial reference identifier (SRID) for this geometry's
        coordinate reference system.

        The method may return ``None`` if the CRS does not specify a
        SRID.
        """
        try:
            crs_name = self.crs.properties.name
            return int(crs_name.split(":")[1] if ":" in crs_name else crs_name)
        except (AttributeError, TypeError, ValueError):
            return None

    def reverse(self) -> Self:
        """Get a copy of the geometry with reversed coordinate order."""
        shape_ = self.shape()
        reversed = shapely.reverse(shape_)
        return load(mapping(reversed), crs=self.crs)

    # def simplify(
    #     self, tolerance: float, preserve_topology: bool = True, **kwargs
    # ):
    #     # Make sure we have a coordinate reference system.
    #     try:
    #         proj_ = self.crs.properties.name
    #     except AttributeError:
    #         if not proj_:
    #             raise MissingCrsException(
    #                 "A geometry without a spatial reference cannot be "
    #                 "simplified."
    #             )
    #     bestproj_ = bestsrid(shape)
    #     shape_ = self.shape()
    #     projected = projector(proj_, bestproj_)(shape_)
    #     simplified = shapely.simplify(
    #         projected,
    #         tolerance=tolerance,
    #         preserve_topology=preserve_topology,
    #         **kwargs
    #     )
    #     unprojected = projector(bestproj_, proj_)(simplified)
    #     return load(mapping(unprojected), crs=self.crs)


class Point(Geometry):
    type: str = Field(
        "Point",
        title="Point",
    )
    coordinates: Coordinates

    def reverse(self) -> Self:
        """Get a copy of the geometry with reversed coordinate order."""
        return self


class MultiPoint(Geometry):
    type: str = Field(
        "MultiPoint",
        title="MultiPoint",
    )
    coordinates: List[Coordinates]


class LineString(Geometry):
    type: str = Field(
        "LineString",
        title="Line String",
    )
    coordinates: List[Coordinates]

    def reverse(self) -> Self:
        """Get a copy of the geometry with reversed coordinate order."""
        return LineString(crs=self.crs, coordinates=reversed(self.coordinates))

    @classmethod
    def merge(cls, lines: Sequence[Self]) -> Optional[Self]:
        """Merge multiple linestrings into a single line."""
        # If there's nothing to merge, yield nothing back.
        if not lines:
            return None
        # If there's only one item, it's already "merged" (so to speak).
        if len(lines) == 1:
            return lines[0]
        # Get the spatial reference information from the lines.
        crs = lines[0].crs
        # If any of the spatial references are inconsistent, we have a
        # problem.
        if any(line.crs != crs for line in lines):
            raise CrsMismatchException()
        # Copy the coordinate sets for all of the lines into a list.
        coords = [tuple(line.coordinates) for line in lines]
        # Create a list to hold the coordinates of the new line.  We start
        # with all the coordinates of the first line.
        merged: List[Coordinates] = [*coords.pop(0)]
        for coords_ in coords:
            # Test for continuity.
            if coords_[0] != merged[-1]:
                raise NonContiguousLineStringException()
            # Extend the "merged" coordinates to include all but the first
            # coordinate from the current set.
            merged.extend(coords_[1:])
        # If the last coordinate from the last coordinate set isn't the same
        # as the last coordinate in the merged set, append it.
        if coords_[-1] != merged[-1]:
            merged.append(coords_[-1])
        # Create the new `LineString`.
        return LineString(crs=crs, coordinates=merged)


class MultiLineString(Geometry):
    type: str = Field(
        "MultiLineString",
        title="MultiLineString",
    )
    coordinates: List[List[Coordinates]]


class Polygon(Geometry):
    type: str = Field(
        "Polygon",
        title="Polygon",
    )
    coordinates: List[List[Coordinates]]


class MultiPolygon(Geometry):
    type: str = Field(
        "MultiPolygon",
        title="MultiPolygon",
    )
    coordinates: List[List[List[Coordinates]]]


class GeometryCollection(BaseModel):
    type: str = Field(
        "GeometryCollection",
        title="GeometryCollection",
    )
    geometries: List[Geometry]


class Feature(BaseModel):
    type: str = Field("Feature", title="Feature")
    geometry: Geometry


class FeatureCollection(BaseModel):
    type: str = Field("FeatureCollection", title="FeatureCollection")
    features: List[Feature]


def load(
    geojson: Mapping[str, Any], crs: Union[str, Crs] = None
) -> Union[Geometry, GeometryCollection, Feature, FeatureCollection,]:
    """Load a model from a GeoJSON object."""
    if crs:
        geojson_ = dict(geojson)
        geojson_["crs"] = (
            crs
            if isinstance(crs, Crs)
            else Crs(properties=CrsProperties(name=crs))
        )
    else:
        geojson_ = geojson
    return {
        "Point": Point,
        "MultiPoint": MultiPoint,
        "LineString": LineString,
        "MultiLineString": MultiLineString,
        "Polygon": Polygon,
        "MultiPolygon": MultiPolygon,
        "GeometryCollection": GeometryCollection,
        "Feature": Feature,
        "FeatureCollection": FeatureCollection,
    }[geojson.get("type")].model_validate(geojson_)


def loads(
    text: str, crs: Union[str, Crs] = None
) -> Union[Geometry, GeometryCollection, Feature, FeatureCollection,]:
    """Load a model from a GeoJSON string."""
    try:
        return load(json.loads(text), crs=crs)
    except json.JSONDecodeError:
        return load(mapping(shapely.from_wkt(text)), crs=crs)
