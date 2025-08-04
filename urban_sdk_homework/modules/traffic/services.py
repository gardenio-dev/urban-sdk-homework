from functools import lru_cache
from typing import Self
from urban_sdk_homework.core.services import Service
from urban_sdk_homework.modules.traffic.models import TrafficHello


class TrafficService(Service):
    """traffic service."""

    def __init__(self, tenant: str):
        """Create a new instance."""
        self._tenant = tenant

    @property
    def tenant(self) -> str:
        """Get the current tenant."""
        return self._tenant

    def say_hello(self) -> TrafficHello:
        """Get a friendly greeting."""
        return TrafficHello(greeting=f"Hello, {self._tenant}!")
    
    @classmethod
    @lru_cache()
    def connect(cls, tenant: str) -> Self:
        """Connect to the service."""
        return cls(tenant=tenant)
