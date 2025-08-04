from typing import Optional
from typing import Tuple

from pydantic import conint
from pydantic import Field
from pydantic import IPvAnyAddress
from pydantic_settings import SettingsConfigDict

from urban_sdk_homework.core.project.metadata import metadata
from urban_sdk_homework.core.settings.base import BaseSettings
from urban_sdk_homework.core.settings.base import env_prefix


class APICORSConfig(BaseSettings):
    """API Cross-Origin Resource Sharing (CORS) configuration"""

    model_config = SettingsConfigDict(
        env_prefix=env_prefix("api", "cors"), title="CORS"
    )

    allow_origins: Tuple[str, ...] = Field(
        default=("*",),
        description=(
            "These origins (site URLs) that are allowed to contact the API"
        ),
    )
    allow_credentials: bool = Field(
        default=True, description="Allow cookies for cross-origin requests."
    )
    allow_methods: Tuple[str, ...] = Field(
        default=("*",),
        description=(
            "These are the allowed HTTP methods for cross-origin requests."
        ),
    )
    allow_headers: Tuple[str, ...] = Field(
        default=("*",),
        description=(
            "These are the permitted HTTP headers for cross-origin requests"
        ),
    )


class ApiSettings(BaseSettings):
    """Web API settings."""

    model_config = SettingsConfigDict(
        env_prefix=env_prefix(
            "api",
        ),
        title="API",
    )
    title: Optional[str] = Field(
        default=None,
        description="This is an optional title for the web application.",
    )
    entry_point: str = Field(
        default=f"{metadata().package}.modules.api.app:app",
        description="This is the main application entry point.",
    )
    bind: IPvAnyAddress = Field(
        default="127.0.0.1",
        description="Thisis the interface to which the API service binds.",
    )
    port: conint(le=65535) = Field(
        default=8000,
        description=("This is the port on which the API service listens."),
    )
    reload: bool = Field(
        default=False, description="Reload the API when code changes."
    )
    workers: conint(ge=1) = Field(
        default=1,
        description=(
            "This setting controls the number of API worker processes.  If "
            "it isn't set, Uvicorn's WEB_CONCURRENCY environment variable "
            "will be honored.  The default value is based on the number of "
            "available CPUs as detected by the multiprocessing module. "
            "(See https://www.uvicorn.org/settings/#workers.) "
        ),
    )
    limit_concurrency: Optional[int] = Field(
        default=None,
        description=(
            "This setting controls the number of maximum number of concurrent "
            "connections or tasks to allow, before issuing HTTP 503 "
            "responses. Useful for ensuring known memory usage patterns even "
            "under over-resourced loads."
            "(See https://www.uvicorn.org/settings/#resource-limits.) "
        ),
    )
    limit_max_requests: Optional[int] = Field(
        default=None,
        description=(
            "This setting controls the number maximum number of requests to "
            "service before terminating the process. Useful when running "
            "together with a process manager, for preventing memory leaks "
            "from impacting long-running processes."
            "(See https://www.uvicorn.org/settings/#resource-limits.) "
        ),
    )
    docs_url: str = Field(
        default="/openapi",
        description="This is the URI of OpenAPI live documentation.",
    )
    redoc_url: str = Field(
        default="/redoc",
        description="This is the URI of Redoc live documentation.",
    )
    openapi_url: str = Field(
        default="/openapi.json",
        description="This is the URI of OpenAPI definition.",
    )
    cors: APICORSConfig = Field(
        default_factory=APICORSConfig, description=APICORSConfig.__doc__
    )
