from functools import lru_cache
from functools import partial
from typing import Callable
from typing import Union

import pyproj
import shapely.ops
from pyproj import CRS
from pyproj import Proj
from shapely.geometry.base import BaseGeometry


@lru_cache(maxsize=5096)
def proj(init: Union[str, int]) -> Proj:
    """Get a projection."""
    init_ = str(init).lower()
    init_ = init_ if ":" in init_ else f"epsg:{init_}"
    return Proj(init=init_)


@lru_cache(maxsize=1)
def geographic() -> Proj:
    """Get the default geographic coordinate system."""
    return proj("epsg:4326")


@lru_cache(maxsize=1)
def metric() -> Proj:
    """Get the default metric coordinate system."""
    return proj("epsg:3857")


def bestsrid(geom: BaseGeometry, srs: Union[str, int] = "epsg:4326"):
    """
    Get the best projected coordinate system for a geometry.

    :param geom: the geometry
    :param srs: the spatial reference system of the geometry.
    """
    # NOTE TO THE FUTURE: We could do much more here.  For the moment we're
    # just punting to the default metric coordinate system.
    # 1. See if the geometry fits wtihin a single UTM zone.
    # 2. Try global scales like Albers Equal Area or Robinson.
    # 3. https://en.wikipedia.org/wiki/Robinson_projection
    # https://en.wikipedia.org/wiki/Albers_projection
    return "epsg:3857"


def make_for(
    geom: BaseGeometry,
) -> Callable[[BaseGeometry], BaseGeometry]:
    """
    Create a custom projector for a geometry.

    :param geom: a WGS-84 geometry
    :returns: a transformation function for the geometry
    """
    # Get bounds of the geometry.
    minx, miny, maxx, maxy = geom.bounds
    # TODO: Check for coordinates that don't make sense in a lat/lon CRS.
    # Calculate the center X and Y coordinates.
    cx = (minx + maxx) / 2
    cy = (miny, +maxy) / 2
    # The input CRS in WGS84.
    wgs84 = CRS.from_epsg(4326)
    # Create the projected coordinate system from the informatio we have.
    proj_ = CRS.from_proj4(
        f"+proj=tmerc +lat_0={cx} +lon_0={cy} "
        "+k=1 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs"
    )
    # Create the projector.
    transform = partial(pyproj.transform, wgs84, proj_)
    # Create the projection function.
    return lambda geom: shapely.ops.transform(transform, geom)


@lru_cache(maxsize=5098)
def projector(
    source: Union[str, int], dest: Union[str, int]
) -> Callable[[BaseGeometry], BaseGeometry]:
    """
    Get a projector function.
    """
    source_ = source if isinstance(source, Proj) else proj(init=source)
    dest_ = dest if isinstance(dest, Proj) else proj(init=dest)
    # If the source and destination are the same, we can create a simple
    # function that just returns the original geometry.
    if source_ == dest_:
        return lambda geom: geom
    # Construct the transformation.
    transform = partial(pyproj.transform, source_, dest_)
    # Create the projector.
    return lambda geom: shapely.ops.transform(transform, geom)
