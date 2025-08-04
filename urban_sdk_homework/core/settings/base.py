import inspect
import json
import os
from enum import Enum
from functools import lru_cache
from functools import wraps
from io import StringIO
from pathlib import Path
from textwrap import TextWrapper
from typing import Any
from typing import Dict
from typing import Iterable
from typing import Literal
from typing import Mapping
from typing import Tuple

import pydantic_settings
from dotenv import load_dotenv
from pydantic import Field
from pydantic_core import PydanticUndefined
from pydantic_settings import SettingsConfigDict

from urban_sdk_homework.core.models import BaseModel
from urban_sdk_homework.core.project.metadata import metadata

# Load environment variables from the `.env` file.
load_dotenv()


@lru_cache(maxsize=256)
def env_prefix(*pre: str, sep: str = "__") -> str:
    return f"{sep.join((metadata().package.lower(), *pre))}{sep}"


class EnvironmentVariable(BaseModel):
    """An environment variable definition."""

    path: Tuple[str, ...] = Field(default_factory=tuple)
    name: str = Field(description="the variable name")
    var: str = Field(description="the environment variable")
    type_: str = Field(alias="type", description="the variable type")
    default: Any = Field(description="the default value")
    description: str = Field(description="a description")
    examples: Tuple[Any, ...] = Field(
        description="This is a list of example values."
    )


class BaseSettings(pydantic_settings.BaseSettings):
    """Base class for settings."""

    model_config = SettingsConfigDict(frozen=True)

    def push_env(self) -> Mapping[str, str]:
        """Update the current environment from this settings instance."""
        # Dump this object's values.
        values = self.model_dump(exclude_unset=True, by_alias=False)
        # Create a dict to hold the updated environment variable values.
        updated: Dict[str, str] = {}
        for ev in [v for v in self.env_vars() if v.name in values]:
            value = values[ev.name]
            updated[ev.var] = str(value)
        # Update the environment.
        os.environ.update(updated)
        # Return the updates to the caller.
        return updated

    @classmethod
    def env_vars(
        cls,
        _path: Tuple[str, ...] = None,
        _style: Literal["env", "yaml"] = "env",
    ) -> Iterable[EnvironmentVariable]:
        """Enumerate environment variables."""
        env_prefix_ = cls.model_config.get("env_prefix")
        title_ = cls.model_config.get("title", cls.__name__)
        path_ = (_path if _path is not None else tuple()) + (title_,)
        # Figure out which of the properties are nest `BaseSettings` classes
        # and which appear to be regular fields. This is a little trickier
        # than you might think.
        base_settings = {}
        fields = {}
        # First, do the fields.
        for name, field in cls.model_fields.items():
            try:
                if issubclass(field.annotation, BaseSettings):
                    base_settings[name] = field
                else:
                    fields[name] = field
            except TypeError:
                fields[name] = field
        # Now do the base settings.
        for name, field in fields.items():
            # Resolve the default value.
            if field.default == PydanticUndefined:
                default = field.default
            elif isinstance(field.default, Enum):
                default = {"yaml": field.default.name.lower()}.get(
                    _style, repr(field.default.name.lower())
                )
            elif isinstance(field.default, (str, Path)):
                default = {"yaml": str(field.default)}.get(
                    _style, repr(str(field.default))
                )
            elif isinstance(field.default, (list, tuple)):
                default = {"yaml": str(list(field.default))}.get(
                    _style, repr(field.default)
                )
            else:
                default = repr(field.default)
            # Here it is.
            yield EnvironmentVariable(
                path=path_ if path_ else tuple(),
                name=name,
                var=f"{env_prefix_}{name}",
                type_=str(field.annotation),
                default=default,
                description=field.description or "",
                examples=tuple(field.examples or tuple()),
            )
        for name, field in base_settings.items():
            for env_var_ in field.annotation.env_vars(
                path_ if _path is not None else tuple(),
                _style=_style,
            ):
                yield env_var_

    @classmethod
    def as_env(
        cls, width: int = 79, style: Literal["env", "yaml"] = "env"
    ) -> str:
        """
        Format the configuration class an environment file.

        :param width: the maximum width of the output
        :param style: the formatting style
        """
        # Resolve style-dependent options.
        equals = {"yaml": ": "}.get(style, "=")
        # Let's get a text wrapper for long strings.
        wrapper = TextWrapper(width=width)
        # We'll build the output in a string buffer.
        content = StringIO()
        # Now let's go through all the environment variable definitions.
        for env_var_ in cls.env_vars(_style=style):
            # If a path is specified, we'll prepend it to the variable name.
            if env_var_.path:
                path = "→".join(env_var_.path) if env_var_.path else None
                title = f"{path}→{env_var_.name}"
            else:
                title = env_var_.name
            content.write(f"# {title}\n")
            content.write(f"# {'-' * len(title)}\n")
            # Wrap the description and add it.
            description = "\n# ".join(wrapper.wrap(env_var_.description))
            content.write(f"# {description}\n")
            content.write("# \n")
            content.write("# type:\n")
            content.write(f"# \t{env_var_.type_}\n")
            for example in env_var_.examples:
                example_ = (
                    json.dumps(example)
                    if isinstance(example, dict)
                    else example
                )
                content.write("# example:\n")
                content.write(f"# \t{repr(example_)}\n")
            # Resolve the default value for inclusion in a `.env` file.
            default = (
                ""
                if env_var_.default == PydanticUndefined
                else env_var_.default
            )
            content.write(f"# {env_var_.var}{equals}{default}\n")
            content.write("\n")
        final = content.getvalue()
        return final

    @classmethod
    @lru_cache()
    def these(cls) -> "BaseSettings":
        """Get the current settings."""
        return cls()


def configured(
    settings: str = "settings",
):
    """
    Inject settings.

    :param settings: the name of the argument that hold settings
    :return: the function wrapper
    """

    def decorator(func):
        """Create the function wrapper."""
        # Enumerate the function parameters.
        params = {
            p.name: p.annotation
            for p in inspect.signature(func).parameters.values()
        }
        try:
            settings_ = params[settings]
            if not issubclass(settings_, BaseSettings):
                raise TypeError(
                    f"{settings_.__module__}.{settings_.__class__.__name__} "
                    "is not a subclass of "
                    f"{BaseSettings.__module__}."
                    f"{BaseSettings.__class__.__name__}."
                )
        except KeyError:
            settings_ = None

        @wraps(func)
        def wrapper(*args, **kwargs):
            """Call the function."""
            if settings_ and not kwargs.get(settings):
                kwargs[settings] = settings_.these()
            return func(*args, **kwargs)

        return wrapper

    return decorator
