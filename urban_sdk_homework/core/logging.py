from functools import lru_cache
from typing import Literal
from typing import Optional

import structlog
from pydantic import Field
from pydantic_settings import SettingsConfigDict

from urban_sdk_homework.core.project.metadata import metadata
from urban_sdk_homework.core.settings.base import BaseSettings
from urban_sdk_homework.core.settings.base import env_prefix


class LoggingSettings(BaseSettings):
    """Logging configuration."""

    model_config = SettingsConfigDict(
        env_prefix=env_prefix("logging"), title="Logging"
    )

    level: Literal["debug", "info", "warning", "error", "critical"] = Field(
        default="info", description="This is the logging level."
    )
    format: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="the logging format",
    )
    datefmt: str = Field(
        default="%Y-%m-%d %H:%M:%S",
        description="This is the date format for logging.",
    )
    filename: Optional[str] = Field(
        default=None, description="This is the log file name."
    )
    filemode: Literal["a", "w"] = Field(
        default="a", description="This is the file mode for logging files."
    )


@lru_cache(maxsize=1)
def logger() -> structlog.BoundLogger:
    """Get the logger."""
    return structlog.get_logger(metadata().package)


def configure():
    """Configure the logger."""
    import logging

    structlog.configure(
        # processors=[
        #     structlog.processors.TimeStamper(fmt="iso"),
        #     structlog.processors.JSONRenderer(),
        # ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, LoggingSettings.these().level.upper())
        )
    )
