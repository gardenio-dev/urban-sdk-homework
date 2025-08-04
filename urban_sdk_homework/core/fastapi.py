import importlib
import inspect
import re
import weakref
from collections import defaultdict
from functools import wraps
from typing import Any
from typing import Callable
from typing import Iterable

from fastapi import APIRouter as FastAPIRouter
from fastapi.types import DecoratedCallable

from urban_sdk_homework.core import strings
from urban_sdk_homework.core.modules import load_submodules


class APIRouter(FastAPIRouter):
    """
    A FastAPI router.

    This router overrides the `api_route` method to allow callers to specify
    routes with our without trailing slashes.
    """

    #: instance references
    __refs__ = defaultdict(list)

    # @wraps(FastAPIRouter.__init__)
    def __init__(self, *args, enabled: bool = True, **kwargs):
        super().__init__(*args, **kwargs)
        # Update the prefix and tags properties (if necessary).
        frame = inspect.currentframe()
        # We _should_ always have a frame here, but...
        if frame:
            # ...get the calling frame.
            f_back = frame.f_back
            # Get the module for the calling frame.
            mod = inspect.getmodule(f_back) if f_back else None
            # If we have a module, try to infer attributes.
            if mod:
                self._infer_attrs(modname=mod.__name__)

        self._enabled = enabled
        # Keep a reference to the instance.
        self.__refs__[self.__class__].append(weakref.ref(self))

    @property
    def enabled(self) -> bool:
        """Indicates that the router is enabled."""
        return self._enabled

    def _infer_attrs(self, modname: str):
        """Infer this routers' prefix."""
        # If all the values we would infer are already set, there's nothingg
        # to do.
        if self.prefix and self.tags:
            return
        # Get the tokens for all parts of the module name after "modules".
        mod_tokens = modname.split(".")[2:]
        # The module name is the first item in the tokens.
        mod_name = mod_tokens[0]
        # Create a version of the module where the module name and "api"
        # are removed.
        mod_path = tuple(p for p in mod_tokens[2:-1] if p != "api")
        # If the prefix isn't set...
        if self.prefix is None:
            prefix = f"/{'/'.join([mod_name, *mod_path])}"
            self.prefix = prefix
        if not self.tags:
            self.tags = [strings.snake2title(" ".join([mod_name, *mod_path]))]

    @classmethod
    def instances(
        cls, condition: Callable[["APIRouter"], bool], autoload: bool = True
    ) -> Iterable["APIRouter"]:
        """Get instances of the class."""
        # If the caller requests that we automatically load the Web API
        # modules...
        if autoload:
            # ...resolve the name of this package.
            _this = __name__.split(".")[0]

            # Load all API submodules within the modules package.
            load_submodules(
                importlib.import_module(f"{_this}.modules"),
                pattern=re.compile(rf"{_this}.modules\.\w+\.api\..*$"),
            )
        # If no condition has been supplied, the result is always "True".
        condition_ = condition or (lambda i: True)
        # Let's check all instances...
        for instance_ref in cls.__refs__[cls]:
            instance = instance_ref()
            if instance is None:
                continue
            if condition_(instance):
                yield instance

    @wraps(FastAPIRouter.api_route)
    def api_route(
        self, path: str, *, include_in_schema: bool = True, **kwargs: Any
    ) -> Callable[[DecoratedCallable], DecoratedCallable]:
        if path.endswith("/"):
            path = path[:-1]

        alternate_path = path + "/"
        super().api_route(alternate_path, include_in_schema=False, **kwargs)
        return super().api_route(
            path, include_in_schema=include_in_schema, **kwargs
        )
