from abc import ABC
from typing import Any

import pydantic_settings
from pydantic import Field
from pydantic import field_validator

from urban_sdk_homework.core.settings.base import BaseSettings


class AuthSettings(BaseSettings, ABC):
    """Base class for auth settings."""

    provider: str = Field(
        default="frontegg",
        description="This identifies the auth provider class.",
    )


class AuthProviderSettings(BaseSettings, ABC):
    """Base class for auth provider settings."""


class AuthClientSettings(pydantic_settings.BaseSettings, ABC):
    """Auth client settings."""

    provider: str = Field(
        description="This value identifies the auth client type."
    )

    @field_validator("provider", mode="before")
    @classmethod
    def validate_provider(cls, value: Any) -> str:
        """Validate the provider."""
        if not value:
            return AuthSettings().provider
        return str(value)
