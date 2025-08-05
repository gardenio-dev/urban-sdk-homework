from urban_sdk_homework.core.errors import AppException


class GeometryException(AppException):
    """Base class for geometry exceptions."""


class InvalidEwktException(GeometryException):
    """The EWKT is invalid."""

    code = 400


class InvalidGeoJsonException(GeometryException):
    """The GeoJSON is invalid."""

    code = 400


class NonContiguousLineStringException(GeometryException):
    """The operation requires contiguous linestrings."""

    code = 400


class CrsMismatchException(GeometryException):
    """
    One more more geometries have an inconsistent coordinate reference
    systems.
    """

    code = 400


class MissingCrsException(GeometryException):
    """The coordinate reference system is missing."""

    code = 400
