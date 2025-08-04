import asyncio
import importlib
from abc import ABC
from abc import abstractmethod
from functools import lru_cache
from typing import Any
from typing import List
from typing import Literal
from typing import Mapping
from typing import Self

from urban_sdk_homework.core.auth.models import Friend
from urban_sdk_homework.core.auth.settings import AuthClientSettings
from urban_sdk_homework.core.auth.settings import AuthSettings
from urban_sdk_homework.core.project.metadata import metadata
from urban_sdk_homework.core.settings.base import configured
from urban_sdk_homework.core.strings import snake
from urban_sdk_homework.core.strings import upper_camel


class AuthProvider(ABC):
    """Base class for auth provider implementations."""

    @classmethod
    @abstractmethod
    async def init(cls):
        """Initialize the provider."""

    @classmethod
    @abstractmethod
    def settings(
        cls, profile: Literal["client"] = "client"
    ) -> AuthClientSettings:
        """Get provider settings."""

    @classmethod
    @abstractmethod
    def auth(
        cls,
        permissions: List[str] = None,
        auto_error: bool = True,
        roles: List[str] = None,
        super_user: bool = None,
        multi_tenant: bool = True,
    ) -> Friend:
        """
        Configure endpoint security.

        :param permissions: required permissions
        :param auto_error: raise errors if security fails
        :param roles: required roles
        :param super_user: requires super-user permissions
        :param multi_tenant: require users to be authenticated to the tenant
        """

    @classmethod
    @abstractmethod
    def token(cls, client_id: str, secret: str) -> Mapping[str, Any]:
        """
        Exchange client credentials for a token.

        :param client_id: the client ID
        :param secret: the client secret
        :return: token data
        """

    @classmethod
    @abstractmethod
    def refresh(cls, access: str, refresh: str) -> Mapping[str, Any]:
        """
        Refresh an access token.

        :param access: the access token
        :param refresh: the refresh token
        :return: token data
        """

    @classmethod
    @lru_cache()
    @configured()
    def connect(cls, settings: AuthSettings) -> Self:
        """Get the current auth provider."""
        # Get the provider from the settings.
        provider = settings.provider
        # Work out the fully-qualified path to the provider class.
        classfq = (
            provider
            if "." in provider
            else (
                f"{metadata().package}.modules."
                f"{snake(provider)}.auth.providers."
                f"{upper_camel(provider)}AuthProvider"
            )
        ).split(".")
        # Get the pieces we need...
        classname = classfq[-1]
        modname = ".".join(classfq[:-1])
        # ...to import the module.
        mod = importlib.import_module(modname)
        # If all went well, now we have the provider class.
        provider_ = getattr(mod, classname)
        # We need to instantiate it asynchronously... so...
        try:
            loop = asyncio.get_running_loop()
            # Schedule the coroutine to be run in the event loop
            loop.create_task(provider_.init())
        except RuntimeError:
            # No event loop is running, use asyncio.run()
            asyncio.run(provider_.init())
        # There we go.
        return provider_
