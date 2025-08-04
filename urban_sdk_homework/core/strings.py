import re
from functools import lru_cache
from re import Pattern
from typing import cast

import inflect


@lru_cache
def _inflect() -> inflect.engine:
    return inflect.engine()


@lru_cache()
def _camelsep() -> Pattern:
    """
    Get the pattern that identifies case transitions in a camel-cased string.
    """
    return re.compile(r"(?<=[a-z])(?<![A-Z])(?=[A-Z])|(?=[A-Z][a-z](?!$))")


@lru_cache(maxsize=2048)
def camel2kebab(camel: str) -> str:
    """Convert a camel-cased string to kebab-case."""
    if not camel:
        raise ValueError("The argument cannot be empty.")
    if camel.upper() == camel:
        return camel.lower()
    return _camelsep().sub("-", camel).lower().strip("-").replace(" ", "")


@lru_cache(maxsize=2048)
def upper_camel(s: str) -> str:
    """Convert a string to upper-camel-case."""
    titled = re.sub(r"[^\w]+", " ", s).title()
    return "".join(titled.split(" "))


@lru_cache(maxsize=2048)
def camel2title(camel: str) -> str:
    """Convert a camel-cased string to title-case."""
    if not camel:
        raise ValueError("The argument cannot be empty.")
    if camel.upper() == camel:
        return camel
    return _camelsep().sub(" ", camel).strip()


@lru_cache(maxsize=2048)
def snake2title(snake: str) -> str:
    """Convert a snake-cased string to title-case"""
    spaced = re.sub(r"[\s\_]+", " ", snake)
    return spaced.title()


@lru_cache(maxsize=2048)
def snake(s: str) -> str:
    """Convert a string to snake-case."""
    return re.sub(r"[^a-zA-Z0-9]", "_", s).lower()


@lru_cache(maxsize=2048)
def kebab(s: str) -> str:
    """Convert a string to snake-case."""
    return re.sub(r"[^a-zA-Z0-9]", "-", s).lower()


@lru_cache(maxsize=2048)
def plural(s: str) -> str:
    """Get the pural form of a word."""
    if not s:
        raise ValueError("The argument cannot be empty.")
    if s.upper() == s:
        return f"{s}s"
    # The `inflect` documentation consistently suggests that we pass a `str`
    # to the `plural` function, but the type system specifies a `Word`, so
    # we're casting the value here to make the type linters happy.
    plural = _inflect().plural(cast(inflect.Word, s.lower()))
    if s.istitle():
        return plural.title()
    return plural
