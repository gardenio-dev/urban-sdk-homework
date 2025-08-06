from functools import lru_cache
from pathlib import Path
from typing import Optional
from typing import Tuple

import semantic_version
from pydantic import ConfigDict
from pydantic import Field

from urban_sdk_homework.core.errors import AppException
from urban_sdk_homework.core.models import BaseModel


class MetadataException(AppException):
    """An error occurred while inspecting project metadata."""


class MissingMetdataException(AppException):
    """One or more project metadata items are missing."""


class Version(BaseModel):
    """Version information."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    major: int = Field(description="This is the major version.")
    minor: int = Field(description="This is the minor version.")
    patch: int = Field(description="This is the patch version.")
    prerelease: Optional[Tuple[str, ...]] = Field(
        default=None, description="pre-release information"
    )
    build: Optional[Tuple[str, ...]] = Field(
        default=None, description="build information"
    )

    def release(self) -> str:
        """Get the "release" version."""
        return f"{self.major}.{self.minor}"

    def __str__(self) -> str:
        """Get the version as a string."""
        return str(semantic_version.Version(**self.model_dump()))


class Metadata(BaseModel):
    """Project metadata."""

    model_config = ConfigDict(frozen=True, populate_by_name=True)

    name: str = Field(description="This is the name of the project.")
    package: str = Field(description="This is the name of the package.")
    path: Path = Field(
        description="This is the physical location of the package."
    )
    version: Version = Field(
        description="This is the current version information."
    )


@lru_cache()
def metadata() -> Metadata:
    """Get project metadata."""
    # Get metadata for the parent package.
    package = __name__.split(".")[0]

    import urban_sdk_homework

    # try:
    #     metadata = importlib.metadata.metadata(package)
    # except importlib.metadata.PackageNotFoundError:
    #     # from setuptools import pkg_resources
    #     import importlib.util
    #     spec = importlib.util.find_spec(package)
    #     module = spec.load()
    #     metadata = pkg_resources.get_distribution(package)

    #
    # Resolve the current version info.
    semver = semantic_version.Version(urban_sdk_homework.__version__)
    if not semver:
        raise MissingMetdataException(
            """Failed to retrieve semantic version information."""
        )
    return Metadata(
        name=package,
        package=package,
        path=Path(__file__).parent,
        version=Version(
            major=semver.major or 0,
            minor=semver.minor or 0,
            patch=semver.patch or 0,
            prerelease=semver.prerelease or None,
            build=semver.build or None,
        ),
    )
