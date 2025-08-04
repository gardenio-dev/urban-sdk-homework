from abc import ABC
from functools import lru_cache
from typing import Self


class Service(ABC):
    """Base class for services."""

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    @lru_cache()
    def connect(cls, *args, **kwargs) -> Self:
        """Connect to the service."""
        return cls(*args, **kwargs)
