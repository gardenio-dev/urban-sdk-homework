from typing import Optional

from pydantic import Field
from pydantic_settings import SettingsConfigDict

from urban_sdk_homework.core.settings.base import BaseSettings
from urban_sdk_homework.core.settings.base import env_prefix


# TODO: Consider moving database connection strings to a centralized config.
class TrafficServiceSettings(BaseSettings):
    """Traffic Service settings."""

    model_config = SettingsConfigDict(
        env_prefix=env_prefix(
            "traffic",
        ),
        title="Traffic Service",
    )
    sqa_conn: Optional[str] = Field(
        default="postgresql://localhost:5432/urbansdk",
        description="A SQLAlchemy database connection string.",
    )
